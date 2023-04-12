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
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, OrderReplyConst
from test_framework.java_api_wrappers.oms.ors_messges.FixNewOrderSingleOMS import FixNewOrderSingleOMS
from test_framework.ssh_wrappers.ssh_client import SshClient

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
seconds, nanos = timestamps()


class QAP_T7351(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.bs_connectivity = self.fix_env.buy_side
        self.rule_manager = RuleManager(sim=Simulators.equity)
        self.client = self.data_set.get_client('client_pt_1')
        self.venue_client_name = self.data_set.get_venue_client_names_by_name('client_pt_1_venue_1')
        self.mic = self.data_set.get_mic_by_name('mic_1')
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.venue_client_account_name = self.data_set.get_venue_client_account('client_pt_1_acc_1_venue_client_account')
        self.alloc_account = self.data_set.get_account_by_name('client_pt_1_acc_1')
        self.java_api_connectivity = self.java_api = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.new_order_single = FixNewOrderSingleOMS(self.data_set)
        self.ssh_client_env = self.environment.get_list_ssh_client_environment()[0]
        self.ssh_client = SshClient(self.ssh_client_env.host, self.ssh_client_env.port, self.ssh_client_env.user,
                                    self.ssh_client_env.password, self.ssh_client_env.su_user,
                                    self.ssh_client_env.su_password)
        self.db_manager = DBManager(environment.get_list_data_base_environment()[0])

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region precondition:
        self.db_manager.execute_query(f"""UPDATE  venue SET  valvenueclientaccountname  = 'Y'
                                            WHERE venueid = 'PARIS'""")
        self.ssh_client.send_command("qrestart all")
        time.sleep(200)
        # endregion

        # region step 1-2: Create DMA order with wrong NIN (VenueClientAccountGroupName (VenueClientAccountName))
        try:
            self.new_order_single.set_default_dma_limit()
            self.new_order_single.update_fields_in_component(JavaApiFields.NewOrderSingleBlock.value,
                                                             {JavaApiFields.ClientAccountGroupID.value: self.client,
                                                              'PreTradeAllocationBlock': {
                                                                  'PreTradeAllocationList': {'PreTradeAllocAccountBlock': [
                                                                      {
                                                                          'AllocClientAccountID': self.venue_client_account_name,
                                                                          'AllocQty': '100'}]}}
                                                              })
            price = self.new_order_single.get_parameters()[JavaApiFields.NewOrderSingleBlock.value][
                JavaApiFields.Price.value]
            new_order_single_rule = self.rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(
                self.bs_connectivity, self.venue_client_name, self.mic, float(price))
            self.java_api_manager.send_message_and_receive_response(self.new_order_single)
            ord_reply = \
                self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
                    JavaApiFields.OrdReplyBlock.value]
            self.java_api_manager.compare_values({JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_OPN.value},
                                                 ord_reply,
                                                 f'Verify that order created (step 2)')
            actually_alloc_account = ord_reply[JavaApiFields.PreTradeAllocationBlock.value][JavaApiFields.PreTradeAllocationList.value][JavaApiFields.PreTradeAllocAccountBlock][0][JavaApiFields.AllocAccountID.value]
            self.java_api_manager.compare_values({JavaApiFields.AllocAccountID.value: self.alloc_account},
                                                 {JavaApiFields.AllocAccountID.value: actually_alloc_account},
                                                 f'Verify that order has properly {JavaApiFields.AllocAccountID.value} (step 2)')
        finally:
            time.sleep(1)
            self.rule_manager.remove_rule(new_order_single_rule)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.db_manager.execute_query(f"""UPDATE  venue SET  valvenueclientaccountname  = 'N'
                                                    WHERE venueid = 'PARIS'""")
        self.ssh_client.send_command("qrestart all")
        time.sleep(200)
        self.db_manager.close_connection()
        self.ssh_client.close()
