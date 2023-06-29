import logging
import os
import time
from pathlib import Path

from pkg_resources import resource_filename

from custom import basic_custom_actions as bca
from custom.basic_custom_actions import timestamps
from rule_management import RuleManager, Simulators
import xml.etree.ElementTree as ET
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, OrderReplyConst
from test_framework.java_api_wrappers.oms.ors_messges.FixNewOrderSingleOMS import FixNewOrderSingleOMS
from test_framework.rest_api_wrappers.RestApiManager import RestApiManager
from test_framework.rest_api_wrappers.oms.RestAPIModifySecurityAccountMessage import RestAPIModifySecurityAccountMessage
from test_framework.rest_api_wrappers.oms.RestApiModifyAccoutGroupMessage import RestApiModifyAccountGroupMessage
from test_framework.ssh_wrappers.ssh_client import SshClient

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

seconds, nanos = timestamps()  # Test case start time


class QAP_T11192(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.java_api_connectivity = self.java_api = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.new_order_single = FixNewOrderSingleOMS(self.data_set)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.rest_api_connectivity = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.rest_api_manager = RestApiManager(session_alias=self.rest_api_connectivity, case_id=self.test_id)
        self.rest_api_security_account = RestAPIModifySecurityAccountMessage(self.data_set)
        self.rest_api_client = RestApiModifyAccountGroupMessage(self.data_set, self.environment)
        self.venue = self.data_set.get_mic_by_name('mic_1')
        self.rule_manager = RuleManager(Simulators.equity)
        self.ssh_client_env = self.environment.get_list_ssh_client_environment()[0]
        self.ssh_client = SshClient(self.ssh_client_env.host, self.ssh_client_env.port, self.ssh_client_env.user,
                                    self.ssh_client_env.password, self.ssh_client_env.su_user,
                                    self.ssh_client_env.su_password)
        self.local_path = resource_filename("test_resources.be_configs.oms_be_configs", "client_ors.xml")
        self.remote_path = f"/home/{self.ssh_client_env.su_user}/quod/cfg/client_ors.xml"
        self.client = self.data_set.get_client_by_name('client_rest_api')
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region precondition: set up needed configuration for listing
        self.rest_api_client.set_default()
        client_account_id = self.client + '_EXT'
        account = self.data_set.get_account_by_name('client_rest_api_acc_2')
        self.rest_api_client.change_params({'clientAccountGroupID': client_account_id,
                                            'giveUpMatchingID': client_account_id})
        self.rest_api_manager.send_post_request(self.rest_api_client)
        self.rest_api_security_account.set_default()
        self.rest_api_security_account.change_params({'clientAccountID': client_account_id})
        self.rest_api_manager.send_post_request(self.rest_api_security_account)
        time.sleep(3)
        self.rest_api_security_account.change_params({
            'clientAccountID': client_account_id,
            "accountGroupID": self.data_set.get_client_by_name('client_pt_1'),
            "accountID": self.data_set.get_account_by_name('client_rest_api_acc_3'),
            "clientMatchingID": self.data_set.get_account_by_name('client_rest_api_acc_3'),
        })
        time.sleep(3)
        self.rest_api_manager.send_post_request(self.rest_api_security_account)
        tree = ET.parse(self.local_path)
        element = ET.fromstring("<clientAccountGroupConversion>true</clientAccountGroupConversion>")
        quod = tree.getroot().find("ors/FrontToBack")
        quod.append(element)
        tree.write("temp.xml")
        self.ssh_client.send_command("~/quod/script/site_scripts/change_permission_script")
        self.ssh_client.put_file(self.remote_path, "temp.xml")
        self.ssh_client.send_command("qrestart ORS")
        time.sleep(40)
        # endregion

        # region step 1: Create DMA order via FIX
        self.new_order_single.set_default_dma_limit()
        qty = self.new_order_single.get_parameters()[JavaApiFields.NewOrderSingleBlock.value][
            JavaApiFields.OrdQty.value]
        self.new_order_single.update_fields_in_component(JavaApiFields.NewOrderSingleBlock.value, {
            JavaApiFields.ClientAccountGroupID.value: client_account_id,
            JavaApiFields.PreTradeAllocationBlock.value: {
                JavaApiFields.PreTradeAllocationList.value: {JavaApiFields.PreTradeAllocAccountBlock.value: [
                    {
                        JavaApiFields.AllocClientAccountID.value: client_account_id,
                        JavaApiFields.AllocQty.value: qty}]}}
        })
        price = self.new_order_single.get_parameters()[JavaApiFields.NewOrderSingleBlock.value][
            JavaApiFields.Price.value]
        try:
            nos_rule = self.rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(self.fix_env.buy_side,
                                                                                                  self.client, self.venue,
                                                                                                  float(price))
            self.java_api_manager.send_message_and_receive_response(self.new_order_single)
        except Exception as e:
            logger.error(f'Exception {e}', exc_info=True)
        finally:
            self.rule_manager.remove_rule(nos_rule)

        ord_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value]
        self.java_api_manager.compare_values({JavaApiFields.AccountGroupID.value: self.client,
                                              JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_OPN.value},
                                             ord_reply, 'Verify that order has properly status and client (step 1)')
        self.java_api_manager.compare_values({JavaApiFields.AllocAccountID.value: account},
                                             ord_reply[JavaApiFields.PreTradeAllocationBlock.value][
                                                 JavaApiFields.PreTradeAllocationList.value][
                                                 JavaApiFields.PreTradeAllocAccountBlock.value][0],
                                             'Verify that order has properly security account (step 1)')

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.rest_api_security_account.set_default()
        self.rest_api_manager.send_post_request(self.rest_api_security_account)
        self.rest_api_security_account.change_params({
            'clientAccountID': self.data_set.get_account_by_name('client_rest_api_acc_3'),
            "accountGroupID": self.client,
            "accountID": self.data_set.get_account_by_name('client_rest_api_acc_3'),
            "clientMatchingID": self.data_set.get_account_by_name('client_rest_api_acc_3'),
        })
        self.rest_api_manager.send_post_request(self.rest_api_security_account)
        self.rest_api_client.set_default()
        self.rest_api_manager.send_post_request(self.rest_api_client)
        self.ssh_client.put_file(self.remote_path, self.local_path)
        self.ssh_client.send_command("qrestart ORS")
        time.sleep(40)
        os.remove("temp.xml")
