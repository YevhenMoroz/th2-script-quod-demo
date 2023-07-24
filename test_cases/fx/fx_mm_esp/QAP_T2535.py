import time
from pathlib import Path
from pkg_resources import resource_filename
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from custom import basic_custom_actions as bca
from test_framework.environments.full_environment import FullEnvironment
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.forex.FixMessageMarketDataRequestFX import FixMessageMarketDataRequestFX
from test_framework.fix_wrappers.forex.FixMessageNewOrderSingleFX import FixMessageNewOrderSingleFX
from test_framework.fix_wrappers.forex.FixMessageNewOrderSingleTaker import FixMessageNewOrderSingleTaker
from test_framework.ssh_wrappers.ssh_client import SshClient
from xml.etree.ElementTree import parse as parse_xml


class QAP_T2535(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.buy_side_esp_env = self.fix_env.buy_side_esp
        self.ss_connectivity = self.fix_env.sell_side_esp
        self.fix_manager_gtw = FixManager(self.ss_connectivity, self.test_id)
        self.md_request = FixMessageMarketDataRequestFX(data_set=self.data_set)
        self.new_order_single = FixMessageNewOrderSingleFX(data_set=self.data_set)
        self.new_order = FixMessageNewOrderSingleTaker(data_set=self.data_set)
        self.fix_manager = FixManager(self.buy_side_esp_env, self.test_id)
        self.eur_usd = self.data_set.get_symbol_by_name('symbol_1')
        self.security_type = self.data_set.get_security_type_by_name("fx_spot")
        self.settle_type = self.data_set.get_settle_type_by_name("spot")
        # region SSH
        self.config_file = "client_ors.xml"
        self.ssh_client_env = self.environment.get_list_ssh_client_environment()[0]
        self.ssh_client = SshClient(self.ssh_client_env.host, self.ssh_client_env.port, self.ssh_client_env.user,
                                    self.ssh_client_env.password, self.ssh_client_env.su_user,
                                    self.ssh_client_env.su_password)
        self.local_path = resource_filename("test_resources.be_configs.fx_be_configs", self.config_file)
        self.remote_path = f"/home/quod314/quod/cfg/{self.config_file}"
        self.tree = None
        self.making_internal = None
        self.result = None

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region precondition: Prepare QS configuration
        self.tree = parse_xml(self.local_path)
        self.making_internal = self.tree.getroot().find("ors/FIXNotif/makingInternal")
        self.making_internal.text = 'false'
        self.tree.write("temp.xml")
        self.ssh_client.send_command('~/automation_scripts/change_permission_script')
        self.ssh_client.put_file(self.remote_path, "temp.xml")
        self.ssh_client.send_command("qrestart ORS")
        time.sleep(70)
        # endregion
        # region step 1
        self.new_order.set_default_SOR()
        cl_ord_id = self.fix_manager.send_message_and_receive_response(self.new_order)[-1].get_parameters()["ClOrdID"]
        # endregion
        self.result = self.ssh_client.find_regex_pattern("/Logs/quod314/QUOD.ORS.log",
                                                         rf"^.*{cl_ord_id}.*EV..................2.*$")
        if self.result:
            self.result = "failed"
        else:
            self.result = "pass"
        self.verifier.set_parent_id(self.test_id)
        self.verifier.set_event_name("Check that there is no internal execution in logs")
        self.verifier.compare_values("status", "pass", self.result)
        self.verifier.verify()

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.md_request.set_md_uns_parameters_maker()
        self.fix_manager_gtw.send_message(self.md_request)
        self.making_internal.text = 'true'
        self.tree.write("temp.xml")
        self.ssh_client.send_command('~/automation_scripts/change_permission_script')
        self.ssh_client.put_file(self.remote_path, "temp.xml")
        self.ssh_client.send_command("qrestart ORS")
        time.sleep(70)
