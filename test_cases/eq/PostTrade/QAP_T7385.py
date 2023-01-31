import logging
import os
from datetime import datetime
from datetime import timezone
from pathlib import Path

from pandas import Timestamp as tm

from custom import basic_custom_actions as bca
from custom.basic_custom_actions import timestamps
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import (
    OrderReplyConst,
    JavaApiFields,
    ExecutionReportConst,
    ConfirmationReportConst,
    AllocationReportConst,
)
from test_framework.java_api_wrappers.oms.es_messages.ExecutionReportOMS import ExecutionReportOMS
from test_framework.java_api_wrappers.oms.ors_messges.AllocationInstructionOMS import AllocationInstructionOMS
from test_framework.java_api_wrappers.oms.ors_messges.ConfirmationOMS import ConfirmationOMS
from test_framework.java_api_wrappers.oms.ors_messges.ForceAllocInstructionStatusRequestOMS import (
    ForceAllocInstructionStatusRequestOMS,
)
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

seconds, nanos = timestamps()  # Test case start time


def print_message(message, responses):
    logger.info(message)
    for i in responses:
        logger.info(i)
        logger.info(i.get_parameters())


class QAP_T7385(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(os.path.basename(__file__)[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.qty = "100"
        self.price = "20"
        self.client = self.data_set.get_client("client_pt_1")  # MOClient
        self.alloc_account = self.data_set.get_account_by_name("client_pt_1_acc_1")  # MOClient_SA1
        self.java_api_connectivity = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.order_submit = OrderSubmitOMS(data_set)
        self.allocation_instruction = AllocationInstructionOMS(self.data_set)
        self.execution_report = ExecutionReportOMS(self.data_set)
        self.approve_request = ForceAllocInstructionStatusRequestOMS(self.data_set)
        self.confirmation_request = ConfirmationOMS(self.data_set)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Precondition - Create DMA order
        self.order_submit.set_default_dma_limit()
        self.order_submit.update_fields_in_component(
            "NewOrderSingleBlock",
            {
                "OrdQty": self.qty,
                "AccountGroupID": self.client,
                "Price": self.price,
            },
        )
        responses = self.java_api_manager.send_message_and_receive_response(self.order_submit)
        print_message("CREATE", responses)
        order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value
        ]
        ord_id = order_reply["OrdID"]
        self.java_api_manager.compare_values(
            {JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_SEN.value},
            order_reply,
            "Comparing Status of DMA order",
        )
        # endregion

        # region Precondition - Trade DMA order and checking statuses
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
                "TransactTime": tm(datetime.now(timezone.utc).isoformat()).date().strftime("%Y-%m-%dT%H:%M:%S"),
            },
        )

        # Checking Order_ExecutionReport
        responses = self.java_api_manager.send_message_and_receive_response(self.execution_report)
        print_message("TRADE", responses)
        execution_report_message = self.java_api_manager.get_last_message(
            ORSMessageType.ExecutionReport.value
        ).get_parameters()[JavaApiFields.ExecutionReportBlock.value]
        self.java_api_manager.compare_values(
            {
                JavaApiFields.TransExecStatus.value: ExecutionReportConst.TransExecStatus_FIL.value,
                JavaApiFields.TransStatus.value: "TER",
                JavaApiFields.PostTradeStatus.value: "RDY",
            },
            execution_report_message,
            "Comparing Statuses after Execute DMA",
        )
        # endregion

        # region Step 1,2 - Book order
        self.allocation_instruction.set_default_book(ord_id)
        self.allocation_instruction.update_fields_in_component(
            "AllocationInstructionBlock",
            {
                "Qty": self.qty,
                "AccountGroupID": self.client,
                "GrossTradeAmt": "2000",
                "AvgPx": self.price,
                "SettlCurrAmt": "2000",
            },
        )

        responses = self.java_api_manager.send_message_and_receive_response(self.allocation_instruction)
        print_message("BOOK", responses)

        # Checking Order_OrdUpdate
        order_update_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdUpdate.value).get_parameters()[
            JavaApiFields.OrdUpdateBlock.value
        ]
        self.java_api_manager.compare_values(
            {JavaApiFields.PostTradeStatus.value: OrderReplyConst.PostTradeStatus_BKD.value},
            order_update_reply,
            "Comparing PostTradeStatus after Book",
        )

        # Checking AllocationReportBlock
        alloc_report_reply = self.java_api_manager.get_last_message(
            ORSMessageType.AllocationReport.value
        ).get_parameters()[JavaApiFields.AllocationReportBlock.value]
        alloc_id: str = alloc_report_reply["ClientAllocID"]
        trade_date_block: str = alloc_report_reply["TradeDate"]  # Get TradeDate for the block
        trade_date_expected = datetime.strftime(datetime.now(), "%Y-%m-%d") + "T12:00"
        self.java_api_manager.compare_values(
            {
                JavaApiFields.AllocStatus.value: "APP",
                JavaApiFields.MatchStatus.value: "UNM",
                "TradeDate": trade_date_expected,
            },
            alloc_report_reply,
            "Comparing Status and Match Status in MO after auto Book",
        )
        # endregion

        # region Step 3 - Approve
        self.approve_request.set_default_approve(alloc_id)
        responses = self.java_api_manager.send_message_and_receive_response(self.approve_request)
        print_message("APPROVE", responses)

        # Checking Order_AllocationReport
        alloc_report_reply = self.java_api_manager.get_last_message(
            ORSMessageType.AllocationReport.value
        ).get_parameters()[JavaApiFields.AllocationReportBlock.value]
        self.java_api_manager.compare_values(
            {JavaApiFields.AllocStatus.value: "ACK", JavaApiFields.MatchStatus.value: "MAT"},
            alloc_report_reply,
            "Comparing Status and Match Status after Approve",
        )
        # endregion

        # region Step 4,5 - Allocate block
        self.confirmation_request.set_default_allocation(alloc_id)
        self.confirmation_request.update_fields_in_component(
            "ConfirmationBlock",
            {
                "AllocAccountID": self.alloc_account,
                "AllocQty": self.qty,
                "AvgPx": "20",
            },
        )
        responses = self.java_api_manager.send_message_and_receive_response(self.confirmation_request)
        print_message("ALLOCATE", responses)

        # Comparing values for Allocation after Allocate block
        conf_report_message = self.java_api_manager.get_last_message(
            ORSMessageType.ConfirmationReport.value
        ).get_parameters()["ConfirmationReportBlock"]
        trade_date_alloc: str = conf_report_message["TradeDate"]  # Get TradeDate for the allocation
        self.java_api_manager.compare_values(
            {
                JavaApiFields.AffirmStatus.value: ConfirmationReportConst.AffirmStatus_AFF.value,
                JavaApiFields.MatchStatus.value: ConfirmationReportConst.MatchStatus_MAT.value,
                "AllocAccountID": self.alloc_account,
                "AllocQty": str(float(self.qty)),
                "TradeDate": trade_date_expected,
            },
            conf_report_message,
            "Comparing values for Allocation after Allocate block",
        )

        # Comparing statuses for Block after Allocate block
        allocation_report_message = self.java_api_manager.get_last_message(
            ORSMessageType.AllocationReport.value
        ).get_parameters()["AllocationReportBlock"]
        self.java_api_manager.compare_values(
            {
                JavaApiFields.AllocStatus.value: AllocationReportConst.AllocStatus_ACK.value,
                JavaApiFields.MatchStatus.value: AllocationReportConst.MatchStatus_MAT.value,
                JavaApiFields.AllocSummaryStatus.value: AllocationReportConst.AllocSummaryStatus_MAG.value,
            },
            allocation_report_message,
            "Comparing statuses for Block after Allocate block",
        )
        # endregion

        # region Step 6 - Comparing TradeDate between the Block and Allocation
        self.java_api_manager.compare_values(
            {"TradeDate": trade_date_block},
            {"TradeDate": trade_date_alloc},
            "Comparing TradeDate between the Block and Allocation",
        )
        # endregion

        logger.info(f"Case {self.test_id} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")
