import logging
import os
import time
from pathlib import Path

from pkg_resources import resource_filename
import xml.etree.ElementTree as ET
from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, OrderReplyConst
from test_framework.java_api_wrappers.oms.es_messages.NewOrderReplyOMS import NewOrderReplyOMS
from test_framework.rest_api_wrappers.RestApiManager import RestApiManager
from test_framework.rest_api_wrappers.oms.RestApiWashBookRuleMessages import RestApiWashBookRuleMessages
from test_framework.ssh_wrappers.ssh_client import SshClient

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


@try_except(test_id=Path(__file__).name[:-3])
class QAP_T9033(TestCase):
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.ja_manager = JavaApiManager(environment.get_list_java_api_environment()[0].java_api_conn_user2, self.test_id)
        self.venue_acc_grp_name = self.data_set.get_venue_client_names_by_name("client_pt_1_venue_1")
        self.client = self.data_set.get_client_by_name('client_pt_1')
        self.washbook_acc = self.data_set.get_washbook_account_by_name('washbook_account_5')
        self.recipient = self.data_set.get_recipient_by_name("recipient_user_1")
        self.nos = NewOrderReplyOMS(self.data_set).set_unsolicited_dma_limit()
        self.rest_api_connectivity = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.rest_api_manager = RestApiManager(session_alias=self.rest_api_connectivity, case_id=self.test_id)
        self.mod_washbook = RestApiWashBookRuleMessages(self.data_set)
        self.venue_list_id = self.data_set.get_venue_list('venue_list_1')
        self.ssh_client_env = self.environment.get_list_ssh_client_environment()[0]
        self.ssh_client = SshClient(self.ssh_client_env.host, self.ssh_client_env.port, self.ssh_client_env.user,
                                    self.ssh_client_env.password, self.ssh_client_env.su_user,
                                    self.ssh_client_env.su_password)
        self.local_path = resource_filename("test_resources.be_configs.oms_be_configs", "client_es.xml")
        self.remote_path = f"/home/{self.ssh_client_env.su_user}/quod/cfg/client_es.xml"
        self.local_path_2 = resource_filename("test_resources.be_configs.oms_be_configs", "client_ors.xml")
        self.remote_path_2 = f"/home/{self.ssh_client_env.su_user}/quod/cfg/client_ors.xml"

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region precondition: Set WashBook rule:
        # part 1:
        desk = self.environment.get_list_fe_environment()[0].desk_ids[0]
        self.mod_washbook.modify_wash_book_rule(client=self.client, desk=desk, exec_policy='D',
                                                venue_list_id=self.venue_list_id)
        self.rest_api_manager.send_post_request(self.mod_washbook)
        time.sleep(3)
        # end_of_part

        # part 2: Set up needed configuration
        java_api_user_2 = self.environment.get_list_fe_environment()[0].user_2
        tree = ET.parse(self.local_path)
        quod = tree.getroot()
        quod.find("es/order/implicit/user").text = f'{java_api_user_2}'
        tree.write("temp.xml")
        tree_2 = ET.parse(self.local_path_2)
        quod_2 = tree_2.getroot()
        quod_2.find('ors/FrontToBack/orphanTradeUser').text = f'{java_api_user_2}'
        quod_2.find('ors/FrontToBack/orphanTradeRole').text = 'HSD'
        tree_2.write('temp_2.xml')
        self.ssh_client.send_command("~/quod/script/site_scripts/change_permission_script")
        self.ssh_client.put_file(self.remote_path_2, 'temp_2.xml')
        self.ssh_client.put_file(self.remote_path, "temp.xml")
        self.ssh_client.send_command("qrestart QUOD.ESBUYTH2TEST, QUOD.ORS")
        time.sleep(100)
        # end_of_part

        # endregion

        # region step 1: Create Unsolicity order:
        self.nos.set_unsolicited_dma_limit()
        self.nos.update_fields_in_component(JavaApiFields.NewOrderReplyBlock.value,
                                            {JavaApiFields.VenueAccount.value: {JavaApiFields.VenueActGrpName.value:
                                                                                    self.venue_acc_grp_name}})
        self.ja_manager.send_message_and_receive_response(self.nos)
        ord_rep = self.ja_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value]
        self.ja_manager.compare_values({JavaApiFields.WashBookAccountID.value: self.washbook_acc,
                                        JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_OPN.value,
                                        JavaApiFields.UnsolicitedOrder.value: 'Y'},
                                       ord_rep, 'Verify that order created and has properly values (step 1)')
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.mod_washbook.clear_washbook_rule()
        self.rest_api_manager.send_post_request(self.mod_washbook)
        self.ssh_client.put_file(self.remote_path, self.local_path)
        self.ssh_client.put_file(self.remote_path_2, self.local_path_2)
        self.ssh_client.send_command("qrestart QUOD.ESBUYTH2TEST QUOD.ORS")
        time.sleep(100)
        os.remove("temp.xml")
        os.remove("temp_2.xml")
        self.ssh_client.close()
