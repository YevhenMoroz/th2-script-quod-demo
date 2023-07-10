import logging
import time
from pathlib import Path
from custom import basic_custom_actions as bca
from custom.basic_custom_actions import timestamps
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.db_wrapper.db_manager import DBManager
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.oms.FixMessageExecutionReportOMS import FixMessageExecutionReportOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, OrderReplyConst
from test_framework.java_api_wrappers.oms.ors_messges.FixNewOrderSingleOMS import FixNewOrderSingleOMS
from test_framework.rest_api_wrappers.RestApiManager import RestApiManager
from test_framework.rest_api_wrappers.oms.RestAPIModifySecurityAccountMessage import RestAPIModifySecurityAccountMessage
from test_framework.ssh_wrappers.ssh_client import SshClient

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
seconds, nanos = timestamps()


class QAP_T6921(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.bs_connectivity = self.fix_env.buy_side
        self.rule_manager = RuleManager(sim=Simulators.equity)
        self.client = self.data_set.get_client('client_rest_api')
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.mic = self.data_set.get_mic_by_name('mic_1')
        self.alloc_account = self.data_set.get_account_by_name('client_rest_api_acc_2')
        self.rest_api_conn = environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.rest_api_manager = RestApiManager(self.rest_api_conn, self.test_id)
        self.venue_client_account_name = self.data_set.get_venue_client_account(
            'client_rest_api_acc_2_venue_client_account')
        self.java_api_connectivity = self.java_api = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.new_order_single = FixNewOrderSingleOMS(self.data_set)
        self.ssh_client_env = self.environment.get_list_ssh_client_environment()[0]
        self.ssh_client = SshClient(self.ssh_client_env.host, self.ssh_client_env.port, self.ssh_client_env.user,
                                    self.ssh_client_env.password, self.ssh_client_env.su_user,
                                    self.ssh_client_env.su_password)
        self.db_manager = DBManager(environment.get_list_data_base_environment()[0])
        self.rest_api_modify_sec_account = RestAPIModifySecurityAccountMessage(self.data_set)
        self.execution_report = FixMessageExecutionReportOMS(self.data_set)
        self.fix_verifier = FixVerifier(self.fix_env.sell_side, self.test_id)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region precondition:
        # part 1: Set needed configuration for venue
        self.db_manager.execute_query(f"""UPDATE  venue SET  valvenueclientaccountname  = 'Y'
                                            WHERE venueid = 'PARIS'""")
        self.ssh_client.send_command("qrestart QUOD.AQS QUOD.ORS QUOD.ESBUYTH2TEST QUOD.RDS")
        time.sleep(120)
        # end_of_part

        # part 2: Set needed configuration for SecurityAccount
        additional_parameters = {'venueSecActName': [{
            "venueAccountName": "CLIENT_REST_API_SA2",
            "venueAccountIDSource": "OTH",
            "venueID": "PARIS",
            "stampFeeExemption": 'false',
            "levyFeeExemption": 'false',
            "perTransacFeeExemption": 'false',
            "venueClientAccountName": self.venue_client_account_name}]}
        self.rest_api_modify_sec_account.set_default()
        self.rest_api_modify_sec_account.add_additional_parameters(additional_parameters)
        self.rest_api_manager.send_post_request(self.rest_api_modify_sec_account)
        # endregion

        # region step 1: Create DMA order with
        self.new_order_single.set_default_dma_limit()
        self.new_order_single.update_fields_in_component(JavaApiFields.NewOrderSingleBlock.value,
                                                         {JavaApiFields.ClientAccountGroupID.value: self.client,
                                                          JavaApiFields.PreTradeAllocationBlock.value: {
                                                              JavaApiFields.PreTradeAllocationList.value: {
                                                                  JavaApiFields.PreTradeAllocAccountBlock.value: [
                                                                      {
                                                                          JavaApiFields.AllocClientAccountID.value: self.venue_client_account_name,
                                                                          JavaApiFields.AllocQty.value: '100'}]}}
                                                          })
        price = self.new_order_single.get_parameters()[JavaApiFields.NewOrderSingleBlock.value][
            JavaApiFields.Price.value]
        self._send_new_order_single(price)
        ord_reply = \
            self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
                JavaApiFields.OrdReplyBlock.value]
        self.java_api_manager.compare_values({JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_OPN.value},
                                             ord_reply,
                                             f'Verify that order created (step 2)')
        actually_alloc_account = \
            ord_reply[JavaApiFields.PreTradeAllocationBlock.value][JavaApiFields.PreTradeAllocationList.value][
                JavaApiFields.PreTradeAllocAccountBlock.value][0][JavaApiFields.AllocAccountID.value]
        self.java_api_manager.compare_values({JavaApiFields.AllocAccountID.value: self.alloc_account},
                                             {JavaApiFields.AllocAccountID.value: actually_alloc_account},
                                             f'Verify that order has properly {JavaApiFields.AllocAccountID.value} (step 2)')
        # endregion

        # region step 2: Amend venueClientAccountName via WebAdmin
        additional_parameters['venueSecActName'][0]['venueClientAccountName'] = 'something'
        self.rest_api_manager.send_post_request(self.rest_api_modify_sec_account)
        # endregion

        # region step 3: Send new OrderSingle again
        cl_ord_id = bca.client_orderid(8)
        self.new_order_single.update_fields_in_component(JavaApiFields.NewOrderSingleBlock.value,
                                                         {
                                                             JavaApiFields.ClOrdID.value: cl_ord_id
                                                         })
        self._send_new_order_single(price)
        self.execution_report.change_parameters({"ExecType": "8", "OrdStatus": "8", 'ClOrdID': cl_ord_id})
        self.fix_verifier.check_fix_message_fix_standard(self.execution_report)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.rest_api_modify_sec_account.get_parameters().clear()
        self.rest_api_modify_sec_account.set_default()
        self.rest_api_manager.send_post_request(self.rest_api_modify_sec_account)
        self.db_manager.execute_query(f"""UPDATE venue SET  valvenueclientaccountname  = 'N'
                                                    WHERE venueid = 'PARIS'""")
        self.ssh_client.send_command("qrestart QUOD.AQS QUOD.ORS QUOD.ESBUYTH2TEST QUOD.RDS")
        time.sleep(120)
        self.db_manager.close_connection()
        self.ssh_client.close()

    def _send_new_order_single(self, price):
        try:
            new_order_single_rule = self.rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(
                self.bs_connectivity, self.client, self.mic, float(price))
            self.java_api_manager.send_message(self.new_order_single)
        except Exception as e:
            logger.error(f'{e}', exc_info=True)
        finally:
            time.sleep(1)
            self.rule_manager.remove_rule(new_order_single_rule)
