import logging
import os
from pathlib import Path

from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import SubmitRequestConst, JavaApiFields, ExecutionReportConst, \
    BasketMessagesConst
from test_framework.java_api_wrappers.oms.ors_messges.NewOrderListOMS import NewOrderListOMS
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.java_api_wrappers.oms.ors_messges.TradeEntryOMS import TradeEntryOMS
from test_framework.java_api_wrappers.ors_messages.AddOrdersToOrderListRequest import AddOrdersToOrderListRequest

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP_T7406(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(os.path.basename(__file__)[:-3], self.report_id)
        self.java_api_connectivity = self.java_api = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.fix_env = environment.get_list_fix_environment()[0]
        self.fe_env = environment.get_list_fe_environment()[0]
        self.user1 = self.fe_env.user_1
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.order_submit = OrderSubmitOMS(self.data_set)
        self.trade_request = TradeEntryOMS(self.data_set)
        self.list_creation_request = NewOrderListOMS(self.data_set)
        self.add_order_to_basket_request = AddOrdersToOrderListRequest()

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region create basket
        self.list_creation_request.set_default_order_list()
        responses = self.java_api_manager.send_message_and_receive_response(self.list_creation_request)
        self.return_result(responses, ORSMessageType.OrdListNotification.value)
        list_notify_block = self.result.get_parameter('OrdListNotificationBlock')
        self.java_api_manager.compare_values(
            {JavaApiFields.ListOrderStatus.value: BasketMessagesConst.ListOrderStatus_EXE.value}, list_notify_block,
            'Check created basket')
        list_id = list_notify_block['OrderListID']
        # endregion

        # region create order
        self.order_submit.set_default_care_limit(recipient=self.environment.get_list_fe_environment()[0].user_1,
                                                 desk=self.environment.get_list_fe_environment()[0].desk_ids[0],
                                                 role=SubmitRequestConst.USER_ROLE_1.value)
        responses = self.java_api_manager.send_message_and_receive_response(self.order_submit)
        self.return_result(responses, ORSMessageType.OrdReply.value)
        order_id = self.result.get_parameter('OrdReplyBlock')['OrdID']
        # endregion

        # region ManualExecute
        self.trade_request.set_default_trade(order_id)
        responses = self.java_api_manager.send_message_and_receive_response(self.trade_request)
        self.return_result(responses, ORSMessageType.ExecutionReport.value)
        exec_report = self.result.get_parameter('ExecutionReportBlock')
        self.java_api_manager.compare_values(
            {JavaApiFields.TransExecStatus.value: ExecutionReportConst.TransExecStatus_FIL.value},
            exec_report, 'Check exec order')
        # endregion

        # region Verify context menu
        self.add_order_to_basket_request.set_default(order_id, list_id)
        responses = self.java_api_manager.send_message_and_receive_response(self.add_order_to_basket_request)
        self.return_result(responses, ORSMessageType.AddOrdersToOrderListReply.value)
        message_reply = self.result.get_parameter('MessageReply')['MessageReplyBlock'][0]
        self.java_api_manager.compare_values({'ErrorMsg': f'Runtime error (order {order_id} is Filled)'},
                                             message_reply, 'Check Error')
        # endregion

    def return_result(self, responses, message_type):
        for response in responses:
            if response.get_message_type() == message_type:
                self.result = response
