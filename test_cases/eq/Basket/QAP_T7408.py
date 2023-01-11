import logging
from pathlib import Path
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from custom import basic_custom_actions as bca
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import BasketMessagesConst, JavaApiFields, SubmitRequestConst, \
    ExecutionReportConst, OrderReplyConst
from test_framework.java_api_wrappers.oms.ors_messges.AllocationInstructionOMS import AllocationInstructionOMS
from test_framework.java_api_wrappers.oms.ors_messges.DFDManagementBatchOMS import DFDManagementBatchOMS
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.java_api_wrappers.oms.ors_messges.TradeEntryOMS import TradeEntryOMS
from test_framework.java_api_wrappers.ors_messages.NewOrderListFromExistingOrders import NewOrderListFromExistingOrders

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


@try_except(test_id=Path(__file__).name[:-3])
class QAP_T7408(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.java_api_connectivity = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.trade_request = TradeEntryOMS(self.data_set)
        self.dfd_manage_batch = DFDManagementBatchOMS(self.data_set)
        self.alloc_instr_request = AllocationInstructionOMS(self.data_set)
        self.create_basket_request = NewOrderListFromExistingOrders()

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declaration
        order_submit = OrderSubmitOMS(self.data_set)
        order_submit.set_default_care_limit(recipient=self.environment.get_list_fe_environment()[0].user_1,
                                                 desk=self.environment.get_list_fe_environment()[0].desk_ids[0],
                                                 role=SubmitRequestConst.USER_ROLE_1.value)
        responses = self.java_api_manager.send_message_and_receive_response(order_submit)
        self.return_result(responses, ORSMessageType.OrdReply.value)
        order_id1 = self.result.get_parameter('OrdReplyBlock')['OrdID']
        # endregion

        # region ReOrder
        order_submit = OrderSubmitOMS(self.data_set)
        order_submit.set_default_care_limit(recipient=self.environment.get_list_fe_environment()[0].user_1,
                                                 desk=self.environment.get_list_fe_environment()[0].desk_ids[0],
                                                 role=SubmitRequestConst.USER_ROLE_1.value)
        responses = self.java_api_manager.send_message_and_receive_response(order_submit)
        self.return_result(responses, ORSMessageType.OrdReply.value)
        order_id2 = self.result.get_parameter('OrdReplyBlock')['OrdID']
        # endregion

        # region create basket
        self.create_basket_request.set_default([order_id1, order_id2])
        responses = self.java_api_manager.send_message_and_receive_response(self.create_basket_request)
        self.return_result(responses, ORSMessageType.OrdListNotification.value)
        list_notify_block = self.result.get_parameter('OrdListNotificationBlock')
        self.java_api_manager.compare_values(
            {JavaApiFields.ListOrderStatus.value: BasketMessagesConst.ListOrderStatus_EXE.value}, list_notify_block,
            'Check created basket')
        list_id = list_notify_block['OrderListID']
        # endregion

        # region manual exec first order
        self.trade_request.set_default_trade(order_id1, '20')
        responses = self.java_api_manager.send_message_and_receive_response(self.trade_request)
        self.return_result(responses, ORSMessageType.ExecutionReport.value)
        exec_report_block = self.result.get_parameter('ExecutionReportBlock')
        self.java_api_manager.compare_values(
            {JavaApiFields.TransExecStatus.value: ExecutionReportConst.TransExecStatus_FIL.value}, exec_report_block,
            'Check first Manual Execution')
        # endregion

        # region manual exec second order
        self.trade_request.set_default_trade(order_id2, '20')
        responses = self.java_api_manager.send_message_and_receive_response(self.trade_request)
        self.return_result(responses, ORSMessageType.ExecutionReport.value)
        exec_report_block = self.result.get_parameter('ExecutionReportBlock')
        self.java_api_manager.compare_values(
            {JavaApiFields.TransExecStatus.value: ExecutionReportConst.TransExecStatus_FIL.value}, exec_report_block,
            'Check second Manual Execution')
        # endregion

        # region complete orders
        self.dfd_manage_batch.set_default_complete_for_some_orders([order_id1, order_id2])
        responses = self.java_api_manager.send_message_and_receive_response(self.dfd_manage_batch)
        # endregion

        # region check fields
        self.return_result(responses, ORSMessageType.OrdReply.value)
        ord_reply_block = self.result.get_parameter('OrdReplyBlock')
        self.java_api_manager.compare_values(
            {JavaApiFields.DoneForDay.value: OrderReplyConst.DoneForDay_YES.value,
             JavaApiFields.OrderListID.value: list_id}, ord_reply_block,
            'Check values after complete')
        # endregion

        # region book basket
        self.alloc_instr_request.set_default_book(order_id1)
        responses = self.java_api_manager.send_message_and_receive_response(self.alloc_instr_request)
        self.return_result(responses, ORSMessageType.OrdUpdate.value)
        exec_report_block = self.result.get_parameter('OrdUpdateBlock')
        self.java_api_manager.compare_values(
            {JavaApiFields.PostTradeStatus.value: OrderReplyConst.PostTradeStatus_BKD.value}, exec_report_block,
            'Check values booking first order')
        self.alloc_instr_request.set_default_book(order_id2)
        responses = self.java_api_manager.send_message_and_receive_response(self.alloc_instr_request)
        self.return_result(responses, ORSMessageType.OrdUpdate.value)
        exec_report_block = self.result.get_parameter('OrdUpdateBlock')
        self.java_api_manager.compare_values(
            {JavaApiFields.PostTradeStatus.value: OrderReplyConst.PostTradeStatus_BKD.value}, exec_report_block,
            'Check values booking second order')
        # endregion

    def return_result(self, responses, message_type):
        for response in responses:
            if response.get_message_type() == message_type:
                self.result = response
