import logging
import os
from pathlib import Path

from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.oms.FixMessageExecutionReportOMS import FixMessageExecutionReportOMS
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, ExecutionReportConst, OrderReplyConst
from test_framework.java_api_wrappers.oms.ors_messges.DFDManagementBatchOMS import DFDManagementBatchOMS
from test_framework.java_api_wrappers.oms.ors_messges.TradeEntryOMS import TradeEntryOMS

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP_T8940(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(os.path.basename(__file__)[:-3], self.report_id)
        self.java_api_connectivity = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.ss_connectivity = self.fix_env.sell_side
        self.dc_connectivity = self.fix_env.drop_copy
        self.fix_manager = FixManager(self.ss_connectivity, self.test_id)
        self.new_order_single = FixMessageNewOrderSingleOMS(self.data_set).set_default_care_limit()
        self.trade_entry_message = TradeEntryOMS(self.data_set)
        self.qty = self.new_order_single.get_parameter('OrderQtyData')['OrderQty']
        self.price = self.new_order_single.get_parameter('Price')
        self.price_to_replace_fill = '15'
        self.fix_verifier_dc = FixVerifier(self.dc_connectivity, self.test_id)
        self.exec_report = FixMessageExecutionReportOMS(self.data_set)
        self.dfd_batch = DFDManagementBatchOMS(self.data_set)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # STEP 1
        # region create order
        response = self.fix_manager.send_message_and_receive_response_fix_standard(self.new_order_single)
        order_id = response[0].get_parameter("OrderID")
        # endregion

        # region do manual execution
        self.trade_entry_message.set_default_trade(order_id, self.price)
        self.java_api_manager.send_message_and_receive_response(self.trade_entry_message)
        exec_report = self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value).get_parameter(
            JavaApiFields.ExecutionReportBlock.value)
        exec_id = exec_report[JavaApiFields.ExecID.value]
        self.java_api_manager.compare_values(
            {JavaApiFields.TransExecStatus.value: ExecutionReportConst.TransExecStatus_FIL.value}, exec_report,
            'Check order after execution')
        # endregion

        # STEP 2
        # region complete order
        self.dfd_batch.set_default_complete(order_id)
        self.java_api_manager.send_message_and_receive_response(self.dfd_batch)
        exec_report = self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value).get_parameter(
            JavaApiFields.ExecutionReportBlock.value)
        self.java_api_manager.compare_values(
            {JavaApiFields.DoneForDay.value: OrderReplyConst.DoneForDay_YES.value,
             JavaApiFields.PostTradeStatus.value: OrderReplyConst.PostTradeStatus_RDY.value}, exec_report,
            'Check order after complete')
        # endregion

        # STEP 3
        # region uncomplete order
        self.dfd_batch.set_default_uncomplete(order_id)
        self.java_api_manager.send_message_and_receive_response(self.dfd_batch)
        # endregion

        # STEP 4
        # region amend manual execution
        self.trade_entry_message.set_default_replace_execution(order_id, exec_id, self.price_to_replace_fill)
        self.java_api_manager.send_message_and_receive_response(self.trade_entry_message)
        exec_report = self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value).get_parameter(
            JavaApiFields.ExecutionReportBlock.value)
        self.java_api_manager.compare_values(
            {JavaApiFields.ExecPrice.value: self.price_to_replace_fill + '.0',
             JavaApiFields.ExecQty.value: self.qty + '.0',
             JavaApiFields.TransExecStatus.value: ExecutionReportConst.TransExecStatus_FIL.value}, exec_report,
            'Check order after execution modification')
        # endregion

        # STEP 5
        # region complete order
        self.dfd_batch.set_default_complete(order_id)
        self.java_api_manager.send_message_and_receive_response(self.dfd_batch)
        exec_report = self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value).get_parameter(
            JavaApiFields.ExecutionReportBlock.value)
        self.java_api_manager.compare_values(
            {JavaApiFields.DoneForDay.value: OrderReplyConst.DoneForDay_YES.value,
             JavaApiFields.PostTradeStatus.value: OrderReplyConst.PostTradeStatus_RDY.value}, exec_report,
            'Check order after second complete')
        # endregion

        # region check 35=8, 150=B message
        ignored_fields = ['GatingRuleCondName', 'GatingRuleName', 'Parties', 'QuodTradeQualifier', 'BookID',
                          'TradeReportingIndicator', 'NoParty', 'tag5120', 'ExecBroker']
        self.exec_report.set_default_calculated(self.new_order_single)
        self.exec_report.change_parameters({'AvgPx': '15'})
        self.fix_verifier_dc.check_fix_message_fix_standard(self.exec_report, ['AvgPx', 'ExecType'],
                                                            ignored_fields=ignored_fields)
        # endregion
