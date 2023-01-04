import logging
from pathlib import Path
from custom import basic_custom_actions as bca
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, OrderReplyConst, ExecutionReportConst
from test_framework.java_api_wrappers.oms.ors_messges.TradeEntryOMS import TradeEntryOMS
from test_framework.java_api_wrappers.ors_messages.CheckOutOrderRequest import CheckOutOrderRequest

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP_T7519(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.java_api_connectivity = self.java_api = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.fix_verifier = FixVerifier(self.fix_env.sell_side, self.test_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set).set_default_care_limit()
        self.qty = self.fix_message.get_parameter('OrderQtyData')['OrderQty']
        self.price = self.fix_message.get_parameter('Price')
        self.rule_manager = RuleManager(sim=Simulators.equity)
        self.check_out = CheckOutOrderRequest()
        self.trade_request = TradeEntryOMS(self.data_set)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region create CO order
        response = self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message)
        order_id = response[0].get_parameters()['OrderID']
        # endregion

        # region check out order
        self.check_out.set_default(order_id)
        responses = self.java_api_manager.send_message_and_receive_response(self.check_out)
        self.return_result(responses, ORSMessageType.OrdNotification.value)
        notify_block = self.result.get_parameter('OrdNotificationBlock')
        self.java_api_manager.compare_values({JavaApiFields.IsLocked.value: OrderReplyConst.IsLocked_Y.value},
                                             notify_block, "Check order values after check out")
        # endregion

        # region manual exec order
        self.trade_request.set_default_trade(order_id, self.price, self.qty)
        responses = self.java_api_manager.send_message_and_receive_response(self.trade_request)
        self.return_result(responses, ORSMessageType.OrdNotification.value)
        notify_block = self.result.get_parameter('OrdNotificationBlock')
        self.java_api_manager.compare_values({JavaApiFields.IsLocked.value: OrderReplyConst.IsLocked_Y.value},
                                             notify_block, "Check IsLocked value after order Execution")
        self.return_result(responses, ORSMessageType.ExecutionReport.value)
        notify_block = self.result.get_parameter('ExecutionReportBlock')
        self.java_api_manager.compare_values(
            {JavaApiFields.TransExecStatus.value: ExecutionReportConst.TransExecStatus_FIL.value},
            notify_block, "Check order is executed")
        # endregion

    def return_result(self, responses, message_type):
        for response in responses:
            if response.get_message_type() == message_type:
                self.result = response
