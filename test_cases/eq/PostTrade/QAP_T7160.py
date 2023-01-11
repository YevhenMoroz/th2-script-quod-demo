import logging
from datetime import datetime
from pathlib import Path

from custom import basic_custom_actions as bca
from custom.basic_custom_actions import timestamps
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import (
    OrderReplyConst,
    JavaApiFields,
    ExecutionReportConst,
    AllocationReportConst,
)
from test_framework.java_api_wrappers.oms.ors_messges.AllocationInstructionOMS import AllocationInstructionOMS
from test_framework.java_api_wrappers.oms.ors_messges.DFDManagementBatchOMS import DFDManagementBatchOMS
from test_framework.java_api_wrappers.oms.ors_messges.TradeEntryOMS import TradeEntryOMS
from test_framework.java_api_wrappers.ors_messages.BlockChangeConfirmationServiceRequest import (
    BlockChangeConfirmationServiceRequest,
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

seconds, nanos = timestamps()  # Test case start time


def print_message(message, responses):
    logger.info(message)
    for i in responses:
        logger.info(i)
        logger.info(i.get_parameters())


class QAP_T7160(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.ss_connectivity = self.fix_env.sell_side
        self.bs_connectivity = self.fix_env.buy_side
        self.fix_manager = FixManager(self.ss_connectivity, self.test_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set)
        self.client = self.data_set.get_client_by_name("client_pt_11")  # MOClient8
        # self.client = "MOClient9"
        self.qty = "100"
        self.price = "20"
        self.java_api_connectivity = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.trade_request = TradeEntryOMS(self.data_set)
        self.complete_request = DFDManagementBatchOMS(self.data_set)
        self.allocation_instruction = AllocationInstructionOMS(self.data_set)
        self.change_confirmation_service_request = BlockChangeConfirmationServiceRequest()

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Create CO order via FIX
        self.fix_message.set_default_care_limit()
        self.fix_message.change_parameters(
            {"Side": "1", "OrderQtyData": {"OrderQty": self.qty}, "Account": self.client, "Price": self.price}
        )
        response = self.fix_manager.send_message_and_receive_response(self.fix_message)
        # get Client Order ID and Order ID
        cl_ord_id = response[0].get_parameters()["ClOrdID"]
        ord_id = response[0].get_parameters()["OrderID"]
        # endregion

        # region Step 3 - Execute Care order
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

        # region Step 4 - Complete CO
        self.complete_request.set_default_complete(ord_id)
        responses = self.java_api_manager.send_message_and_receive_response(self.complete_request)
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

        # region Step 5- Book order
        self.allocation_instruction.set_default_book(ord_id)
        self.allocation_instruction.update_fields_in_component(
            "AllocationInstructionBlock",
            {
                "Qty": self.qty,
                "AccountGroupID": self.client,
                "GrossTradeAmt": "2000",
                "AvgPx": self.price,
                "SettlCurrAmt": "2000",
                "InstrID": self.data_set.get_instrument_id_by_name("instrument_2"),
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
        self.java_api_manager.compare_values(
            {
                JavaApiFields.AllocStatus.value: "APP",
                JavaApiFields.MatchStatus.value: "UNM",
                JavaApiFields.ConfirmationService.value: AllocationReportConst.ConfirmationService_INT.value,
            },
            alloc_report_reply,
            "Comparing Statuses and ConfirmationService in MO after Book",
        )
        # endregion

        # region Step 6 - Change Confirmation Service
        self.change_confirmation_service_request.set_default(alloc_id)
        responses = self.java_api_manager.send_message_and_receive_response(self.change_confirmation_service_request)
        print_message("Change Confirmation Service", responses)
        allocation_report = self.java_api_manager.get_last_message(
            ORSMessageType.AllocationReport.value
        ).get_parameters()[JavaApiFields.AllocationReportBlock.value]
        self.java_api_manager.compare_values(
            {
                JavaApiFields.AllocStatus.value: "APP",
                JavaApiFields.MatchStatus.value: "UNM",
                JavaApiFields.ConfirmationService.value: AllocationReportConst.ConfirmationService_MAN.value,
            },
            allocation_report,
            "Comparing ConfirmationService after Override Conf Service",
        )
        # endregion

        logger.info(f"Case {self.test_id} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")
