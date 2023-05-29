import logging
from pathlib import Path
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from custom import basic_custom_actions as bca
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.fix_wrappers.FixManager import FixManager
from rule_management import RuleManager, Simulators
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, OrderReplyConst
from test_framework.java_api_wrappers.ors_messages.CancelOrderRequest import CancelOrderRequest
from test_framework.java_api_wrappers.ors_messages.SuspendOrderManagementRequest import SuspendOrderManagementRequest

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP_T7287(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.java_api_connectivity = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.qty = "1000"
        self.price = "500"
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set).set_default_care_limit()
        self.fix_message.change_parameters({'OrderQtyData': {'OrderQty': self.qty}, "Price": self.price})
        self.rule_manager = RuleManager(Simulators.equity)
        self.suspend_order = SuspendOrderManagementRequest()
        self.cancel_request = CancelOrderRequest()

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region create CO order (precondition)
        response = self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message)
        order_id = response[0].get_parameters()['OrderID']
        cl_order_id = response[0].get_parameters()['ClOrdID']
        # endregion

        # region suspend order
        self.suspend_order.set_default(order_id)
        self.java_api_manager.send_message_and_receive_response(self.suspend_order)
        suspend_reply = \
            self.java_api_manager.get_last_message(
                ORSMessageType.SuspendOrderManagementReply.value).get_parameters()[
                JavaApiFields.SuspendOrderManagementReplyBlock.value]
        self.java_api_manager.compare_values({JavaApiFields.SuspendedCare.value: 'Y',
                                              JavaApiFields.OrdID.value: order_id},
                                             suspend_reply,
                                             f'Checking that order has {JavaApiFields.SuspendedCare.value} = "Y" (step 1)')
        # endregion

        # region cancel oreder
        self.cancel_request.set_default(order_id)
        self.java_api_manager.send_message_and_receive_response(self.cancel_request)
        # endregion

        # region check order after cancellation
        ord_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameter(
            JavaApiFields.OrdReplyBlock.value)
        self.java_api_manager.compare_values({JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_CXL.value},
                                             ord_reply,
                                             "Check order after cancellation")
        # endregion
