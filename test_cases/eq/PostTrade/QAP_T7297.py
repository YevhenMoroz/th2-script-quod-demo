import logging
from datetime import datetime, timedelta
from pathlib import Path

from pandas import Timestamp as tm

from custom import basic_custom_actions as bca
from custom.basic_custom_actions import timestamps
from datetime import timezone
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import (
    SubmitRequestConst,
    OrderReplyConst,
    JavaApiFields,
    ExecutionReportConst,
    ConfirmationReportConst,
    AllocationReportConst,
)
from test_framework.java_api_wrappers.oms.ors_messges.AllocationInstructionOMS import AllocationInstructionOMS
from test_framework.java_api_wrappers.oms.ors_messges.ConfirmationOMS import ConfirmationOMS
from test_framework.java_api_wrappers.oms.ors_messges.DFDManagementBatchOMS import DFDManagementBatchOMS
from test_framework.java_api_wrappers.oms.ors_messges.ForceAllocInstructionStatusRequestOMS import (
    ForceAllocInstructionStatusRequestOMS,
)
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.java_api_wrappers.oms.ors_messges.TradeEntryOMS import TradeEntryOMS

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

seconds, nanos = timestamps()  # Test case start time


def print_message(message, responses):
    logger.info(message)
    for i in responses:
        logger.info(i)
        logger.info(i.get_parameters())


