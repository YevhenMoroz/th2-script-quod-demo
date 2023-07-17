from datetime import datetime, timedelta
from pathlib import Path
from random import randint
from xml.etree.ElementTree import parse

from pkg_resources import resource_filename

from custom import basic_custom_actions as bca
from custom.verifier import Verifier
from test_cases.fx.fx_wrapper.common_tools import check_value_in_db
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.environments.full_environment import FullEnvironment
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.fx.ExecutePricedOrderRequestFX import ExecutePricedOrderRequestFX
from test_framework.java_api_wrappers.fx.OrderSubmitFX import OrderSubmitFX
from test_framework.rest_api_wrappers.RestApiManager import RestApiManager
from test_framework.rest_api_wrappers.forex.RestApiOrderCompressionMessages import RestApiOrderCompressionMessages
from test_framework.rest_api_wrappers.forex.RestApiOrderPricingMessages import RestApiOrderPricingMessages
from test_framework.ssh_wrappers.ssh_client import SshClient


class QAP_T2680(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.java_api_connectivity = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.submit_request = OrderSubmitFX(self.data_set)
        self.random_qty_1 = randint(3000000, 4000000)
        self.verifier = Verifier()
        # region SSH
        self.config_file = "client_cs.xml"
        self.ssh_client_env = self.environment.get_list_ssh_client_environment()[0]
        self.ssh_client = SshClient(self.ssh_client_env.host, self.ssh_client_env.port, self.ssh_client_env.user,
                                    self.ssh_client_env.password, self.ssh_client_env.su_user,
                                    self.ssh_client_env.su_password)
        self.local_path = resource_filename("test_resources.be_configs.fx_be_configs", self.config_file)
        self.remote_path = f"/home/quod314/quod/cfg/{self.config_file}"
        self.tree = None
        self.timeout_notif = None
        self.result = None
        self.base_value = str()

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region precondition: Prepare QS configuration
        self.tree = parse(self.local_path)
        self.timeout_notif = self.tree.getroot().find("cs/timeoutNotif")
        self.base_value = self.timeout_notif.text
        self.timeout_notif.text = '10'
        self.tree.write("temp.xml")
        self.ssh_client.send_command('~/automation_scripts/change_permission_script')
        self.ssh_client.put_file(self.remote_path, "temp.xml")
        self.ssh_client.send_command("qrestart CS")
        self.sleep(50)
        # endregion
        # region Step 1
        self.submit_request.set_default_care(recipient=None, role=None).get_parameter("NewOrderSingleBlock")[
            "OrdQty"] = self.random_qty_1
        self.java_api_manager.send_message(self.submit_request)
        # endregion
        # # region Step 3
        order_id = check_value_in_db(extracting_value="ordid",
                                     query=f"SELECT ordid FROM ordr "
                                           f"WHERE ordqty = {self.random_qty_1}")
        self.sleep(10)
        # endregion
        self.result = self.ssh_client.find_regex_pattern("/Logs/quod314/QUOD.ORS.log",
                                                         rf"^.*{order_id}.*FreeNotes.=..Time Out.*$")
        if self.result:
            self.result = "failed"
        else:
            self.result = "pass"
        self.verifier.set_parent_id(self.test_id)
        self.verifier.set_event_name("Check that Care Order is timed out")
        self.verifier.compare_values("status", "pass", self.result)
        self.verifier.verify()
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.timeout_notif.text = self.base_value
        self.tree.write("temp.xml")
        self.ssh_client.send_command('~/automation_scripts/change_permission_script')
        self.ssh_client.put_file(self.remote_path, "temp.xml")
        self.ssh_client.send_command("qrestart CS")
        self.sleep(50)
