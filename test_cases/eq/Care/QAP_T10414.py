import logging
import time
from pathlib import Path

from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from custom import basic_custom_actions as bca
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.oms.FixMessageExecutionReportOMS import FixMessageExecutionReportOMS
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.cs_message.ManualMatchExecToParentOrdersRequest import \
    ManualMatchExecToParentOrdersRequest
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, ExecutionReportConst, OrderReplyConst
from test_framework.java_api_wrappers.oms.ors_messges.DFDManagementBatchOMS import DFDManagementBatchOMS
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.java_api_wrappers.oms.ors_messges.TradeEntryOMS import TradeEntryOMS
from test_framework.java_api_wrappers.ors_messages.OrderActionRequest import OrderActionRequest
from test_framework.java_api_wrappers.ors_messages.UnMatchRequest import UnMatchRequest

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP_T10414(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.java_api_connectivity = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.bs_connectivity = self.fix_env.buy_side
        self.ss_connectivity = self.fix_env.sell_side
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set).set_default_care_limit()
        self.price = self.fix_message.get_parameter("Price")
        self.qty = self.fix_message.get_parameter("OrderQtyData")['OrderQty']
        self.fix_verifier = FixVerifier(self.fix_env.sell_side, self.test_id)
        self.action_request = OrderActionRequest()
        self.order_submit = OrderSubmitOMS(data_set)
        self.rule_manager = RuleManager(sim=Simulators.equity)
        self.mic = self.data_set.get_mic_by_name("mic_1")
        self.client_for_rule = self.data_set.get_venue_client_names_by_name("client_1_venue_1")
        self.unmatch_request = UnMatchRequest()
        self.match_request = ManualMatchExecToParentOrdersRequest()
        self.trade_entry_request = TradeEntryOMS(self.data_set)
        self.fix_verifier_sell = FixVerifier(self.ss_connectivity, self.test_id)
        self.exec_report = FixMessageExecutionReportOMS(self.data_set)
        self.dfd_manag_batch = DFDManagementBatchOMS(self.data_set)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declaration
        # region create CO order
        response = self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message)
        order_id = response[0].get_parameter("OrderID")
        cl_ord_id = response[0].get_parameter("ClOrdID")
        # endregion

        # region set disclose execution
        self.action_request.set_default([order_id])
        order_dict = {order_id: order_id}
        self.java_api_manager.send_message_and_receive_response(self.action_request, order_dict)
        # endregion

        # region check values
        ord_notify = self.java_api_manager.get_last_message(
            ORSMessageType.OrdNotification.value, order_id).get_parameter(JavaApiFields.OrdNotificationBlock.value)
        self.java_api_manager.compare_values({JavaApiFields.DiscloseExec.value: OrderReplyConst.DiscloseExec_M.value},
                                             ord_notify, "Check DiscloseExec")
        # endregion

        # region split order
        open_rule = None
        trade_rule = None
        try:
            open_rule = self.rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(self.bs_connectivity,
                                                                                                   self.client_for_rule,
                                                                                                   self.mic,
                                                                                                   int(self.price))
            trade_rule = self.rule_manager.add_NewOrdSingleExecutionReportTrade_FIXStandard(self.bs_connectivity,
                                                                                            self.client_for_rule,
                                                                                            self.mic,
                                                                                            int(self.price),
                                                                                            int(self.qty), 2)
            self.order_submit.set_default_child_dma(order_id)
            self.order_submit.update_fields_in_component('NewOrderSingleBlock', {
                'InstrID': self.data_set.get_instrument_id_by_name("instrument_2"), 'ClOrdID': cl_ord_id})
            self.java_api_manager.send_message_and_receive_response(self.order_submit)
        finally:
            time.sleep(1)
            self.rule_manager.remove_rule(open_rule)
            self.rule_manager.remove_rule(trade_rule)
        # endregion

        # region check values
        child_order_id = self.java_api_manager.get_last_message(
            ORSMessageType.OrdReply.value).get_parameter(JavaApiFields.OrdReplyBlock.value)['OrdID']
        exec_report = self.java_api_manager.get_last_message(
            ORSMessageType.ExecutionReport.value, order_id).get_parameter(JavaApiFields.ExecutionReportBlock.value)
        parent_exec_id1 = exec_report[JavaApiFields.ExecID.value]
        exec_report = self.java_api_manager.get_last_message(
            ORSMessageType.ExecutionReport.value, child_order_id).get_parameter(
            JavaApiFields.ExecutionReportBlock.value)
        child_exec_id = exec_report[JavaApiFields.ExecID.value]
        # endregion

        # region unmatch execution
        self.unmatch_request.set_default(self.data_set, parent_exec_id1)
        self.java_api_manager.send_message_and_receive_response(self.unmatch_request)
        # endregion

        # region check values
        exec_report = self.java_api_manager.get_last_message(
            ORSMessageType.ExecutionReport.value, order_id).get_parameter(JavaApiFields.ExecutionReportBlock.value)
        self.java_api_manager.compare_values({JavaApiFields.ExecType.value: ExecutionReportConst.ExecType_CAN.value},
                                             exec_report, "Check Exec sts after UnMatch action")
        # endregion

        # region match child execution with parent order again
        qty_to_match = str(int(int(self.qty) / 2))
        self.match_request.set_default(order_id, qty_to_match, child_exec_id)
        self.java_api_manager.send_message_and_receive_response(self.match_request)
        # endregion

        # region check values
        exec_report = self.java_api_manager.get_last_message(
            ORSMessageType.ExecutionReport.value, order_id).get_parameter(JavaApiFields.ExecutionReportBlock.value)
        self.java_api_manager.compare_values({JavaApiFields.ExecType.value: ExecutionReportConst.ExecType_TRD.value,
                                              JavaApiFields.TransExecStatus.value: ExecutionReportConst.TransExecStatus_PFL.value},
                                             exec_report, "Check Exec sts after Manual Match action")
        parent_exec_id2 = exec_report[JavaApiFields.ExecID.value]
        # endregion

        # region Exec Summary
        self.trade_entry_request.set_default_execution_summary(order_id, [parent_exec_id2], self.price, qty_to_match)
        self.java_api_manager.send_message_and_receive_response(self.trade_entry_request)
        # endregion

        # region check values
        exec_report = self.java_api_manager.get_last_message(
            ORSMessageType.ExecutionReport.value, order_id).get_parameter(JavaApiFields.ExecutionReportBlock.value)
        self.java_api_manager.compare_values({JavaApiFields.ExecType.value: ExecutionReportConst.ExecType_CAL.value,
                                              JavaApiFields.ExecQty.value: qty_to_match+'.0'},
                                             exec_report, "Check Exec sts after Exec Summary action")
        # endregion

        # region check values on Sell-side gtw
        ignored_list = ['GatingRuleCondName', 'GatingRuleName', 'VenueType', 'TradeDate', 'LastMkt']
        self.exec_report.set_default_calculated(self.fix_message)
        self.exec_report.change_parameters({'LastQty': qty_to_match})
        self.fix_verifier.check_fix_message_fix_standard(self.exec_report, ['LastQty'], ignored_fields=ignored_list)
        # endregion

        # region complete order
        self.dfd_manag_batch.set_default_complete(order_id)
        self.java_api_manager.send_message_and_receive_response(self.dfd_manag_batch)
        # endregion

        # region check values
        order_reply_message = self.java_api_manager.get_last_message(
            ORSMessageType.OrdReply.value).get_parameters()[JavaApiFields.OrdReplyBlock.value]
        expected_result = {JavaApiFields.PostTradeStatus.value: OrderReplyConst.PostTradeStatus_RDY.value,
                           JavaApiFields.DoneForDay.value: OrderReplyConst.DoneForDay_YES.value}
        self.java_api_manager.compare_values(expected_result, order_reply_message, 'Check order values after Complete')
        exec_report = self.java_api_manager.get_last_message(
            ORSMessageType.ExecutionReport.value, order_id).get_parameter(JavaApiFields.ExecutionReportBlock.value)
        self.java_api_manager.compare_values({JavaApiFields.ExecType.value: ExecutionReportConst.ExecType_CAL.value},
                                             exec_report, "Check Exec report after Complete action")
        # endregion
