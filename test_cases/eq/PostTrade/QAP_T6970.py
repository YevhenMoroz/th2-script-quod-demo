import logging
from datetime import datetime
from pathlib import Path

from custom import basic_custom_actions as bca
from custom.basic_custom_actions import timestamps
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, ExecutionReportConst, \
    AllocationInstructionConst
from test_framework.java_api_wrappers.oms.es_messages.ExecutionReportOMS import ExecutionReportOMS
from test_framework.java_api_wrappers.oms.ors_messges.AllocationInstructionOMS import AllocationInstructionOMS
from test_framework.java_api_wrappers.oms.ors_messges.ComputeBookingFeesCommissionsRequestOMS import \
    ComputeBookingFeesCommissionsRequestOMS
from test_framework.java_api_wrappers.oms.ors_messges.ConfirmationOMS import ConfirmationOMS
from test_framework.java_api_wrappers.oms.ors_messges.ForceAllocInstructionStatusRequestOMS import \
    ForceAllocInstructionStatusRequestOMS
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

seconds, nanos = timestamps()  # Test case start time


def print_message(message, responses):
    logger.info(message)
    for i in responses:
        logger.info(i)
        logger.info(i.get_parameters())


class QAP_T6970(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        # region Declarations
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.ss_connectivity = self.fix_env.sell_side
        self.bs_connectivity = self.fix_env.buy_side
        self.currency = self.data_set.get_currency_by_name('currency_5')
        self.qty = '100'
        self.price = '10'
        self.venue = self.data_set.get_mic_by_name('mic_1')  # XPAR
        self.client = self.data_set.get_client('client_pt_1')  # MOClient
        self.alloc_account = self.data_set.get_account_by_name('client_pt_1_acc_1')  # MOClient_SA1
        self.java_api_connectivity = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.order_submit = OrderSubmitOMS(data_set)
        self.allocation_instruction = AllocationInstructionOMS(self.data_set)
        self.execution_report = ExecutionReportOMS(self.data_set)
        self.approve_request = ForceAllocInstructionStatusRequestOMS(self.data_set)
        self.compute_booking_fees_commission_request = ComputeBookingFeesCommissionsRequestOMS(self.data_set)
        self.confirmation_request = ConfirmationOMS(self.data_set)

        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region precondition
        # part 1 (create dma order)
        self.order_submit.set_default_dma_limit()
        self.order_submit.update_fields_in_component(
            "NewOrderSingleBlock",
            {"OrdQty": self.qty,
             "AccountGroupID": self.client,
             "Price": self.price})
        responses = self.java_api_manager.send_message_and_receive_response(self.order_submit)
        print_message("Create Dma order", responses)
        order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value
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
        responses = self.java_api_manager.send_message_and_receive_response(self.execution_report)
        print_message("TRADE", responses)
        execution_report_message = self.java_api_manager.get_last_message(
            ORSMessageType.ExecutionReport.value
        ).get_parameters()[JavaApiFields.ExecutionReportBlock.value]
        self.java_api_manager.compare_values(
            {
                JavaApiFields.TransExecStatus.value: ExecutionReportConst.TransExecStatus_FIL.value,
                JavaApiFields.PostTradeStatus.value: "RDY",
            },
            execution_report_message,
            "Comparing Statuses after Execute DMA (part of precondition)",
        )
        exec_id = execution_report_message[JavaApiFields.ExecID.value]
        # end of part
        # endregion

        # region Book order (step 1 , step 2)
        rate = str(0.222)
        gross_trade_amt = float(self.qty) * float(self.price)
        self.allocation_instruction.set_default_book(ord_id)
        settl_dict = {JavaApiFields.SettlCurrency.value: self.currency,
                      JavaApiFields.SettlCurrFxRate.value: rate,
                      JavaApiFields.SettlCurrFxRateCalc.value: AllocationInstructionConst.SettlCurrFxRateCalc_D.value}
        self.allocation_instruction.update_fields_in_component('AllocationInstructionBlock', {
            "Qty": self.qty,
            "AvgPx": self.price,
            'GrossTradeAmt': str(gross_trade_amt),
        })
        self.allocation_instruction.update_fields_in_component('AllocationInstructionBlock', settl_dict)
        responses = self.java_api_manager.send_message_and_receive_response(self.allocation_instruction)
        print_message("Book order", responses)
        allocation_report = \
        self.java_api_manager.get_last_message(ORSMessageType.AllocationReport.value).get_parameters()[
            JavaApiFields.AllocationReportBlock.value]
        alloc_id = allocation_report[JavaApiFields.ClientAllocID.value]
        self.java_api_manager.compare_values(settl_dict, allocation_report,
                                             'Check expected and actually results from step 2')
        # endregion

        # region step 3 (Amend Block)
        self.allocation_instruction.set_amend_book(alloc_id, exec_id, self.qty, self.price)
        responses = self.java_api_manager.send_message_and_receive_response(self.allocation_instruction)
        print_message("Book order", responses)
        allocation_report = \
            self.java_api_manager.get_last_message(ORSMessageType.AllocationReport.value).get_parameters()[
                JavaApiFields.AllocationReportBlock.value]
        self.java_api_manager.compare_values(settl_dict, allocation_report,
                                             'Check expected and actually results from step 2')
        # endregion

        # region step 4 and step 5 (approve block)
        # part 1 - Approve block
        self.approve_request.set_default_approve(alloc_id)
        responses = self.java_api_manager.send_message_and_receive_response(self.allocation_instruction)
        print_message("Approve block", responses)
        # end of part

        # part 2 - Allocate block
        self.confirmation_request.set_default_allocation(alloc_id)
        self.confirmation_request.update_fields_in_component("ConfirmationBlock", {
            "AllocAccountID": self.alloc_account,
            "AllocQty": self.qty,
            "AvgPx": self.price})
        responses = self.java_api_manager.send_message_and_receive_response(self.confirmation_request)
        print_message('Allocate block', responses)
        allocation_report = \
            self.java_api_manager.get_last_message(ORSMessageType.AllocationReport.value).get_parameters()[
                JavaApiFields.AllocationReportBlock.value]
        confirmation_report = \
            self.java_api_manager.get_last_message(ORSMessageType.ConfirmationReport.value).get_parameters()[
                JavaApiFields.ConfirmationReportBlock.value]
        self.java_api_manager.compare_values(settl_dict, allocation_report,
                                             'Check expected and actually results from step 5 (concerning block)')
        self.java_api_manager.compare_values(settl_dict, confirmation_report,
                                             'Check expected and actually results from step 5 (concerning allocation)')
        # end of part
        # endregion
        logger.info(f"Case {self.test_id} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")
