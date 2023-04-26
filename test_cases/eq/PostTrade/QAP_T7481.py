import logging
import time
from datetime import datetime
from pathlib import Path

from custom import basic_custom_actions as bca
from custom.basic_custom_actions import timestamps
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, OrderReplyConst, ExecutionReportConst, \
    AllocationInstructionConst, AllocationReportConst, ConfirmationReportConst
from test_framework.java_api_wrappers.oms.es_messages.ExecutionReportOMS import ExecutionReportOMS
from test_framework.java_api_wrappers.oms.ors_messges.AllocationInstructionOMS import AllocationInstructionOMS
from test_framework.java_api_wrappers.oms.ors_messges.ComputeBookingFeesCommissionsRequestOMS import \
    ComputeBookingFeesCommissionsRequestOMS
from test_framework.java_api_wrappers.oms.ors_messges.ConfirmationOMS import ConfirmationOMS
from test_framework.java_api_wrappers.oms.ors_messges.ForceAllocInstructionStatusRequestOMS import \
    ForceAllocInstructionStatusRequestOMS
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.java_api_wrappers.ors_messages.BlockUnallocateRequest import BlockUnallocateRequest
from test_framework.read_log_wrappers.ReadLogVerifier import ReadLogVerifier
from test_framework.read_log_wrappers.oms_messages.AlsMessages import AlsMessages

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

seconds, nanos = timestamps()  # Test case start time


