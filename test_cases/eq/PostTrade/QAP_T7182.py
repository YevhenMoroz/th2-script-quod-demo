import logging
from datetime import datetime
from pathlib import Path

from custom import basic_custom_actions as bca
from custom.basic_custom_actions import timestamps
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, OrderReplyConst, ExecutionReportConst
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


class QAP_T7182(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        # region Declarations
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.qty = "100"
        self.price = "1234"
        self.currency = self.data_set.get_currency_by_name("currency_3")  # GBp
        self.currency_major = self.data_set.get_currency_by_name("currency_2")  # GBP
        self.client = self.data_set.get_client("client_pt_1")  # MOClient
        self.java_api_connectivity = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.allocation_instruction = AllocationInstructionOMS(self.data_set)
        self.order_submit = OrderSubmitOMS(data_set)
        self.order_submit_second = OrderSubmitOMS(data_set)
        self.execution_report = ExecutionReportOMS(self.data_set)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Precondition - Create first DMA order
        self.order_submit.set_default_dma_limit()
        self.order_submit.update_fields_in_component(
            "NewOrderSingleBlock",
            {
                "OrdQty": self.qty,
                "AccountGroupID": self.client,
                "Price": self.price,
                "InstrID": self.data_set.get_instrument_id_by_name("instrument_3"),
                "SettlCurrency": self.currency,
                "ListingList": {"ListingBlock": [{"ListingID": self.data_set.get_listing_id_by_name("listing_2")}]},
            },
        )
        responses = self.java_api_manager.send_message_and_receive_response(self.order_submit)
        print_message("CREATE", responses)
        order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value
        ]
        ord_id_first = order_reply["OrdID"]
        self.java_api_manager.compare_values(
            {JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_SEN.value},
            order_reply,
            "Comparing Status of DMA order",
        )
        # endregion

        # region Precondition - Trade first DMA order and checking statuses
        self.execution_report.set_default_trade(ord_id_first)
        self.execution_report.update_fields_in_component(
            "ExecutionReportBlock",
            {
                "Price": self.price,
                "AvgPrice": self.price,
                "LastPx": self.price,
                "OrdQty": self.qty,
                "LastTradedQty": self.qty,
                "CumQty": self.qty,
                "InstrumentBlock": self.data_set.get_java_api_instrument("instrument_3"),
                "LastMkt": self.data_set.get_mic_by_name("mic_2"),
                "Currency": self.currency,
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

        execution_report_message_2 = self.java_api_manager.get_last_message(
            ORSMessageType.ExecutionReport.value, filter_value=ExecutionReportConst.ExecType_TRD.value
        ).get_parameters()[JavaApiFields.ExecutionReportBlock.value]
        exec_id_first = execution_report_message_2["ExecID"]  # get first ExecID (EX) for Mass Book
        # endregion

        # region Precondition - Create second DMA order
        self.order_submit_second.set_default_dma_limit()
        self.order_submit_second.update_fields_in_component(
            "NewOrderSingleBlock",
            {
                "OrdQty": self.qty,
                "AccountGroupID": self.client,
                "Price": self.price,
                "InstrID": self.data_set.get_instrument_id_by_name("instrument_3"),
                "SettlCurrency": self.currency,
                "ListingList": {"ListingBlock": [{"ListingID": self.data_set.get_listing_id_by_name("listing_2")}]},
            },
        )
        responses = self.java_api_manager.send_message_and_receive_response(self.order_submit_second)
        print_message("CREATE", responses)
        order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value
        ]
        ord_id_second = order_reply["OrdID"]
        self.java_api_manager.compare_values(
            {JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_SEN.value},
            order_reply,
            "Comparing Status of DMA order",
        )
        # endregion

        # region Precondition - Trade second DMA order and checking statuses
        self.execution_report.set_default_trade(ord_id_second)
        self.execution_report.update_fields_in_component(
            "ExecutionReportBlock",
            {
                "Price": self.price,
                "AvgPrice": self.price,
                "LastPx": self.price,
                "OrdQty": self.qty,
                "LastTradedQty": self.qty,
                "CumQty": self.qty,
                "InstrumentBlock": self.data_set.get_java_api_instrument("instrument_3"),
                "LastMkt": self.data_set.get_mic_by_name("mic_2"),
                "Currency": self.currency,
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

        execution_report_message_2 = self.java_api_manager.get_last_message(
            ORSMessageType.ExecutionReport.value, filter_value=ExecutionReportConst.ExecType_TRD.value
        ).get_parameters()[JavaApiFields.ExecutionReportBlock.value]
        exec_id_second = execution_report_message_2["ExecID"]  # get second ExecID (EX) for Mass Book
        # endregion

        # region Step 1,2 - Book first order
        self.allocation_instruction.set_default_book(ord_id_first)
        self.allocation_instruction.remove_fields_from_component(
            "AllocationInstructionBlock",
            [
                "GrossTradeAmt",
                "SettlCurrAmt",
                "AvgPx",
                "Currency",
                "BookingType",
                "NetGrossInd",
                "RecomputeInSettlCurrency",
                "SettlDate",
            ],
        )
        self.allocation_instruction.update_fields_in_component(
            "AllocationInstructionBlock",
            {
                "Qty": self.qty,
                "AccountGroupID": self.client,
                "InstrID": self.data_set.get_instrument_id_by_name("instrument_3"),
                "ExecAllocList": {
                    "ExecAllocBlock": [
                        {"ExecQty": self.qty, "ExecID": exec_id_first, "ExecPrice": str(int(self.price) / 100)}
                    ]
                },
                "ComputeFeesCommissions": "Yes",
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
            "Comparing PostTradeStatus after Book for",
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
                "AvgPrice": str(int(self.price) / 100),
                "Qty": str(float(self.qty)),
            },
            alloc_report_reply,
            "Comparing the values after Book in the Middle Office for first order",
        )
        # endregion

        # region Step 1,2 - Book second order
        self.allocation_instruction.set_default_book(ord_id_second)
        self.allocation_instruction.update_fields_in_component(
            "AllocationInstructionBlock",
            {
                "ExecAllocList": {
                    "ExecAllocBlock": [
                        {"ExecQty": self.qty, "ExecID": exec_id_second, "ExecPrice": str(int(self.price) / 100)}
                    ]
                }
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
            "Comparing PostTradeStatus after Book for",
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
                "AvgPrice": str(int(self.price) / 100),
                "Qty": str(float(self.qty)),
            },
            alloc_report_reply,
            "Comparing the values after Book in the Middle Office for second order",
        )
        # endregion

        logger.info(f"Case {self.test_id} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")
