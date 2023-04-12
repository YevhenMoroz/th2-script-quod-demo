import logging
import os
import time
import xml.etree.ElementTree as ET
from pathlib import Path

from pkg_resources import resource_filename

from custom import basic_custom_actions as bca
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, OrderReplyConst
from test_framework.java_api_wrappers.oms.ors_messges.FixNewOrderSingleOMS import FixNewOrderSingleOMS
from test_framework.ssh_wrappers.ssh_client import SshClient

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def _get_fix_message(parameter: dict, response):
    for i in range(len(response)):
        for j in parameter.keys():
            print(response[i].get_parameters())
            if response[i].get_parameters()[j] == parameter[j]:
                return response[i].get_parameters()


class QAP_T6979(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.rule_manager = RuleManager(sim=Simulators.equity)
        self.venue_client_name = self.data_set.get_venue_client_names_by_name('client_pt_1_venue_1')
        self.mic = self.data_set.get_mic_by_name('mic_1')  # XPAR
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.fix_nos = FixMessageNewOrderSingleOMS(self.data_set)
        self.bs_connectivity = self.fix_env.buy_side
        self.java_api_connectivity = self.java_api = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.fix_new_ord_single = FixNewOrderSingleOMS(self.data_set)
        self.ssh_client_env = self.environment.get_list_ssh_client_environment()[0]
        self.ssh_client = SshClient(self.ssh_client_env.host, self.ssh_client_env.port, self.ssh_client_env.user,
                                    self.ssh_client_env.password, self.ssh_client_env.su_user,
                                    self.ssh_client_env.su_password)
        self.local_path = resource_filename("test_resources.be_configs.oms_be_configs", "client_ors.xml")
        self.remote_path = f"/home/{self.ssh_client_env.su_user}/quod/cfg/client_ors.xml"

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region precondition
        tree = ET.parse(self.local_path)
        dma = tree.getroot().find("ors/FrontToBack/acceptUnknownAccountGroup/DMA")
        dma.text = 'false'
        tree.write("temp.xml")
        self.ssh_client.send_command('~/quod/script/site_scripts/change_permission_script')
        self.ssh_client.put_file(self.remote_path, "temp.xml")
        self.ssh_client.send_command("qrestart ORS")
        time.sleep(50)
        # endregion

        # region step 1: Create DMA order without Account
        self.fix_nos.set_default_dma_limit()
        self.fix_nos.remove_parameter("Account")
        expected_values = {'ExecType': '8'}
        responses = self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_nos)
        response = _get_fix_message(expected_values, responses)

        self.fix_manager.compare_values({expected_values},
                                        responses, 'Verifying that order is reject (step 1)')
        # endregion

        # region step 2: Create DMA order with Account
        self.fix_new_ord_single.update_fields_in_component(JavaApiFields.NewOrderSingleBlock.value,
                                                           {JavaApiFields.ClientAccountGroupID.value: 'WRONG_CLIENT'})
        self.java_api_manager.send_message_and_receive_response(self.fix_new_ord_single)
        order_notification = \
        self.java_api_manager.get_last_message(ORSMessageType.OrdNotification.value).get_parameters()[
            JavaApiFields.OrdNotificationBlock.value]
        self.java_api_manager.compare_values({JavaApiFields.OrdStatus.value: OrderReplyConst.OrdStatus_REJ.value},
                                             order_notification,
                                             'Verifying that FIX Order with 1 tag rejected (step 2)')
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.ssh_client.put_file(self.remote_path, self.local_path)
        self.ssh_client.send_command("qrestart ORS")
        time.sleep(50)
        os.remove("temp.xml")
        self.ssh_client.close()