class QAP_T7481(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        # region Declarations
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.ss_connectivity = self.fix_env.sell_side
        self.bs_connectivity = self.fix_env.buy_side
        self.qty = "200"
        self.price = "20"
        self.rule_manager = RuleManager(sim=Simulators.equity)
        self.venue_client_names = self.data_set.get_venue_client_names_by_name("client_pt_2_venue_1")  # MOClient2_PARIS
        self.venue = self.data_set.get_mic_by_name("mic_1")  # XPAR
        self.client = self.data_set.get_client("client_pt_1")  # MOClient2
        self.currency = self.data_set.get_currency_by_name('currency_1')
        self.alloc_account_1 = self.data_set.get_account_by_name("client_pt_1_acc_1")  # MOClient2_SA1
        self.alloc_account_2 = self.data_set.get_account_by_name("client_pt_1_acc_2")  # MOClient2_SA2
        self.java_api_connectivity = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.order_submit = OrderSubmitOMS(data_set)
        self.allocation_instruction = AllocationInstructionOMS(self.data_set)
        self.execution_report = ExecutionReportOMS(self.data_set)
        self.compute_booking_fees_commission_request = ComputeBookingFeesCommissionsRequestOMS(self.data_set)
        self.confirmation_request = ConfirmationOMS(self.data_set)
        self.approve_message = ForceAllocInstructionStatusRequestOMS(self.data_set)
        self.als_email_report = self.environment.get_list_read_log_environment()[0].read_log_conn
        self.read_log_verifier = ReadLogVerifier(self.als_email_report, self.test_id)
        self.unallocate_request = BlockUnallocateRequest()
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region precondition

        # part 1 : Create DMA order
        self.order_submit.set_default_dma_limit()
        self.order_submit.update_fields_in_component(
            "NewOrderSingleBlock",
            {"OrdQty": self.qty,
             "AccountGroupID": self.client,
             "Price": self.price})
        self.java_api_manager.send_message_and_receive_response(self.order_submit)
        order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdNotification.value).get_parameters()[
            JavaApiFields.OrderNotificationBlock.value
        ]
        ord_id = order_reply["OrdID"]
        # end of part

        # part 2 (trade dma order)
        self.execution_report.set_default_trade(ord_id)
        self.execution_report.update_fields_in_component(
            "ExecutionReportBlock",
            {
                "Price": self.price,
                "AvgPrice": self.price,
                "LastPx": self.price,
                "OrdQty": self.qty,
                "LastTradedQty": self.qty,
                "CumQty": self.qty,
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

        # region step 1 and step 2
        gross_trade_amt = float(self.price) * float(self.qty)
        self.allocation_instruction.set_default_book(ord_id)
        rate_of_commission = 21
        client_comm = {JavaApiFields.CommissionCurrency.value: self.currency,
                       JavaApiFields.CommissionBasis.value: AllocationInstructionConst.COMM_AND_FEE_BASIS_ABS.value,
                       JavaApiFields.CommissionRate.value: str(rate_of_commission),
                       JavaApiFields.CommissionAmount.value: str(rate_of_commission),
                       JavaApiFields.CommissionAmountType.value: AllocationInstructionConst.CommissionAmountType_BRK.value,
                       JavaApiFields.CommissionAmountSubType.value: AllocationInstructionConst.CommissionAmountSubType_OTH.value}
        self.allocation_instruction.update_fields_in_component('AllocationInstructionBlock',
                                                               {"Qty": self.qty,
                                                                "AvgPx": self.price,
                                                                'GrossTradeAmt': str(gross_trade_amt),
                                                                "SettlCurrAmt": str(gross_trade_amt + float(21)),
                                                                'ExecAllocList': {
                                                                    'ExecAllocBlock': [{'ExecQty': self.qty,
                                                                                        'ExecID': exec_id,
                                                                                        'ExecPrice': self.price}]},
                                                                JavaApiFields.ClientCommissionList.value: {
                                                                    JavaApiFields.ClientCommissionBlock.value: [
                                                                        client_comm
                                                                    ]}
                                                                })
        self.java_api_manager.send_message_and_receive_response(self.allocation_instruction, response_time=10000)
        allocation_report = \
            self.java_api_manager.get_last_message(ORSMessageType.AllocationReport.value).get_parameters()[
                JavaApiFields.AllocationReportBlock.value]
        order_update = self.java_api_manager.get_last_message(ORSMessageType.OrdUpdate.value).get_parameters()[
            JavaApiFields.OrdUpdateBlock.value]
        alloc_id = allocation_report[JavaApiFields.ClientAllocID.value]
        alloc_instr_id = allocation_report[JavaApiFields.ClBookingRefID.value]
        self.java_api_manager.compare_values(
            {JavaApiFields.AllocStatus.value: AllocationReportConst.AllocStatus_APP.value,
             JavaApiFields.MatchStatus.value: ConfirmationReportConst.MatchStatus_UNM.value},
            allocation_report,
            'Check expected and actually results for block (step 2)')
        self.java_api_manager.compare_values(
            {JavaApiFields.PostTradeStatus.value: OrderReplyConst.PostTradeStatus_BKD.value},
            order_update, 'Check expected and actually result for order (step 2)')
        # endregion

        # region step 3
        self.approve_message.set_default_approve(alloc_id)
        self.java_api_manager.send_message_and_receive_response(self.approve_message, response_time=12000)
        allocation_report = \
            self.java_api_manager.get_last_message(ORSMessageType.AllocationReport.value).get_parameters()[
                JavaApiFields.AllocationReportBlock.value]
        self.java_api_manager.compare_values(
            {JavaApiFields.AllocStatus.value: AllocationReportConst.AllocStatus_ACK.value,
             JavaApiFields.MatchStatus.value: AllocationReportConst.MatchStatus_MAT.value},
            allocation_report,
            'Check expected and actually results (step 3)')
        # endregion

        # region step 4 and step 5
        list_of_account = [self.alloc_account_1, self.alloc_account_2]
        for account in list_of_account:
            self.confirmation_request.set_default_allocation(alloc_id)
            self.confirmation_request.update_fields_in_component('ConfirmationBlock',
                                                                 {"AllocQty": str(float(self.qty) / 2),
                                                                  "Side": "B",
                                                                  "AvgPx": self.price,
                                                                  "AllocAccountID": account})
            self.java_api_manager.send_message_and_receive_response(self.confirmation_request)
        # endregion

        # region step 6 Check ALS logs Status New
        als_message = AlsMessages.execution_report.value
        trade_date = datetime.now().strftime('%Y-%m-%d')
        als_message.update({"ConfirmStatus": "New", "ClientAccountID": self.alloc_account_1, "AllocQty": "100",
                            'TradeDate': trade_date})
        self.read_log_verifier.check_read_log_message(als_message, ["ConfirmStatus", 'ClientAccountID', 'TradeDate'],
                                                      timeout=100000)
        # endregion

        # region step 7 (unallocate block)
        time.sleep(3)
        self.unallocate_request.set_default(alloc_id)
        self.java_api_manager.send_message_and_receive_response(self.unallocate_request)
        allocation_report = \
            self.java_api_manager.get_last_message(ORSMessageType.AllocationReport.value).get_parameters()[
                JavaApiFields.AllocationReportBlock.value]
        self.java_api_manager.compare_values(
            {JavaApiFields.AllocStatus.value: AllocationReportConst.AllocStatus_ACK.value,
             JavaApiFields.MatchStatus.value: AllocationReportConst.MatchStatus_MAT.value},
            allocation_report,
            'Check expected and actually results (part of step 7)')
        alloc_summary_status_is_absent = not JavaApiFields.AllocSummaryStatus.value in allocation_report
        self.java_api_manager.compare_values({'AllocSummaryStatusIsAbsent': True},
                                             {'AllocSummaryStatusIsAbsent': alloc_summary_status_is_absent},
                                             f'Check that {JavaApiFields.AllocSummaryStatus.value}'
                                             f' is empty (part of step 7)')
        # endregion

        # region step 8 Check ALS logs Status Canceled
        als_message.update({"ConfirmStatus": "Cancel"})
        self.read_log_verifier.check_read_log_message(als_message, ["ConfirmStatus", 'ClientAccountID', 'TradeDate'],
                                                      timeout=10000)
        time.sleep(10)
        # endregion

        logger.info(f"Case {self.test_id} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")
