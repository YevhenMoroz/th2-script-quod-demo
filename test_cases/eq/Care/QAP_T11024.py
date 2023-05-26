import logging
from pathlib import Path
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from custom import basic_custom_actions as bca, basic_custom_actions
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.fix_wrappers.FixManager import FixManager
from rule_management import RuleManager, Simulators
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, OrderReplyConst
from test_framework.java_api_wrappers.ors_messages.MassCancelOrderRequest import OrderMassCancelRequest
from test_framework.java_api_wrappers.ors_messages.SuspendOrderManagementRequest import SuspendOrderManagementRequest

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP_T11024(TestCase):
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
        self.mass_cancel_request = OrderMassCancelRequest()

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region create CO orders (step 1)
        #  the cs.xml by default has <assignFEModifyCancelToDesk>false</assignFEModifyCancelToDesk>
        response1 = self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message)
        order_id1 = response1[0].get_parameters()['OrderID']

        self.fix_message.change_parameters({'ClOrdID': basic_custom_actions.client_orderid(9)})
        response2 = self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message)
        order_id2 = response2[0].get_parameters()['OrderID']
        # endregion

        # region cancel oreder (step 2)
        self.mass_cancel_request.set_default([order_id1, order_id2])
        self.java_api_manager.send_message_and_receive_response(self.mass_cancel_request, filter_dict=
        {'OrdID1': order_id1, 'OrdID2': order_id2})
        # endregion

        # region check order after cancellation (step 2)
        ord_reply1 = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value, order_id1).get_parameter(
            JavaApiFields.OrdReplyBlock.value)
        self.java_api_manager.compare_values({JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_CXL.value,
                                              JavaApiFields.OrdID.value: order_id1},
                                             ord_reply1,
                                             "Check first order after cancellation")

        ord_reply2 = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value, order_id2).get_parameter(
            JavaApiFields.OrdReplyBlock.value)
        self.java_api_manager.compare_values({JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_CXL.value,
                                              JavaApiFields.OrdID.value: order_id2},
                                             ord_reply2,
                                             "Check second order after cancellation")
        # endregion
