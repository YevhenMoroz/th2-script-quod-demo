import logging
import time
from pathlib import Path

from custom import basic_custom_actions as bca
from custom.basic_custom_actions import timestamps
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.java_api_wrappers.ors_messages.OrderModificationRequest import OrderModificationRequest

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

seconds, nanos = timestamps()  # Test case start time


class QAP_T7387(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.java_api_connectivity = self.java_api = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.bs_connectivity = self.fix_env.buy_side
        self.client = self.data_set.get_client_by_name('client_pt_1')
        self.account = self.data_set.get_account_by_name('client_pt_1_acc_1')  # MOClient_SA1
        self.washbook = self.data_set.get_washbook_account_by_name('washbook_account_5')  # EquityWashBook
        self.new_account = self.data_set.get_account_by_name('client_pt_1_acc_2')  # MOClient_SA2
        self.new_washbook = self.data_set.get_washbook_account_by_name('washbook_account_3')  # DefaultWashBook
        self.order_submit = OrderSubmitOMS(self.data_set)
        self.venue_client_names = self.data_set.get_venue_client_names_by_name("client_pt_1_venue_1")
        self.venue = self.data_set.get_mic_by_name("mic_1")
        self.order_modification_request = OrderModificationRequest()
        self.rule_manager = RuleManager(sim=Simulators.equity)
        self.price = '20'
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Create DMA order
        cancel_replace_rule = None
        nos_rule = None
        try:
            nos_rule = self.rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(self.bs_connectivity,
                                                                                                  self.venue_client_names,
                                                                                                  self.venue,
                                                                                                  float(self.price))
            self.order_submit.set_default_dma_limit()
            self.order_submit.update_fields_in_component('NewOrderSingleBlock', {
                'PreTradeAllocationBlock': {'PreTradeAllocationList': {
                    "PreTradeAllocAccountBlock": [{'AllocAccountID': self.account, 'AllocQty': '100'}]}},
                'WashBookAccountID': self.washbook, 'AccountGroupID': self.client, 'Price': self.price})
            responses = self.java_api_manager.send_message_and_receive_response(self.order_submit)
            self.__return_result(responses, ORSMessageType.OrdNotification.value)
            order_notify_block = self.result.get_parameter('OrdNotificationBlock')
            self.java_api_manager.compare_values({JavaApiFields.WashBookAccountID.value: self.washbook,
                                                  JavaApiFields.SingleAllocAccountID.value: self.account},
                                                 order_notify_block, 'Check WashBookAccount and AllocAccount')
            order_id = order_notify_block['OrdID']
            # endregion

            # region modify order
            cancel_replace_rule \
                = self.rule_manager.add_OrderCancelReplaceRequest_FIXStandard(self.fix_env.buy_side,
                                                                              self.venue_client_names,
                                                                              self.venue)
            self.order_modification_request.set_default(self.data_set, order_id)
            self.order_modification_request.update_fields_in_component('OrderModificationRequestBlock', {
                'PreTradeAllocationBlock': {'PreTradeAllocationList': {
                    "PreTradeAllocAccountBlock": [
                        {'AllocAccountID': self.new_account, 'AllocQty': '100'}]}},
                'WashBookAccountID': self.new_washbook, 'ExecutionPolicy': 'D', 'AccountGroupID': self.client})
            responses = self.java_api_manager.send_message_and_receive_response(self.order_modification_request)
            self.__return_result(responses, ORSMessageType.OrderReply.value)
            order_reply_block = self.result.get_parameter('OrdReplyBlock')
            self.java_api_manager.compare_values({JavaApiFields.WashBookAccountID.value: self.new_washbook,
                                                  JavaApiFields.SingleAllocAccountID.value: self.new_account},
                                                 order_reply_block,
                                                 'Check WashBookAccount and AllocAccount after Amending')
        finally:
            time.sleep(1)
            self.rule_manager.remove_rule(nos_rule)
            self.rule_manager.remove_rule(cancel_replace_rule)
        # endregion

    def __return_result(self, responses, message_type):
        for response in responses:
            if response.get_message_type() == message_type:
                self.result = response
