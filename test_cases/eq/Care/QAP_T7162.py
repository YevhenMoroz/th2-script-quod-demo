import logging
import os
import time
import xml.etree.ElementTree as ET
from pathlib import Path

from pkg_resources import resource_filename

from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields
from test_framework.java_api_wrappers.oms.ors_messges.FixNewOrderSingleOMS import FixNewOrderSingleOMS
from test_framework.ssh_wrappers.ssh_client import SshClient

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP_T7162(TestCase):
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(os.path.basename(__file__)[:-3], self.report_id)
        self.java_api_connectivity = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.fix_env = environment.get_list_fix_environment()[0]
        self.venue_client_account_name = self.data_set.get_venue_client_account_name('venue_client_account_name')
        self.client = self.data_set.get_client_by_name('client_pt_1')
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.ssh_client_env = self.environment.get_list_ssh_client_environment()[0]
        self.ssh_client = SshClient(self.ssh_client_env.host, self.ssh_client_env.port, self.ssh_client_env.user,
                                    self.ssh_client_env.password, self.ssh_client_env.su_user,
                                    self.ssh_client_env.su_password)
        self.nos_request = FixNewOrderSingleOMS(self.data_set)
        self.local_path = resource_filename("test_resources.be_configs.oms_be_configs", "client_ors.xml")
        self.remote_path = f"/home/{self.ssh_client_env.su_user}/quod/cfg/client_ors.xml"
        self.fix_responses = None
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.expected_sec_account = self.data_set.get_account_by_name('client_pt_1_acc_1')

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region precondition
        tree = ET.parse(self.local_path)
        ors = tree.getroot().find("ors/FrontToBack/acceptMultipleVenueAccountGroups")
        ors.text = 'true'
        tree.write("temp.xml")
        self.ssh_client.send_command('~/quod/script/site_scripts/change_permission_script')
        self.ssh_client.put_file(self.remote_path, "temp.xml")
        self.ssh_client.send_command("qrestart ORS")
        time.sleep(80)
        # endregion

        # region step 1: send CO order
        self.nos_request.set_default_care_limit()
        self.nos_request.update_fields_in_component('NewOrderSingleBlock', {
            'ClientAccountGroupID': self.client,
            'PreTradeAllocationBlock': {'PreTradeAllocationList': {'PreTradeAllocAccountBlock': [
                {'AllocClientAccountID': self.venue_client_account_name, 'AllocQty': '100'}]}}})
        self.java_api_manager.send_message_and_receive_response(self.nos_request)
        order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value]
        print(order_reply)
        self.java_api_manager.compare_values({JavaApiFields.AllocAccountID.value: self.expected_sec_account},
                                             order_reply[JavaApiFields.PreTradeAllocationBlock.value][
                                                 JavaApiFields.PreTradeAllocationList.value][
                                                 JavaApiFields.PreTradeAllocAccountBlock.value][0],
                                             'Checking expected and actually result for step 1')
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.ssh_client.put_file(self.remote_path, self.local_path)
        self.ssh_client.send_command("qrestart ORS")
        time.sleep(80)
        os.remove("temp.xml")
        self.ssh_client.close()

    def __get_fix_message(self, parameter: dict):
        for i in range(len(self.fix_responses)):
            for j in parameter.keys():
                print(self.fix_responses[i].get_parameters()[j])
                if self.fix_responses[i].get_parameters()[j] == parameter[j]:
                    return self.fix_responses[i].get_parameters()
