import logging
import os
import time
from pathlib import Path
from custom import basic_custom_actions as bca
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.cs_message.ManualMatchExecToParentOrdersRequest import \
    ManualMatchExecToParentOrdersRequest
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, ExecutionReportConst, OrderReplyConst
from test_framework.java_api_wrappers.ors_messages.UnMatchRequest import UnMatchRequest

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP_T7422(TestCase):
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(os.path.basename(__file__)[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.java_api = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api, self.test_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.fix_message_dma = FixMessageNewOrderSingleOMS(self.data_set).set_default_dma_limit()
        self.price = '10'
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set)
        self.fix_message.set_default_dma_limit()
        self.fix_message.change_parameter('Price', self.price)
        self.qty_dma = self.fix_message.get_parameter('OrderQtyData')['OrderQty']
        self.client_for_rule = self.data_set.get_venue_client_names_by_name('client_1_venue_1')
        self.exec_destination = self.data_set.get_mic_by_name('mic_1')
        self.lookup = self.data_set.get_lookup_by_name('lookup_1')
        self.rule_manager = RuleManager(Simulators.equity)
        self.manual_match_request = ManualMatchExecToParentOrdersRequest()
        self.unmatch_request = UnMatchRequest()
        self.washbook = self.data_set.get_washbook_account_by_name('washbook_account_1')

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):

        # region create  DMA order
        dma_order_id = None
        trade_rule = None
        nos_rule = None
        exec_id = None
        try:
            nos_rule = self.rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(self.fix_env.buy_side,
                                                                                                  self.client_for_rule,
                                                                                                  self.exec_destination,
                                                                                                  float(self.price))
            trade_rule = self.rule_manager.add_NewOrdSingleExecutionReportTrade_FIXStandard(self.fix_env.buy_side,
                                                                                            self.client_for_rule,
                                                                                            self.exec_destination,
                                                                                            float(self.price),
                                                                                            int(self.qty_dma),
                                                                                            delay=0)
            response = self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message)
            exec_id = response[5].get_parameters()['ExecID']
        except Exception as e:
            logger.error(f'{e}')

        finally:
            time.sleep(5)
            self.rule_manager.remove_rule(nos_rule)
            self.rule_manager.remove_rule(trade_rule)
        # endregion

        # region create and accept CO order
        self.fix_message.set_default_care_limit()
        qty_care = self.fix_message.get_parameter('OrderQtyData')['OrderQty']
        response = self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message)
        care_order_id = response[0].get_parameters()['OrderID']
        # endregion

        # region match
        self.manual_match_request.set_default(care_order_id, qty_care, exec_id)
        self.java_api_manager.send_message_and_receive_response(self.manual_match_request)
        # endregion

        # region verifying values of care order after match
        exec_report_block = self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value).get_parameter(
            JavaApiFields.ExecutionReportBlock.value)
        self.java_api_manager.compare_values(
            {JavaApiFields.TransExecStatus.value: ExecutionReportConst.TransExecStatus_FIL.value,
             JavaApiFields.UnmatchedQty.value: '0.0',
             JavaApiFields.ExecType.value: ExecutionReportConst.ExecType_TRD.value}, exec_report_block,
            'Comparing values at CO order(after match)')
        # endregion

        # region extraction execution from CO order
        exec_id_co_order = exec_report_block['ExecID']
        # endregion

        # region unmatch order on half of qty
        half_of_qty = str(int(int(qty_care) / 2))
        self.unmatch_request.set_default(self.data_set, exec_id_co_order, half_of_qty, self.washbook)
        self.java_api_manager.send_message_and_receive_response(self.unmatch_request)
        # endregion

        # region verifying values of care order after first unmatch
        exec_report_block = self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value).get_parameter(
            JavaApiFields.ExecutionReportBlock.value)
        self.java_api_manager.compare_values(
            {JavaApiFields.TransExecStatus.value: ExecutionReportConst.TransExecStatus_PFL.value,
             JavaApiFields.UnmatchedQty.value: half_of_qty + '.0'}, exec_report_block,
            'Comparing values at CO order(after unmatch on half of qty)')
        # endregion

        # region unmatch order on half of qty
        exec_id_co_order = exec_report_block['ExecID']
        self.unmatch_request.set_default(self.data_set, exec_id_co_order, half_of_qty, self.washbook)
        self.java_api_manager.send_message_and_receive_response(self.unmatch_request)
        # endregion

        # region verifying values of care order after second unmatch
        exec_report_block = self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value).get_parameter(
            JavaApiFields.ExecutionReportBlock.value)
        self.java_api_manager.compare_values(
            {JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_OPN.value,
             JavaApiFields.UnmatchedQty.value: qty_care + '.0',
             JavaApiFields.ExecType.value: ExecutionReportConst.ExecType_CAN.value}, exec_report_block,
            'Comparing values at CO order(after unmatch on half of remaining qty)')
        # endregion
