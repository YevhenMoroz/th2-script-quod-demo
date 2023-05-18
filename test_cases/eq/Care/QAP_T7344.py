import logging
from pathlib import Path

from custom import basic_custom_actions as bca
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import SubmitRequestConst, JavaApiFields, ExecutionReportConst, \
    OrderReplyConst
from test_framework.java_api_wrappers.oms.ors_messges.DFDManagementBatchOMS import DFDManagementBatchOMS
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.java_api_wrappers.oms.ors_messges.TradeEntryOMS import TradeEntryOMS

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


@try_except(test_id=Path(__file__).name[:-3])
class QAP_T7344(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.order_submit = OrderSubmitOMS(self.data_set)
        self.java_api_connectivity = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.complete_request = DFDManagementBatchOMS(self.data_set)
        self.manual_execute = TradeEntryOMS(self.data_set)
        self.rule_manager = RuleManager(Simulators.equity)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region precondition:
        # part 1: Create CO order
        self.order_submit.set_default_care_limit(recipient=self.environment.get_list_fe_environment()[0].user_1,
                                                 desk=self.environment.get_list_fe_environment()[0].desk_ids[0],
                                                 role=SubmitRequestConst.USER_ROLE_1.value)
        qty = '300'
        self.order_submit.update_fields_in_component(JavaApiFields.NewOrderSingleBlock.value,
                                                     {JavaApiFields.OrdQty.value: qty})
        price = self.order_submit.get_parameters()[JavaApiFields.NewOrderSingleBlock.value][JavaApiFields.Price.value]
        self.java_api_manager.send_message_and_receive_response(self.order_submit)
        ord_id = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value][JavaApiFields.OrdID.value]
        # end_of_part

        # part 2: Manual Execute CO order
        half_qty = str(float(qty) / 2)
        self.manual_execute.set_default_trade(ord_id, price, half_qty)
        self.java_api_manager.send_message_and_receive_response(self.manual_execute)
        execution_report = \
            self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value).get_parameters()[
                JavaApiFields.ExecutionReportBlock.value]
        exec_id = execution_report[JavaApiFields.ExecID.value]
        self.java_api_manager.compare_values(
            {JavaApiFields.TransExecStatus.value: ExecutionReportConst.TransExecStatus_PFL.value},
            execution_report, 'Verify that order Partially Filled (precondition)')
        # end_of_part

        # part 3: Complete CO order
        self.complete_request.set_default_complete(ord_id)
        self.java_api_manager.send_message_and_receive_response(self.complete_request)
        order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value]
        self.java_api_manager.compare_values(
            {JavaApiFields.PostTradeStatus.value: OrderReplyConst.PostTradeStatus_RDY.value,
             JavaApiFields.DoneForDay.value: OrderReplyConst.DoneForDay_YES.value}, order_reply,
            'Verify that order completed (precondition)')
        # end_of_part
        # endregion

        # region step 1: Uncomplete CO order
        self.complete_request.set_default_uncomplete(ord_id)
        self.java_api_manager.send_message_and_receive_response(self.complete_request)
        order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value]
        key_is_absent = not (JavaApiFields.DoneForDay.value in order_reply)
        self.java_api_manager.compare_values({'KeyIsAbsent': True}, {'KeyIsAbsent': key_is_absent},
                                             f'Verify that {JavaApiFields.DoneForDay.value} is empty (step 1)')
        key_is_absent = not (JavaApiFields.PostTradeStatus.value in order_reply)
        self.java_api_manager.compare_values({'KeyIsAbsent': True}, {'KeyIsAbsent': key_is_absent},
                                             f'Verify that {JavaApiFields.PostTradeStatus.value} is empty (step 1)')
        # endregion

        # region step 2-3: Split CO order and trade it
        try:
            venue_client = self.data_set.get_venue_client_names_by_name('client_1_venue_1')
            mic = self.data_set.get_mic_by_name('mic_1')
            self.rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(self.fix_env.buy_side,
                                                                                       venue_client, mic, float(price))
            self.rule_manager.add_NewOrdSingleExecutionReportTrade_FIXStandard(self.fix_env.buy_side, venue_client, mic,
                                                                               float(price), (int(int(qty) / 2)), 0)

            self.order_submit.set_default_child_dma(ord_id)
            self.order_submit.update_fields_in_component(JavaApiFields.NewOrderSingleBlock.value,
                                                         {JavaApiFields.OrdQty.value: half_qty})
            self.java_api_manager.send_message_and_receive_response(self.order_submit, {ord_id: ord_id})
            execution_report = \
                self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value).get_parameters()[
                    JavaApiFields.ExecutionReportBlock.value]
            self.java_api_manager.compare_values(
                {JavaApiFields.TransExecStatus.value: ExecutionReportConst.TransExecStatus_FIL.value},
                execution_report, 'Verify that order Filled (step 3)')
        except Exception as e:
            tb = e.__traceback__
            bca.create_event(f"TEST FAILED  {e.with_traceback(tb)}", self.test_id,
                             status='FAILED')
        # endregion

        # region step 4-5: Modify first execution
        modify_qty_of_exec = '100'
        self.manual_execute.set_default_replace_execution(ord_id, exec_id, price, modify_qty_of_exec)
        self.java_api_manager.send_message_and_receive_response(self.manual_execute)
        execution_report = \
            self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value).get_parameters()[
                JavaApiFields.ExecutionReportBlock.value]
        self.java_api_manager.compare_values(
            {JavaApiFields.TransExecStatus.value: ExecutionReportConst.TransExecStatus_PFL.value,
             JavaApiFields.UnmatchedQty.value: str(float(half_qty) - float(modify_qty_of_exec))},
            execution_report,
            f'Verify that order Partially Filled and has valid value for {JavaApiFields.UnmatchedQty.value} (step 5)')
        # endregion
