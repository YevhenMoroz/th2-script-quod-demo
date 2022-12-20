import logging
import os
from pathlib import Path

from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from custom.verifier import VerificationMethod
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, OrderReplyConst, AllocationReportConst, \
    ConfirmationReportConst, ExecutionReportConst
from test_framework.java_api_wrappers.oms.es_messages.ExecutionReportOMS import ExecutionReportOMS
from test_framework.java_api_wrappers.oms.ors_messges.AllocationInstructionOMS import AllocationInstructionOMS
from test_framework.java_api_wrappers.oms.ors_messges.ForceAllocInstructionStatusRequestOMS import \
    ForceAllocInstructionStatusRequestOMS
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def print_message(message, responses):
    logger.info(message)
    for i in responses:
        logger.info(i)
        logger.info(i.get_parameters())


class QAP_T7532(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(os.path.basename(__file__)[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.java_api = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api, self.test_id)
        self.order_submit = OrderSubmitOMS(self.data_set)
        self.execution_report = ExecutionReportOMS(self.data_set)
        self.allocation_instruction = AllocationInstructionOMS(self.data_set)
        self.approve_block = self.approve_block = ForceAllocInstructionStatusRequestOMS(self.data_set)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declaration
        qty = '200'
        price = '10'
        client = self.data_set.get_client_by_name('client_pt_4')
        client_acc1 = self.data_set.get_account_by_name("client_pt_4_acc_1")
        exec_destination = self.data_set.get_mic_by_name('mic_1')
        # endregion

        # region precondition
        # create DMA order (part of precondition)
        self.order_submit.set_default_dma_limit()
        self.order_submit.update_fields_in_component('NewOrderSingleBlock', {
            'AccountGroupID': client,
            'OrdQty': qty,
            'Price': price,
            'PreTradeAllocationBlock': {"PreTradeAllocationList": {"PreTradeAllocAccountBlock":[{'AllocAccountID': client_acc1, 'AllocQty': qty}]}},
        })
        responses = self.java_api_manager.send_message_and_receive_response(self.order_submit)
        print_message('Create DMA  order', responses)
        order_id = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value][JavaApiFields.OrdID.value]
        # the end

        # trade DMA order (part of precondition)
        self.execution_report.set_default_trade(order_id)
        self.execution_report.update_fields_in_component('ExecutionReportBlock',
                                                         {
                                                             "InstrumentBlock": self.data_set.get_java_api_instrument(
                                                                 "instrument_2"),
                                                             "Side": "Buy",
                                                             "LastTradedQty": qty,
                                                             "LastPx": price,
                                                             "OrdType": "Limit",
                                                             "Price": price,
                                                             "LeavesQty": qty,
                                                             "CumQty": qty,
                                                             "AvgPrice": price,
                                                             "LastMkt": exec_destination,
                                                             "OrdQty": qty
                                                         })
        responses = self.java_api_manager.send_message_and_receive_response(self.execution_report)
        print_message('Trade DMA  order ', responses)
        # the end

        # check PostTrade Status and ExecSts (part of precondition)
        order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value]
        execution_report = \
            self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value, ExecutionReportConst.ExecType_TRD.value).get_parameters()[
                JavaApiFields.ExecutionReportBlock.value]
        exec_id = execution_report[JavaApiFields.ExecID.value]
        self.java_api_manager.compare_values(
            {JavaApiFields.PostTradeStatus.value: OrderReplyConst.PostTradeStatus_RDY.value,
             JavaApiFields.DoneForDay.value: OrderReplyConst.DoneForDay_YES.value},
            order_reply,
            'Check expected and actually PostTradeStatus and DoneForDay values (part of precondition)')
        # the end
        # endregion

        # region Book DMA order (step 1)
        self.allocation_instruction.set_default_book(order_id)
        gross_trade_amt = str(float(qty) * float(price))
        self.allocation_instruction.update_fields_in_component('AllocationInstructionBlock', {
            "AccountGroupID": client,
            "SettlCurrAmt": gross_trade_amt,
            'Qty': qty,
            'ExecAllocList': {
                'ExecAllocBlock': [{'ExecQty': qty,
                                    'ExecID': exec_id,
                                    'ExecPrice': price}]},
            "ComputeFeesCommissions": "Yes"
        })
        responses = self.java_api_manager.send_message_and_receive_response(self.allocation_instruction)
        print_message(f'Book {order_id} order', responses)
        allocation_report = \
            self.java_api_manager.get_last_message(ORSMessageType.AllocationReport.value).get_parameters()[
                JavaApiFields.AllocationReportBlock.value]
        order_update = self.java_api_manager.get_last_message(ORSMessageType.OrdUpdate.value).get_parameters()[
            JavaApiFields.OrdUpdateBlock.value]
        alloc_id = allocation_report[JavaApiFields.ClientAllocID.value]

        # check PostTradeStatus (part of step 1)
        self.java_api_manager.compare_values(
            {JavaApiFields.PostTradeStatus.value: OrderReplyConst.PostTradeStatus_BKD.value},
            order_update, 'Check PostTradeStatus (part of step 1)')
        # the end

        # check Status and Match Status and SummaryStatus
        expected_result = {
            JavaApiFields.AllocStatus.value: AllocationReportConst.AllocStatus_APP.value,
            JavaApiFields.MatchStatus.value: ConfirmationReportConst.MatchStatus_UNM.value
        }

        self.java_api_manager.compare_values(expected_result, allocation_report,
                                             'Check Status and Match Status (part of step 1)')
        self.java_api_manager.key_is_absent(JavaApiFields.AllocSummaryStatus.value, allocation_report,
                                            'Check that AllocSummaryStatus is missed (part of step 1)')
        # the end
        # endregion

        # region step 2
        self.approve_block.set_default_approve(alloc_id)
        responses = self.java_api_manager.send_message_and_receive_response(self.approve_block)
        print_message('Approve Block', responses)
        allocation_report = \
        self.java_api_manager.get_last_message(ORSMessageType.AllocationReport.value).get_parameters()[
            JavaApiFields.AllocationReportBlock.value]
        expected_result.update({JavaApiFields.AllocStatus.value: AllocationReportConst.AllocStatus_ACK.value,
                                JavaApiFields.MatchStatus.value: ConfirmationReportConst.MatchStatus_MAT.value,
                                JavaApiFields.AllocSummaryStatus.value: AllocationReportConst.AllocSummaryStatus_MAG.value})
        self.java_api_manager.compare_values(expected_result, allocation_report,
                                             'Check Status, Match Status and Summary Status ( part of step 2)')
        confirmation_report = self.java_api_manager.get_last_message(ORSMessageType.ConfirmationReport.value).get_parameters()[JavaApiFields.ConfirmationReportBlock.value]
        expected_result.clear()
        expected_result.update({JavaApiFields.ConfirmStatus.value: ConfirmationReportConst.ConfirmStatus_AFF.value,
                                JavaApiFields.MatchStatus.value: ConfirmationReportConst.MatchStatus_MAT.value,
                                JavaApiFields.NetPrice.value: str(float(price)),
                                JavaApiFields.AllocQty.value: str(float(qty))})
        self.java_api_manager.compare_values(expected_result, confirmation_report,
                                             'Check Status , MatchStatus, Qty and Price ( part of step 2)')
        # endregion
