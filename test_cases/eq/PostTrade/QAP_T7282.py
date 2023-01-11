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
    JavaApiFields,
    ExecutionReportConst,
    OrderReplyConst,
    SubmitRequestConst,
)
from test_framework.java_api_wrappers.oms.ors_messges.AllocationInstructionOMS import AllocationInstructionOMS
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


class QAP_T7282(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        # region Declarations
        self.test_id = bca.create_event(os.path.basename(__file__)[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.qty = "40000000"
        self.qty_for_booking_first = "25000000"
        self.qty_for_booking_second = "15000000"
        self.price = "20"
        self.client = self.data_set.get_client("client_pt_1")  # MOClient
        self.java_api_connectivity = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.submit_request = OrderSubmitOMS(self.data_set)
        self.trade_request = TradeEntryOMS(self.data_set)
        self.complete_order = DFDManagementBatchOMS(self.data_set)
        self.allocation_instruction = AllocationInstructionOMS(self.data_set)
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

        # region Step 2 - Execute Care order
        self.trade_request.set_default_trade(ord_id, self.price, self.qty)
        responses = self.java_api_manager.send_message_and_receive_response(self.trade_request)
        print_message("TRADE", responses)
        exec_report = self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value).get_parameters()[
            JavaApiFields.ExecutionReportBlock.value
        ]
        self.java_api_manager.compare_values(
            {JavaApiFields.TransExecStatus.value: ExecutionReportConst.TransExecStatus_FIL.value},
            exec_report,
            "Comparing Execution status (TransExecStatus)",
        )
        # endregion

        # region Step 3 - Complete CO
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
        exec_report_reply = self.java_api_manager.get_last_message(
            ORSMessageType.ExecutionReport.value
        ).get_parameters()[JavaApiFields.ExecutionReportBlock.value]
        # endregion

        # region Step 1-3 - Open Split Book and Change rate of Commissions and Fees > Split Booking
        self.allocation_instruction.set_default_book(ord_id)
        self.allocation_instruction.update_fields_in_component(
            "AllocationInstructionBlock",
            {
                "AccountGroupID": self.client,
                "AllocationInstructionQtyList": {
                    "AllocationInstructionQtyBlock": [
                        {
                            "BookingQty": self.qty_for_booking_first,
                            "NetGrossInd": "Gross",
                            "BookingType": "RegularBooking",
                            "SettlDate": datetime.utcnow().isoformat(),
                            "GrossTradeAmt": "500000000",
                            "NetMoney": "500000000",
                        },
                        {
                            "BookingQty": self.qty_for_booking_second,
                            "NetGrossInd": "Gross",
                            "BookingType": "RegularBooking",
                            "SettlDate": datetime.utcnow().isoformat(),
                            "GrossTradeAmt": "300000000",
                            "NetMoney": "300000000",
                        },
                    ]
                },
                "Qty": self.qty,
                "GrossTradeAmt": "800000000",
                "AvgPx": "20",
                "SettlCurrAmt": "800000000",
            },
        )

        responses = self.java_api_manager.send_message_and_receive_response(self.allocation_instruction)
        print_message("BOOK", responses)

        # AllocationReport for 2nd block
        alloc_report_message_first = self.java_api_manager.get_last_message(
            ORSMessageType.AllocationReport.value, filter_value="'Qty': '1.5E7'"
        ).get_parameters()[JavaApiFields.AllocationReportBlock.value]
        self.java_api_manager.compare_values(
            {
                "Qty": "1.5E7",
                "AvgPrice": str(float(self.price)),
                JavaApiFields.AllocStatus.value: "APP",
                JavaApiFields.MatchStatus.value: "UNM",
            },
            alloc_report_message_first,
            f"Check that block created with Qty={self.qty_for_booking_second}",
        )

        # AllocationReport for 1st block
        alloc_report_message_second = self.java_api_manager.get_last_message(
            ORSMessageType.AllocationReport.value, filter_value="'Qty': '2.5E7'"
        ).get_parameters()[JavaApiFields.AllocationReportBlock.value]
        self.java_api_manager.compare_values(
            {
                "Qty": "2.5E7",
                "AvgPrice": str(float(self.price)),
                JavaApiFields.AllocStatus.value: "APP",
                JavaApiFields.MatchStatus.value: "UNM",
            },
            alloc_report_message_second,
            f"Check that block created with Qty={self.qty_for_booking_first}",
        )
        # endregion

        logger.info(f"Case {self.test_id} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")