class QAP_T7297(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        # region Declarations
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.qty = "100"
        self.price = "20"
        self.client = self.data_set.get_client("client_pt_1")  # MOClient
        self.alloc_account = self.data_set.get_account_by_name("client_pt_1_acc_1")  # MOClient_SA1
        self.java_api_connectivity = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.submit_request = OrderSubmitOMS(self.data_set)
        self.trade_request = TradeEntryOMS(self.data_set)
        self.complete_order = DFDManagementBatchOMS(self.data_set)
        self.allocation_instruction = AllocationInstructionOMS(self.data_set)
        self.approve_request = ForceAllocInstructionStatusRequestOMS(self.data_set)
        self.confirmation_request = ConfirmationOMS(self.data_set)
        self.settl_date = (
            (tm(datetime.now(timezone.utc).isoformat()) + timedelta(days=2)).date().strftime("%Y-%m-%dT%H:%M:%S")
        )
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Step 1 - Create CO order
        self.submit_request.set_default_care_limit(
            recipient=self.environment.get_list_fe_environment()[0].user_1,
            desk=self.environment.get_list_fe_environment()[0].desk_ids[0],
            role=SubmitRequestConst.USER_ROLE_1.value,
        )
        self.submit_request.update_fields_in_component(
            "NewOrderSingleBlock",
            {"OrdQty": self.qty, "Price": self.price, "SettlDate": self.settl_date},
        )
        responses = self.java_api_manager.send_message_and_receive_response(self.submit_request)
        print_message("CREATE", responses)
        order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value
        ]
        ord_id = order_reply["OrdID"]
        cl_ord_id = order_reply["ClOrdID"]
        settl_date_expected = datetime.strftime(datetime.now() + timedelta(days=2), "%Y-%m-%d") + "T12:00"
        self.java_api_manager.compare_values(
            {JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_OPN.value, "SettlDate": settl_date_expected},
            order_reply,
            "Comparing Status and SettlDate of Care order",
        )
        # endregion

        # region Step 2 - Child Care CO
        self.submit_request.set_default_child_care(
            parent_id=ord_id,
            desk=self.environment.get_list_fe_environment()[0].desk_ids[0],
            recipient=self.environment.get_list_fe_environment()[0].user_1,
            role=SubmitRequestConst.USER_ROLE_1.value,
        )
        self.submit_request.update_fields_in_component(
            "NewOrderSingleBlock",
            {
                "SettlDate": (tm(datetime.now(timezone.utc).isoformat()) + timedelta(days=3))
                .date()
                .strftime("%Y-%m-%dT%H:%M:%S")
            },
        )

        responses = self.java_api_manager.send_message_and_receive_response(self.submit_request)
        print_message("CHILD CARE", responses)
        order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value
        ]
        ord_id_child = order_reply["OrdID"]
        settl_date_expected = datetime.strftime(datetime.now() + timedelta(days=3), "%Y-%m-%d") + "T12:00"
        self.java_api_manager.compare_values(
            {
                JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_OPN.value,
                "SettlDate": settl_date_expected,
            },
            order_reply,
            "Comparing Status and SettlDate of Child Care order",
        )
        # endregion

        # region Step 3 - Execute Child Care order
        self.trade_request.set_default_trade(ord_id_child, self.price, self.qty)
        self.trade_request.update_fields_in_component(
            "TradeEntryRequestBlock",
            {
                "SettlDate": (tm(datetime.now(timezone.utc).isoformat()) + timedelta(days=4))
                .date()
                .strftime("%Y-%m-%dT%H:%M:%S")
            },
        )

        responses = self.java_api_manager.send_message_and_receive_response(self.trade_request)
        print_message("Execute Child Care", responses)
        exec_report = self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value).get_parameters()[
            JavaApiFields.ExecutionReportBlock.value
        ]
        settl_date_expected = datetime.strftime(datetime.now() + timedelta(days=4), "%Y-%m-%d") + "T12:00"
        self.java_api_manager.compare_values(
            {
                JavaApiFields.TransExecStatus.value: ExecutionReportConst.TransExecStatus_FIL.value,
                "SettlDate": settl_date_expected,
            },
            exec_report,
            "Comparing Execution status (TransExecStatus) and SettlDate",
        )
        settl_date_extract = exec_report["SettlDate"]  # SettlDate for Book
        # endregion

        # region Step 4 - Complete CO
        self.complete_order.set_default_complete(ord_id)
        responses = self.java_api_manager.send_message_and_receive_response(self.complete_order)
        print_message("COMPLETE", responses)
        order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value
        ]
        self.java_api_manager.compare_values(
            {
                JavaApiFields.PostTradeStatus.value: OrderReplyConst.PostTradeStatus_RDY.value,
                JavaApiFields.DoneForDay.value: OrderReplyConst.DoneForDay_YES.value,
            },
            order_reply,
            "Comparing PostTradeStatus after Complete",
        )
        # endregion

        # region Step 4 - Book order
        self.allocation_instruction.set_default_book(ord_id)
        self.allocation_instruction.update_fields_in_component(
            "AllocationInstructionBlock",
            {
                "Qty": self.qty,
                "AccountGroupID": self.client,
                "GrossTradeAmt": "2000",
                "AvgPx": self.price,
                "SettlCurrAmt": "2000",
                "SettlDate": settl_date_extract,
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
            ORSMessageType.AllocationReport.value, JavaApiFields.BookingAllocInstructionID.value
        ).get_parameters()[JavaApiFields.AllocationReportBlock.value]
        alloc_id = alloc_report_reply["ClientAllocID"]
        self.java_api_manager.compare_values(
            {
                JavaApiFields.AllocStatus.value: "APP",
                JavaApiFields.MatchStatus.value: "UNM",
                "SettlDate": settl_date_expected,
            },
            alloc_report_reply,
            "Comparing SettlDate and Statuses after Book",
        )
        # endregion

        # region Step 5 - Approve
        self.approve_request.set_default_approve(alloc_id)
        responses = self.java_api_manager.send_message_and_receive_response(self.approve_request)
        print_message("APPROVE", responses)

        # Checking Order_AllocationReport
        alloc_report_reply = self.java_api_manager.get_last_message(
            ORSMessageType.AllocationReport.value
        ).get_parameters()[JavaApiFields.AllocationReportBlock.value]
        self.java_api_manager.compare_values(
            {
                JavaApiFields.AllocStatus.value: "ACK",
                JavaApiFields.MatchStatus.value: "MAT",
                "SettlDate": settl_date_expected,
            },
            alloc_report_reply,
            "Comparing Statuses and SettlDate after Approve",
        )
        # endregion

        # region Step 5 - Allocate block
        self.confirmation_request.set_default_allocation(alloc_id)
        self.confirmation_request.update_fields_in_component(
            "ConfirmationBlock",
            {
                "AllocAccountID": self.alloc_account,
                "AllocQty": self.qty,
                "AvgPx": self.price,
            },
        )
        responses = self.java_api_manager.send_message_and_receive_response(self.confirmation_request)
        print_message("ALLOCATE", responses)

        # Comparing values for Allocation after Allocate block
        conf_report_message = self.java_api_manager.get_last_message(
            ORSMessageType.ConfirmationReport.value
        ).get_parameters()["ConfirmationReportBlock"]
        self.java_api_manager.compare_values(
            {
                "AffirmStatus": ConfirmationReportConst.ConfirmStatus_AFF.value,
                "MatchStatus": ConfirmationReportConst.MatchStatus_MAT.value,
                "SettlDate": settl_date_expected,
            },
            conf_report_message,
            "Comparing Statuses and SettlDate for Allocation after Allocate block",
        )

        # Comparing statuses for Block after Allocate block
        allocation_report_message = self.java_api_manager.get_last_message(
            ORSMessageType.AllocationReport.value
        ).get_parameters()["AllocationReportBlock"]
        self.java_api_manager.compare_values(
            {
                "AllocStatus": AllocationReportConst.AllocStatus_ACK.value,
                "MatchStatus": AllocationReportConst.MatchStatus_MAT.value,
                "AllocSummaryStatus": AllocationReportConst.AllocSummaryStatus_MAG.value,
            },
            allocation_report_message,
            "Comparing statuses for Block after Allocate block",
        )
        # endregion

        logger.info(f"Case {self.test_id} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")
