import logging
import os
from datetime import datetime
from pathlib import Path

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
)
from test_framework.java_api_wrappers.oms.es_messages.ExecutionReportOMS import ExecutionReportOMS
from test_framework.java_api_wrappers.oms.ors_messges.AllocationInstructionOMS import AllocationInstructionOMS
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

seconds, nanos = timestamps()  # Test case start time


def print_message(message, responses):
    logger.info(message)
    for i in responses:
        logger.info(i)
        logger.info(i.get_parameters())


class QAP_T10640(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(os.path.basename(__file__)[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.qty = "100"
        self.price = "20"
        self.price_amend = "25"
        self.client = self.data_set.get_client("client_pt_1")  # MOClient
        self.java_api_connectivity = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.order_submit = OrderSubmitOMS(data_set)
        self.allocation_instruction = AllocationInstructionOMS(self.data_set)
        self.execution_report = ExecutionReportOMS(self.data_set)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Step 1 - Create DMA order
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
        # endregion

        # region Step 1 - Trade DMA order and checking statuses
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
            "Step 1 - Comparing Statuses after Execute DMA",
        )
        # endregion

        # region Step 2 - Book order
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
            "Step 2 - Comparing PostTradeStatus after Book",
        )

        # Checking AllocationReportBlock
        alloc_report_reply = self.java_api_manager.get_last_message(
            ORSMessageType.AllocationReport.value
        ).get_parameters()[JavaApiFields.AllocationReportBlock.value]
        creation_time: str = alloc_report_reply["CreationTime"]  # Get the CreationTime of the block after booking
        alloc_instr_id = alloc_report_reply["AllocInstructionID"]
        exec_id = alloc_report_reply["ExecAllocList"]["ExecAllocBlock"][0]["ExecID"]

        self.java_api_manager.compare_values(
            {
                JavaApiFields.AllocStatus.value: "APP",
                JavaApiFields.MatchStatus.value: "UNM",
            },
            alloc_report_reply,
            "Step 2 - Comparing Status and Match Status in MO after Book",
        )
        # endregion

        # region Step 3 - Amend block
        self.allocation_instruction.set_amend_book(alloc_instr_id, exec_id, self.qty, self.price)
        self.allocation_instruction.update_fields_in_component(
            "AllocationInstructionBlock", {"GrossTradeAmt": "2500", "AvgPx": self.price_amend, "SettlCurrAmt": "2500"}
        )
        responses = self.java_api_manager.send_message_and_receive_response(self.allocation_instruction)
        print_message("AMEND BLOCK", responses)

        # Checking AllocationReportBlock
        alloc_report_reply_amend = self.java_api_manager.get_last_message(
            ORSMessageType.AllocationReport.value
        ).get_parameters()[JavaApiFields.AllocationReportBlock.value]
        self.java_api_manager.compare_values(
            {JavaApiFields.AvgPrice.value: str(float(self.price_amend)), "CreationTime": creation_time},
            alloc_report_reply_amend,
            "Step 3 - Comparing CreationTime and Price in MO after Amend",
        )
        # endregion

        logger.info(f"Case {self.test_id} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")
