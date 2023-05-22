import logging
import os
from pathlib import Path

from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import ExecutionReportConst, JavaApiFields, SubmitRequestConst, \
    OrderReplyConst
from test_framework.java_api_wrappers.oms.ors_messges.DFDManagementBatchOMS import DFDManagementBatchOMS
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.java_api_wrappers.oms.ors_messges.TradeEntryOMS import TradeEntryOMS

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP_T7343(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(os.path.basename(__file__)[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.trade_entry_message = TradeEntryOMS(self.data_set)
        self.order_submit = OrderSubmitOMS(self.data_set)
        self.java_api_connectivity = self.java_api = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.complete_request = DFDManagementBatchOMS(self.data_set)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declaration
        qty = '1000'
        price = '10'
        # endregion

        # region step 1: create CO order
        self.order_submit.set_default_care_limit(recipient=self.environment.get_list_fe_environment()[0].user_1,
                                                 desk=self.environment.get_list_fe_environment()[0].desk_ids[0],
                                                 role=SubmitRequestConst.USER_ROLE_1.value)
        self.order_submit.update_fields_in_component(JavaApiFields.NewOrderSingleBlock.value,
                                                     {JavaApiFields.OrdQty.value: qty,
                                                      JavaApiFields.Price.value: price})
        self.java_api_manager.send_message_and_receive_response(self.order_submit)
        order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value]
        order_id = order_reply[JavaApiFields.OrdID.value]
        self.java_api_manager.compare_values({JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_OPN.value},
                                             order_reply, 'Verify that order created (step 1)')
        # endregion

        # region step 2-4: Partially fill CO order
        self.trade_entry_message.set_default_trade(order_id, price, str(float(qty) / 2))
        self.java_api_manager.send_message_and_receive_response(self.trade_entry_message)
        execution_report = \
        self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value).get_parameters()[
            JavaApiFields.ExecutionReportBlock.value]
        exec_id = execution_report[JavaApiFields.ExecID.value]
        self.java_api_manager.compare_values(
            {JavaApiFields.TransExecStatus.value: ExecutionReportConst.TransExecStatus_PFL.value}, execution_report,
            'Verify that order Partially Filled (step 4)')
        # endregion

        # region step 5 : Complete CO order
        self.complete_request.set_default_complete(order_id)
        self.java_api_manager.send_message_and_receive_response(self.complete_request)
        order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value]
        self.java_api_manager.compare_values(
            {JavaApiFields.PostTradeStatus.value: OrderReplyConst.PostTradeStatus_RDY.value,
             JavaApiFields.DoneForDay.value: OrderReplyConst.DoneForDay_YES.value},
            order_reply,
            "Comparing values of step 5")
        # endregion

        # region step 6: Modify Manual Execution
        self.trade_entry_message.set_default_replace_execution(order_id, exec_id, price, qty)
        self.java_api_manager.send_message_and_receive_response(self.trade_entry_message)
        trade_entry_reply = self.java_api_manager.get_last_message(ORSMessageType.TradeEntryReply.value).get_parameters()\
            [JavaApiFields.MessageReply.value][JavaApiFields.MessageReplyBlock.value][0]
        self.java_api_manager.compare_values({JavaApiFields.ErrorMsg.value: f"Invalid 'DoneForDay': {order_id}"},
                                             trade_entry_reply, 'Verify that error message present (step 6)')
        # endregion