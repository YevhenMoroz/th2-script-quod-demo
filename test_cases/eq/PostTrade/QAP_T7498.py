import logging
import time
from datetime import datetime, timedelta, timezone
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
    CommissionAmountTypeConst,
    CommissionBasisConst,
)
from test_framework.java_api_wrappers.oms.es_messages.ExecutionReportOMS import ExecutionReportOMS
from test_framework.java_api_wrappers.oms.ors_messges.AllocationInstructionOMS import AllocationInstructionOMS
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.rest_api_wrappers.oms.rest_commissions_sender import RestCommissionsSender

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

seconds, nanos = timestamps()  # Test case start time


def print_message(message, responses):
    logger.info(message)
    for i in responses:
        logger.info(i)
        logger.info(i.get_parameters())


class QAP_T7498(TestCase):
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
        self.order_submit = OrderSubmitOMS(data_set)
        self.allocation_instruction = AllocationInstructionOMS(self.data_set)
        self.execution_report = ExecutionReportOMS(self.data_set)
        self.abs_amt = self.data_set.get_comm_profile_by_name("abs_amt")
        self.perc_amt = self.data_set.get_comm_profile_by_name("perc_amt")
        self.wa_connectivity = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.rest_commission_sender = RestCommissionsSender(self.wa_connectivity, self.test_id, self.data_set)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Precondition - Send commission
        self.rest_commission_sender.clear_commissions()
        self.rest_commission_sender.clear_fees()
        # send commission
        self.rest_commission_sender.set_modify_client_commission_message(client=self.client, comm_profile=self.abs_amt)
        self.rest_commission_sender.send_post_request()
        time.sleep(3)

        # send fees
        self.rest_commission_sender.set_modify_fees_message(comm_profile=self.perc_amt)
        self.rest_commission_sender.change_message_params({"venueID": self.data_set.get_venue_by_name("venue_1")})
        self.rest_commission_sender.send_post_request()
        time.sleep(3)
        # endregion

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

        # region Step 1 - Book order
        self.allocation_instruction.set_default_book(ord_id)

        expected_commissions: dict = {
            JavaApiFields.CommissionRate.value: "1.0",
            JavaApiFields.CommissionAmount.value: "1.0",
            JavaApiFields.CommissionCurrency.value: "EUR",
            JavaApiFields.CommissionAmountType.value: CommissionAmountTypeConst.CommissionAmountType_BRK.value,
            JavaApiFields.CommissionBasis.value: CommissionBasisConst.CommissionBasis_ABS.value,
        }
        expected_fees: dict = {
            JavaApiFields.RootMiscFeeType.value: "EXC",
            JavaApiFields.RootMiscFeeAmt.value: "100.0",
            JavaApiFields.RootMiscFeeBasis.value: "P",
            JavaApiFields.RootMiscFeeCurr.value: "EUR",
            JavaApiFields.RootMiscFeeRate.value: "5.0",
        }

        self.allocation_instruction.update_fields_in_component(
            "AllocationInstructionBlock",
            {
                "Qty": self.qty,
                "AccountGroupID": self.client,
                "GrossTradeAmt": "2000",
                "AvgPx": self.price,
                "SettlCurrAmt": "4202",
                "SettlType": "REG",
                "SettlCurrFxRate": "2",
                "SettlCurrFxRateCalc": "M",
                "SettlCurrency": "UAH",
                "ClientCommissionList": {"ClientCommissionBlock": [expected_commissions]},
                "RootMiscFeesList": {"RootMiscFeesBlock": [expected_fees]},
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
        alloc_instr_id = alloc_report_reply["AllocInstructionID"]
        exec_id = alloc_report_reply["ExecAllocList"]["ExecAllocBlock"][0]["ExecID"]
        self.java_api_manager.compare_values(
            {
                JavaApiFields.AllocStatus.value: "APP",
                JavaApiFields.MatchStatus.value: "UNM",
                "SettlCurrFxRate": "2.0",
                "SettlCurrFxRateCalc": "M",
                "SettlCurrency": "UAH",
                "NetMoney": "2101.0",
                "AvgPrice": "20.0",
                "SettlType": "REG",
                "NetPrice": "21.01",
                "SettlCurrAmt": "4202.0",
                "GrossTradeAmt": "2000.0",
            },
            alloc_report_reply,
            "Comparing values in MO after Book",
        )

        # Comparing Client Commission
        self.java_api_manager.compare_values(
            expected_commissions,
            alloc_report_reply["ClientCommissionList"]["ClientCommissionBlock"][0],
            "Comparing Client Commission after Book",
        )

        # Comparing Fees
        self.java_api_manager.compare_values(
            expected_fees,
            alloc_report_reply["RootMiscFeesList"]["RootMiscFeesBlock"][0],
            "Comparing Fees after Book",
        )
        # endregion

        # region Step 3 - Amend block
        self.allocation_instruction.set_amend_book(alloc_instr_id, exec_id, self.qty, self.price)
        settl_date_new = (datetime.now(timezone.utc) + timedelta(days=1)).isoformat()
        self.allocation_instruction.remove_fields_from_component(
            "AllocationInstructionBlock", ["ClientCommissionList", "RootMiscFeesList"]
        )
        self.allocation_instruction.update_fields_in_component(
            "AllocationInstructionBlock",
            {
                "GrossTradeAmt": "2000",
                "AvgPx": self.price,
                "SettlCurrAmt": "500",
                "SettlType": "REG",
                "SettlCurrFxRate": "4",
                "SettlCurrFxRateCalc": "D",
                "SettlCurrency": "USD",
                "SettlDate": settl_date_new,
            },
        )

        responses = self.java_api_manager.send_message_and_receive_response(self.allocation_instruction)
        print_message("AMEND", responses)

        # Checking AllocationReportBlock
        alloc_report_reply_amend = self.java_api_manager.get_last_message(
            ORSMessageType.AllocationReport.value
        ).get_parameters()[JavaApiFields.AllocationReportBlock.value]
        settl_date_expected = datetime.strftime(datetime.now() + timedelta(days=1), "%Y-%m-%d") + "T12:00"
        self.java_api_manager.compare_values(
            {
                JavaApiFields.AllocStatus.value: "APP",
                JavaApiFields.MatchStatus.value: "UNM",
                "SettlCurrFxRate": "4.0",
                "SettlCurrFxRateCalc": "D",
                "SettlCurrency": "USD",
                "NetMoney": "2000.0",
                "AvgPrice": "20.0",
                "SettlType": "REG",
                "NetPrice": "20.0",
                "SettlCurrAmt": "500.0",
                "GrossTradeAmt": "2000.0",
                "SettlDate": settl_date_expected,
            },
            alloc_report_reply_amend,
            "Comparing values in MO after Amend",
        )

        self.java_api_manager.key_is_absent(
            "ClientCommissionList", alloc_report_reply_amend, "Checking that ClientCommissionList is absent"
        )
        self.java_api_manager.key_is_absent(
            "RootMiscFeesList", alloc_report_reply_amend, "Checking that RootMiscFeesList is absent"
        )
        # endregion

        logger.info(f"Case {self.test_id} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")
