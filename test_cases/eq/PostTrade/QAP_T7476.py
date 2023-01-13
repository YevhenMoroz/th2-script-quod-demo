import logging
from pathlib import Path

from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.oms.FixMessageConfirmationReportOMS import FixMessageConfirmationReportOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, ExecutionReportConst, OrderReplyConst, \
    AllocationReportConst, ConfirmationReportConst, AllocationInstructionConst
from test_framework.java_api_wrappers.oms.es_messages.ExecutionReportOMS import ExecutionReportOMS
from test_framework.java_api_wrappers.oms.ors_messges.AllocationInstructionOMS import AllocationInstructionOMS
from test_framework.java_api_wrappers.oms.ors_messges.ConfirmationOMS import ConfirmationOMS
from test_framework.java_api_wrappers.oms.ors_messges.ForceAllocInstructionStatusRequestOMS import \
    ForceAllocInstructionStatusRequestOMS
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP_T7476(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.order_submit = OrderSubmitOMS(data_set)
        self.allocation_instruction = AllocationInstructionOMS(self.data_set)
        self.execution_report = ExecutionReportOMS(self.data_set)
        self.confirmation_request = ConfirmationOMS(self.data_set)
        self.approve_message = ForceAllocInstructionStatusRequestOMS(self.data_set)
        self.currency = self.data_set.get_currency_by_name('currency_1')
        self.java_api_connectivity = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.confirmation_report = FixMessageConfirmationReportOMS(self.data_set)
        self.fix_verifier = FixVerifier(self.fix_env.drop_copy, self.test_id)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declaration
        qty = '500'
        price = '50'
        negative_value = '-1'
        account = self.data_set.get_account_by_name('client_pt_1_acc_1')
        client = self.data_set.get_client_by_name('client_pt_1')
        # endregion

        # region precondition

        # part 1 : Create DMA order
        self.order_submit.set_default_dma_limit()
        self.order_submit.update_fields_in_component(
            "NewOrderSingleBlock",
            {"OrdQty": qty,
             "AccountGroupID": client,
             "Price": price})
        self.java_api_manager.send_message_and_receive_response(self.order_submit)
        order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value
        ]
        ord_id = order_reply[JavaApiFields.OrdID.value]
        cl_ord_id = order_reply[JavaApiFields.ClOrdID.value]
        # end of part

        # part 2 (trade dma order)
        self.execution_report.set_default_trade(ord_id)
        self.execution_report.update_fields_in_component(
            "ExecutionReportBlock",
            {
                "Price": price,
                "AvgPrice": price,
                "LastPx": price,
                "OrdQty": qty,
                "LastTradedQty": qty,
                "CumQty": qty,
            },
        )
        self.java_api_manager.send_message_and_receive_response(self.execution_report)
        execution_report_message = self.java_api_manager.get_last_message(
            ORSMessageType.ExecutionReport.value, ExecutionReportConst.ExecType_TRD.value
        ).get_parameters()[JavaApiFields.ExecutionReportBlock.value]
        order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value]
        self.java_api_manager.compare_values(
            {JavaApiFields.TransExecStatus.value: ExecutionReportConst.TransExecStatus_FIL.value, },
            execution_report_message,
            "Comparing ExecSts after Execute DMA (part of precondition)")
        self.java_api_manager.compare_values(
            {JavaApiFields.PostTradeStatus.value: OrderReplyConst.PostTradeStatus_RDY.value, },
            order_reply,
            "Comparing PostTradeStatus after Execute DMA (part of precondition)", )
        exec_id = execution_report_message[JavaApiFields.ExecID.value]
        # end of part

        # endregion

        # region step 1 : Book order
        self.allocation_instruction.set_default_book(ord_id)
        gross_trade_amt = float(price) * float(qty)
        self.allocation_instruction.set_default_book(ord_id)
        self.allocation_instruction.update_fields_in_component('AllocationInstructionBlock',
                                                               {"Qty": qty,
                                                                "AvgPx": price,
                                                                'GrossTradeAmt': str(gross_trade_amt),
                                                                "SettlCurrAmt": str(gross_trade_amt),
                                                                'ExecAllocList': {
                                                                    'ExecAllocBlock': [{'ExecQty': qty,
                                                                                        'ExecID': exec_id,
                                                                                        'ExecPrice': price}]},
                                                                })
        self.java_api_manager.send_message_and_receive_response(self.allocation_instruction)
        allocation_report = \
            self.java_api_manager.get_last_message(ORSMessageType.AllocationReport.value, JavaApiFields.BookingAllocInstructionID).get_parameters()[
                JavaApiFields.AllocationReportBlock.value]
        order_update = self.java_api_manager.get_last_message(ORSMessageType.OrdUpdate.value).get_parameters()[
            JavaApiFields.OrdUpdateBlock.value]
        alloc_id = allocation_report[JavaApiFields.ClientAllocID.value]
        self.java_api_manager.compare_values(
            {JavaApiFields.AllocStatus.value: AllocationReportConst.AllocStatus_APP.value,
             JavaApiFields.MatchStatus.value: ConfirmationReportConst.MatchStatus_UNM.value},
            allocation_report,
            'Check expected and actually results for block (step 1)')
        self.java_api_manager.compare_values(
            {JavaApiFields.PostTradeStatus.value: OrderReplyConst.PostTradeStatus_BKD.value},
            order_update, 'Check expected and actually result for order (step 1)')
        # endregion

        # region step 2 : Amend block
        fee_amt = float(qty) * float(price) / 100 * float(negative_value)
        client_commission = {
            JavaApiFields.CommissionAmountType.value: AllocationInstructionConst.CommissionAmountType_BRK.value,
            JavaApiFields.CommissionAmount.value: str(float(negative_value)),
            JavaApiFields.CommissionAmountSubType.value: AllocationInstructionConst.CommissionAmountSubType_OTH.value,
            JavaApiFields.CommissionBasis.value: AllocationInstructionConst.COMM_AND_FEE_BASIS_ABS.value,
            JavaApiFields.CommissionCurrency.value: self.currency,
            JavaApiFields.CommissionRate.value: str(float(negative_value))
        }
        root_misc_fee_list = {
            JavaApiFields.RootMiscFeeType.value: AllocationInstructionConst.COMM_AMD_FEE_TYPE_REG.value,
            JavaApiFields.RootMiscFeeAmt.value: str(fee_amt),
            JavaApiFields.RootMiscFeeCurr.value: self.currency,
            JavaApiFields.RootMiscFeeBasis.value: AllocationInstructionConst.COMM_AND_FEES_BASIS_P.value,
            JavaApiFields.RootMiscFeeRate.value: negative_value,
            JavaApiFields.RootMiscFeeCategory.value: AllocationInstructionConst.RootMiscFeeCategory_OTH.value
        }
        self.allocation_instruction.set_amend_book(alloc_id, exec_id, qty, price)
        self.allocation_instruction.update_fields_in_component('AllocationInstructionBlock',
                                                               {
                                                                   JavaApiFields.ClientCommissionList.value: {
                                                                       JavaApiFields.ClientCommissionBlock.value:
                                                                           [client_commission]},
                                                                   JavaApiFields.RootMiscFeesList.value: {
                                                                       JavaApiFields.RootMiscFeesBlock.value: [
                                                                           root_misc_fee_list]}
                                                               })
        self.java_api_manager.send_message_and_receive_response(self.allocation_instruction)
        # endregion

        # region step 3: approve block
        self.approve_message.set_default_approve(alloc_id)
        self.java_api_manager.send_message_and_receive_response(self.approve_message)
        allocation_report = \
            self.java_api_manager.get_last_message(ORSMessageType.AllocationReport.value).get_parameters()[
                JavaApiFields.AllocationReportBlock.value]
        self.java_api_manager.compare_values(
            {JavaApiFields.AllocStatus.value: AllocationReportConst.AllocStatus_ACK.value,
             JavaApiFields.MatchStatus.value: AllocationReportConst.MatchStatus_MAT.value},
            allocation_report,
            'Check expected and actually results for block (step 3)')
        # endregion

        # region step 4 : Allocate block
        self.confirmation_request.set_default_allocation(alloc_id)
        self.confirmation_request.update_fields_in_component('ConfirmationBlock',
                                                             {"AllocQty": qty,
                                                              "Side": "B",
                                                              "AvgPx": price,
                                                              "AllocAccountID": account})
        self.java_api_manager.send_message_and_receive_response(self.confirmation_request)
        confirmation_report = \
            self.java_api_manager.get_last_message(ORSMessageType.ConfirmationReport.value).get_parameters()[
                JavaApiFields.ConfirmationReportBlock.value]
        allocation_report = \
            self.java_api_manager.get_last_message(ORSMessageType.AllocationReport.value).get_parameters()[
                JavaApiFields.AllocationReportBlock.value]
        self.java_api_manager.compare_values(
            {JavaApiFields.AllocStatus.value: AllocationReportConst.AllocStatus_ACK.value,
             JavaApiFields.MatchStatus.value: AllocationReportConst.MatchStatus_MAT.value,
             JavaApiFields.AllocSummaryStatus.value: AllocationReportConst.AllocSummaryStatus_MAG.value},
            allocation_report,
            'Check expected and actually results for block (step 4)')
        self.java_api_manager.compare_values({
            JavaApiFields.ConfirmStatus.value: ConfirmationReportConst.ConfirmStatus_AFF.value,
            JavaApiFields.MatchStatus.value: ConfirmationReportConst.MatchStatus_MAT.value
        }, confirmation_report, 'Check expected and actually results for allocation (step 4)')
        # endregion

        # check that confirmation report has fees and commission
        misc_fee_list = {
            JavaApiFields.MiscFeeType.value: AllocationInstructionConst.COMM_AMD_FEE_TYPE_REG.value,
            JavaApiFields.MiscFeeAmt.value: str(float(fee_amt)),
            JavaApiFields.MiscFeeCurr.value: self.currency,
            JavaApiFields.MiscFeeBasis.value: AllocationInstructionConst.COMM_AND_FEES_BASIS_P.value,
            JavaApiFields.MiscFeeRate.value: str(float(negative_value))}
        self.java_api_manager.compare_values(client_commission,
                                             confirmation_report[JavaApiFields.ClientCommissionList.value][
                                                 JavaApiFields.ClientCommissionBlock.value][0],
                                             'Check that allocation has negative commission')
        self.java_api_manager.compare_values(misc_fee_list, confirmation_report[JavaApiFields.MiscFeesList.value][
            JavaApiFields.MiscFeesBlock.value][0],
                                             'Check that allocation has negative fees')
        # endregion

        # region step 7 (check fix_confirmation message)
        list_of_ignored_fields = ['AllocQty', 'TransactTime', 'Side', 'AvgPx', 'QuodTradeQualifier',
                                  'BookID', 'SettlDate', 'OrderAvgPx', 'AllocID', 'Currency',
                                  'NetMoney', 'MatchStatus', 'ConfirmStatus', 'TradeDate',
                                  'NoParty', 'AllocInstructionMiscBlock1', 'tag5120',
                                  'ReportedPx', 'Instrument', 'GrossTradeAmt']
        no_misc_fee = [{'MiscFeeAmt': str(int(fee_amt)), 'MiscFeeCurr': self.currency, 'MiscFeeType': '1'}]
        list_of_ignored_fields.extend(['CpctyConfGrp', 'ConfirmID', 'ConfirmType', 'AllocAccount'])
        self.confirmation_report.change_parameters(
            {'NoOrders': [{'ClOrdID': cl_ord_id, 'OrderID': ord_id}],
             'ConfirmTransType': "0",
             'NoMiscFees': no_misc_fee,
             'CommissionData': {'CommissionType': '3',
                                'Commission': negative_value,
                                'CommCurrency': self.currency}})
        self.fix_verifier.check_fix_message_fix_standard(self.confirmation_report,
                                                         ignored_fields=list_of_ignored_fields)
        # endregion
