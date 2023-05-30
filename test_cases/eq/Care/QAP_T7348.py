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
from test_framework.java_api_wrappers.ors_messages.HeldOrderAckRequest import HeldOrderAckRequest
from test_framework.ssh_wrappers.ssh_client import SshClient

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
seconds, nanos = timestamps()


class QAP_T7348(TestCase):
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
        self.venue_client_account_name = self.data_set.get_venue_client_account(
            'client_pt_1_acc_2_venue_client_account')
        self.java_api_connectivity = self.java_api = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.new_order_single = FixNewOrderSingleOMS(self.data_set)
        self.alloc_account = self.data_set.get_account_by_name('client_pt_1_acc_1')
        self.ssh_client_env = self.environment.get_list_ssh_client_environment()[0]
        self.ssh_client = SshClient(self.ssh_client_env.host, self.ssh_client_env.port, self.ssh_client_env.user,
                                    self.ssh_client_env.password, self.ssh_client_env.su_user,
                                    self.ssh_client_env.su_password)
        self.db_manager = DBManager(environment.get_list_data_base_environment()[0])
        self.group_modify = HeldOrderAckRequest()

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region precondition:
        self.db_manager.execute_query(f"""UPDATE  venue SET  valvenueclientaccountname  = 'Y'
                                            WHERE venueid = 'PARIS'""")
        self.ssh_client.send_command("qrestart QUOD.ORS QUOD.RDS QUOD.CS")
        time.sleep(100)
        # endregion

        # region step 1-2: Create CO order with wrong  NIN (VenueClientAccountGroupName (VenueClientAccountName))
        self.new_order_single.set_default_care_limit()
        self.new_order_single.update_fields_in_component(JavaApiFields.NewOrderSingleBlock.value,
                                                         {JavaApiFields.ClientAccountGroupID.value: self.client,
                                                          'PreTradeAllocationBlock': {
                                                              'PreTradeAllocationList': {'PreTradeAllocAccountBlock': [
                                                                  {
                                                                      'AllocClientAccountID': self.venue_client_account_name,
                                                                      'AllocQty': '100'}]}}
                                                          })
        self.java_api_manager.send_message_and_receive_response(self.new_order_single, response_time=30000)

        ord_notification = \
            self.java_api_manager.get_last_message(ORSMessageType.OrdNotification.value).get_parameters()[
                JavaApiFields.OrdNotificationBlock.value]
        order_id = ord_notification[JavaApiFields.OrdID.value]
        self.java_api_manager.compare_values({JavaApiFields.OrdStatus.value: OrderReplyConst.OrdStatus_HLD.value},
                                             ord_notification,
                                             f'Verify that order created (step 2)')
        # endregion

        # region step 3-4 :Group modify
        self.group_modify.set_default(order_id, self.client, self.alloc_account)
        self.java_api_manager.send_message_and_receive_response(self.group_modify)
        order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[JavaApiFields.OrdReplyBlock.value]
        self.java_api_manager.compare_values({JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_SEN.value},
                                             order_reply,
                                             f'Verifying that order has {OrderReplyConst.TransStatus_SEN.value} status (step 4)')
        actually_alloc_account = \
            order_reply[JavaApiFields.PreTradeAllocationBlock.value][JavaApiFields.PreTradeAllocationList.value][
                JavaApiFields.PreTradeAllocAccountBlock.value][0][JavaApiFields.AllocAccountID.value]
        self.java_api_manager.compare_values({JavaApiFields.AllocAccountID.value: self.alloc_account},
                                             {JavaApiFields.AllocAccountID.value: actually_alloc_account},
                                             f'Verify that order has properly {JavaApiFields.AllocAccountID.value} (step 4)')
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.db_manager.execute_query(f"""UPDATE  venue SET  valvenueclientaccountname  = 'N'
                                                    WHERE venueid = 'PARIS'""")
        self.ssh_client.send_command("qrestart QUOD.ORS QUOD.RDS QUOD.CS")
        time.sleep(100)
        self.db_manager.close_connection()
        self.ssh_client.close()