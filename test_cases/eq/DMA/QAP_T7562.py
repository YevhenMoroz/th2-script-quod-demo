import logging
import time
from pathlib import Path
from custom import basic_custom_actions as bca
from custom.basic_custom_actions import timestamps
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.oms.FixMessageExecutionReportOMS import FixMessageExecutionReportOMS
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, OrderReplyConst
from test_framework.java_api_wrappers.ors_messages.OrderModificationRequest import OrderModificationRequest

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

seconds, nanos = timestamps()


class QAP_T7562(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.java_api_connectivity = self.java_api = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.ss_connectivity = self.fix_env.sell_side
        self.bs_connectivity = self.fix_env.buy_side
        self.rule_manager = RuleManager(sim=Simulators.equity)
        self.venue = self.data_set.get_mic_by_name('mic_1')  # XPAR
        self.client = self.data_set.get_client('client_pos_3')  # SBK
        self.client_acc = self.data_set.get_account_by_name('client_pos_3_acc_1')
        self.venue_client_names = self.data_set.get_venue_client_names_by_name('client_pos_3_venue_1')  # SBK_PARIS
        self.fix_manager = FixManager(self.ss_connectivity, self.test_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set).set_default_dma_limit()
        self.fix_message.remove_parameter('OrderCapacity')
        self.qty = self.fix_message.get_parameter('OrderQtyData')['OrderQty']
        self.price = self.fix_message.get_parameter('Price')
        self.fix_message.change_parameters(
            {'Account': self.client, 'PreAllocGrp': {'NoAllocs': [{'AllocAccount': self.client_acc,
                                                                   'AllocQty': self.qty}]}})
        self.fix_verifier = FixVerifier(self.ss_connectivity, self.test_id)
        self.exec_report = FixMessageExecutionReportOMS(self.data_set)
        self.order_modification_request = OrderModificationRequest()
        # endregion

    @ try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        nos_rule = None
        cancel_replace_rule = None
        try:
            nos_rule = self.rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(self.bs_connectivity,
                                                                                                  self.venue_client_names,
                                                                                                  self.venue,
                                                                                                  float(self.price))

            response = self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message)
            order_id = response[0].get_parameters()['OrderID']
            # endregion

            # region check OrderCapacity in the exec report
            ignored_list = ['ReplyReceivedTime', 'SettlCurrency', 'LastMkt', 'Text', 'SecurityDesc', 'SecondaryOrderID']
            self.exec_report.set_default_new(self.fix_message)
            self.exec_report.change_parameters({'OrderCapacity': 'P', 'Account': self.client})
            self.fix_verifier.check_fix_message_fix_standard(self.exec_report, ignored_fields=ignored_list)
            # endregion

            # region modify order
            cancel_replace_rule \
                = self.rule_manager.add_OrderCancelReplaceRequest_FIXStandard(self.fix_env.buy_side,
                                                                              self.venue_client_names,
                                                                              self.venue)
            self.order_modification_request.set_default(self.data_set, order_id)
            self.order_modification_request.update_fields_in_component('OrderModificationRequestBlock',
                                                                       {'OrdCapacity': 'I',
                                                                        'ExecutionPolicy': 'D',
                                                                        'AccountGroupID': self.client})
            responses = self.java_api_manager.send_message_and_receive_response(self.order_modification_request)
            self.__return_result(responses, ORSMessageType.OrderReply.value)
            order_reply_block = self.result.get_parameter('OrdReplyBlock')
            self.java_api_manager.compare_values({JavaApiFields.OrdCapacity.value: OrderReplyConst.OrdCapacity_I.value},
                                                 order_reply_block,
                                                 'Check Capacity after Amending')
        finally:
            time.sleep(1)
            self.rule_manager.remove_rule(nos_rule)
            self.rule_manager.remove_rule(cancel_replace_rule)

    def __return_result(self, responses, message_type):
        for response in responses:
            if response.get_message_type() == message_type:
                self.result = response
