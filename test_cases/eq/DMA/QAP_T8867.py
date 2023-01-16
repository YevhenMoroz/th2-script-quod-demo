import logging
import os
import time
from pathlib import Path
import xml.etree.ElementTree as ET

from pkg_resources import resource_filename

from custom import basic_custom_actions as bca
from custom.basic_custom_actions import timestamps
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.fix_wrappers.oms.FixMessageExecutionReportOMS import FixMessageExecutionReportOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields
from test_framework.java_api_wrappers.oms.es_messages.NewOrderReplyOMS import NewOrderReplyOMS
from test_framework.ssh_wrappers.ssh_client import SshClient

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

seconds, nanos = timestamps()  # Test case start time


class QAP_T8867(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        # region Declarations
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fe_env = self.environment.get_list_fe_environment()[0]
        self.qty = "100"
        self.price = "10"
        self.venue_client_names = self.data_set.get_venue_client_names_by_name("client_pt_1_venue_1")  # MOClient_PARIS
        self.venue = self.data_set.get_mic_by_name("mic_1")  # XPAR
        self.client = self.data_set.get_client("client_pt_1")  # MOClient
        self.alloc_account = self.data_set.get_account_by_name("client_pt_1_acc_1")  # MOClient_SA1
        self.exec_report = FixMessageExecutionReportOMS(self.data_set)
        self.java_api_connectivity = self.java_api = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.nos = NewOrderReplyOMS(self.data_set).set_unsolicited_dma_limit()
        self.user = self.fe_env.user_2
        self.ssh_client_env = self.environment.get_list_ssh_client_environment()[0]
        self.ssh_client = SshClient(self.ssh_client_env.host, self.ssh_client_env.port, self.ssh_client_env.user,
                                    self.ssh_client_env.password, self.ssh_client_env.su_user,
                                    self.ssh_client_env.su_password)
        self.local_path_es = resource_filename("test_resources.be_configs.oms_be_configs", "client_es.xml")
        self.remote_path_es = f"/home/{self.ssh_client_env.su_user}/quod/cfg/client_es.xml"
        self.local_path_ors = resource_filename("test_resources.be_configs.oms_be_configs", "client_ors.xml")
        self.remote_path_ors = f"/home/{self.ssh_client_env.su_user}/quod/cfg/client_ors.xml"
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region set up configuration on BackEnd(precondition)
        tree = ET.parse(self.local_path_es)
        quod = tree.getroot()
        quod.find("es/order/implicit/enabled").text = 'true'
        quod.find("es/order/implicit/originator").text = 'ORS'
        quod.find("es/order/implicit/user").text = self.user
        quod.find("es/order/implicit/role").text = 'HSD'
        tree.write("temp1.xml")
        self.ssh_client.send_command("~/quod/script/site_scripts/change_permission_script")
        self.ssh_client.put_file(self.remote_path_es, "temp1.xml")
        tree = ET.parse(self.local_path_ors)
        quod = tree.getroot()
        quod.find("ors/FrontToBack/orphanTradeUser").text = self.user
        quod.find("ors/FrontToBack/orphanTradeRole").text = 'HSD'
        tree.write("temp2.xml")
        self.ssh_client.send_command("~/quod/script/site_scripts/change_permission_script")
        self.ssh_client.put_file(self.remote_path_ors, "temp2.xml")
        self.ssh_client.send_command("qrestart ORS ESBUYTH2TEST")
        time.sleep(90)
        # endregion

        # region Create order
        self.nos.update_fields_in_component("NewOrderReplyBlock",
                                            {"VenueAccount": {"VenueActGrpName": self.venue_client_names}})
        self.java_api_manager.send_message_and_receive_response(self.nos)

        ord_rep = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value]
        self.java_api_manager.compare_values(
            {JavaApiFields.TransStatus.value: "OPN", JavaApiFields.UnsolicitedOrder.value: "Y"}, ord_rep,
            'Check order status')
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.ssh_client.put_file(self.remote_path_es, self.local_path_es)
        self.ssh_client.put_file(self.remote_path_ors, self.local_path_ors)
        self.ssh_client.send_command("qrestart ORS ESBUYTH2TEST")
        os.remove("temp1.xml")
        os.remove("temp2.xml")
