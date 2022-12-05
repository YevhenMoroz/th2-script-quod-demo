import logging
from datetime import datetime
from pathlib import Path

from custom import basic_custom_actions as bca
from custom.basic_custom_actions import timestamps
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import (
    SubmitRequestConst,
    JavaApiFields,
    OrderReplyConst,
    ExecutionReportConst,
)
from test_framework.java_api_wrappers.oms.ors_messges.AllocationInstructionOMS import AllocationInstructionOMS
from test_framework.java_api_wrappers.oms.ors_messges.ComputeBookingFeesCommissionsRequestOMS import (
    ComputeBookingFeesCommissionsRequestOMS,
)
from test_framework.java_api_wrappers.oms.ors_messges.DFDManagementBatchOMS import DFDManagementBatchOMS
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


class QAP_T7306(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        # region Declarations
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.qty = "100"
        self.price = "20"
        self.client = self.data_set.get_client("client_pt_1")  # MOClient
        self.java_api_connectivity = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.submit_request = OrderSubmitOMS(self.data_set)
        self.trade_request = TradeEntryOMS(self.data_set)
        self.complete_order = DFDManagementBatchOMS(self.data_set)
        self.allocation_instruction = AllocationInstructionOMS(self.data_set)
        self.compute_request = ComputeBookingFeesCommissionsRequestOMS(self.data_set)
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
            {
                "OrdQty": self.qty,
                "Price": self.price,
            },
        )
        responses = self.java_api_manager.send_message_and_receive_response(self.submit_request)
        print_message("CREATE", responses)
        order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value
        ]
        ord_id = order_reply["OrdID"]
        cl_ord_id = order_reply["ClOrdID"]
        self.java_api_manager.compare_values(
            {JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_OPN.value},
            order_reply,
            "Comparing Status of Care order",
        )
        # endregion

        # region Step 2 - Do 2 Executions for CO order
        self.trade_request.set_default_trade(ord_id, self.price, str(int(self.qty) / 2))
        responses = self.java_api_manager.send_message_and_receive_response(self.trade_request)
        print_message("TRADE", responses)
        exec_report = self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value).get_parameters()[
            JavaApiFields.ExecutionReportBlock.value
        ]
        exec_id_first: str = exec_report["ExecID"]
        self.java_api_manager.compare_values(
            {JavaApiFields.TransExecStatus.value: ExecutionReportConst.TransExecStatus_PFL.value},
            exec_report,
            "Comparing Execution status (TransExecStatus) after first execution",
        )

        self.trade_request.set_default_trade(ord_id, self.price, str(int(self.qty) / 2))
        responses = self.java_api_manager.send_message_and_receive_response(self.trade_request)
        print_message("TRADE", responses)
        exec_report = self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value).get_parameters()[
            JavaApiFields.ExecutionReportBlock.value
        ]
        exec_id_second: str = exec_report["ExecID"]
        self.java_api_manager.compare_values(
            {JavaApiFields.TransExecStatus.value: ExecutionReportConst.TransExecStatus_FIL.value},
            exec_report,
            "Comparing Execution status (TransExecStatus) after second execution",
        )
        # endregion

        # region Step 3 - Cancel 1 Execution of Care order
        self.trade_request.set_default_trade(ord_id, 0, 0)
        self.trade_request.update_fields_in_component(
            "TradeEntryRequestBlock", {"TradeEntryTransType": "Cancel", "ExecRefID": exec_id_second}
        )
        responses = self.java_api_manager.send_message_and_receive_response(self.trade_request)
        print_message("CANCEL SECOND EXECUTION", responses)
        exec_report = self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value).get_parameters()[
            JavaApiFields.ExecutionReportBlock.value
        ]
        self.java_api_manager.compare_values(
            {
                JavaApiFields.TransExecStatus.value: ExecutionReportConst.TransExecStatus_PFL.value,
                "LeavesQty": str(float(self.qty) / 2),
            },
            exec_report,
            "Comparing Execution status (TransExecStatus)",
        )
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
        post_trd_sts = order_reply["PostTradeStatus"]
        exec_report_reply = self.java_api_manager.get_last_message(
            ORSMessageType.ExecutionReport.value
        ).get_parameters()[JavaApiFields.ExecutionReportBlock.value]
        exec_id_calculated: str = exec_report_reply["ExecID"]
        # endregion

        # region Step 4,5 - Open Booking ticket
        self.compute_request.set_list_of_order_alloc_block(cl_ord_id, ord_id, post_trd_sts)
        self.compute_request.set_list_of_exec_alloc_block(
            str(float(self.qty) / 2), exec_id_first, self.price, post_trd_sts
        )
        self.compute_request.set_default_compute_booking_request(qty=str(float(self.qty) / 2), client=self.client)
        self.compute_request.update_fields_in_component(
            "ComputeBookingFeesCommissionsRequestBlock",
            {
                "CalculatedExecList": {
                    "ExecAllocBlock": [
                        {
                            "ExecQty": str(float(self.qty) / 2),
                            "ExecID": exec_id_calculated,
                            "ExecPrice": self.price,
                            "PostTradeExecStatus": "ReadyToBook",
                        }
                    ]
                }
            },
        )
        responses = self.java_api_manager.send_message_and_receive_response(self.compute_request)
        print_message("OPEN BOOKING TICKET", responses)
        # endregion

        # region Step 6 - Book order
        self.allocation_instruction.set_default_book(ord_id)
        self.allocation_instruction.update_fields_in_component(
            "AllocationInstructionBlock",
            {
                "Qty": str(float(self.qty) / 2),
                "AccountGroupID": self.client,
                "GrossTradeAmt": "1000",
                "AvgPx": self.price,
                "SettlCurrAmt": "1000",
                "ExecAllocList": {
                    "ExecAllocBlock": [
                        {"ExecQty": str(float(self.qty) / 2), "ExecID": exec_id_first, "ExecPrice": self.price}
                    ]
                },
                "CalculatedExecList": {
                    "ExecAllocBlock": [{"ExecQty": str(float(self.qty) / 2), "ExecID": exec_id_calculated}]
                },
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
        alloc_id = alloc_report_reply["ClientAllocID"]
        self.java_api_manager.compare_values(
            {
                JavaApiFields.AllocStatus.value: "APP",
                JavaApiFields.MatchStatus.value: "UNM",
                "Qty": str(float(self.qty) / 2),
            },
            alloc_report_reply,
            "Comparing Statuses and Qty in MO after Book",
        )
        # endregion

        logger.info(f"Case {self.test_id} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")
