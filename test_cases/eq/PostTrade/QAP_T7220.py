import logging
import os
import time
from datetime import datetime, timedelta
from pathlib import Path

from custom import basic_custom_actions as bca
from custom.basic_custom_actions import timestamps
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import (
    OrderReplyConst,
    JavaApiFields,
    ExecutionReportConst,
    ConfirmationReportConst,
)
from test_framework.java_api_wrappers.oms.es_messages.ExecutionReportOMS import ExecutionReportOMS
from test_framework.java_api_wrappers.oms.ors_messges.AllocationInstructionOMS import AllocationInstructionOMS
from test_framework.java_api_wrappers.oms.ors_messges.ConfirmationOMS import ConfirmationOMS
from test_framework.java_api_wrappers.oms.ors_messges.FixNewOrderSingleOMS import FixNewOrderSingleOMS
from test_framework.java_api_wrappers.oms.ors_messges.ForceAllocInstructionStatusRequestOMS import (
    ForceAllocInstructionStatusRequestOMS,
)
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.java_api_wrappers.ors_messages.OrderModificationRequest import OrderModificationRequest

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

seconds, nanos = timestamps()  # Test case start time


def print_message(message, responses):
    logger.info(message)
    for i in responses:
        logger.info(i)
        logger.info(i.get_parameters())


class QAP_T7220(TestCase):
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
        self.nos = FixNewOrderSingleOMS(self.data_set)
        self.settl_date = (datetime.now() + timedelta(days=4)).strftime("%Y-%m-%dT%H:%M")
        self.modification_request = OrderModificationRequest()
        self.rule_manager = RuleManager(Simulators.equity)
        self.venue = self.data_set.get_mic_by_name("mic_1")
        self.venue_client_names = self.data_set.get_venue_client_names_by_name("client_pt_1_venue_1")

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Precondition - Create DMA order via FIX
        try:
            nos_rule = self.rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(
                self.fix_env.buy_side, self.venue_client_names, self.venue, float(self.price)
            )
            self.nos.set_default_dma_limit()
            self.nos.update_fields_in_component(
                "NewOrderSingleBlock",
                {
                    "OrdQty": self.qty,
                    "ClientAccountGroupID": self.client,
                    "Price": self.price,
                    "SettlDate": self.settl_date,
                },
            )
            responses = self.java_api_manager.send_message_and_receive_response(self.nos)
            print_message("CREATE", responses)

        except Exception as e:
            logger.info(f"Your Exception is {e}")
        finally:
            time.sleep(2)
            self.rule_manager.remove_rule(nos_rule)

        order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value
        ]
        ord_id = order_reply["OrdID"]
        cl_ord_id = order_reply["ClOrdID"]
        settl_date_expected = datetime.strftime(datetime.now() + timedelta(days=4), "%Y-%m-%d") + "T12:00"
        self.java_api_manager.compare_values(
            {JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_OPN.value, "SettlDate": settl_date_expected},
            order_reply,
            "Precondition - Checking Status, SettlDate(+4 days) of DMA order",
        )
        # endregion

        # region Step 1 - Amend SettlDate of DMA order
        try:
            modification_rule = self.rule_manager.add_OrderCancelReplaceRequest_FIXStandard(
                self.fix_env.buy_side, self.venue_client_names, self.venue, True
            )
            self.modification_request.set_default(self.data_set, ord_id)
            settl_date = (datetime.now() + timedelta(days=5)).strftime("%Y-%m-%dT%H:%M")  # +5 days
            self.modification_request.update_fields_in_component(
                "OrderModificationRequestBlock",
                {"AccountGroupID": self.client, "SettlDate": settl_date, "ExecutionPolicy": "DMA"},
            )
            responses = self.java_api_manager.send_message_and_receive_response(self.modification_request)
            print_message("Amend SettlDate", responses)
        except Exception as e:
            logger.info(f"Your Exception is {e}")
        finally:
            time.sleep(2)
            self.rule_manager.remove_rule(modification_rule)

        order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value
        ]
        settl_date_expected = datetime.strftime(datetime.now() + timedelta(days=5), "%Y-%m-%d") + "T12:00"
        self.java_api_manager.compare_values(
            {JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_OPN.value, "SettlDate": settl_date_expected},
            order_reply,
            "Step 1 - Checking SettlDate(+5 days) of DMA order after Amend SettlDate",
        )
        # endregion

        # region Step 2,3 - Execute DMA order
        self.execution_report.set_default_trade(ord_id)
        responses = self.java_api_manager.send_message_and_receive_response(self.execution_report)
        print_message("Execute DMA", responses)
        execution_report_message = self.java_api_manager.get_last_message(
            ORSMessageType.ExecutionReport.value,
        ).get_parameters()[JavaApiFields.ExecutionReportBlock.value]
        settl_date_expected = datetime.strftime(datetime.now() + timedelta(days=2), "%Y-%m-%d") + "T12:00"
        self.java_api_manager.compare_values(
            {
                JavaApiFields.TransExecStatus.value: ExecutionReportConst.TransExecStatus_FIL.value,
                "SettlDate": settl_date_expected,
            },
            execution_report_message,
            "Step 3 - Checking SettlDate(+2 days) after Execute DMA order",
        )
        # endregion

        # region Step 6 - Book order
        self.allocation_instruction.set_default_book(ord_id)
        settl_date = (datetime.now() + timedelta(days=6)).strftime("%Y-%m-%dT%H:%M")  # +6 days
        self.allocation_instruction.update_fields_in_component(
            "AllocationInstructionBlock",
            {
                "AccountGroupID": self.client,
                "GrossTradeAmt": "2000",
                "AvgPx": self.price,
                "SettlCurrAmt": "2000",
                "SettlDate": settl_date,
                "InstrID": self.data_set.get_instrument_id_by_name("instrument_2"),
            },
        )
        responses = self.java_api_manager.send_message_and_receive_response(self.allocation_instruction)
        print_message("BOOK", responses)

        # Checking AllocationReportBlock
        alloc_report_reply = self.java_api_manager.get_last_message(
            ORSMessageType.AllocationReport.value
        ).get_parameters()[JavaApiFields.AllocationReportBlock.value]
        alloc_id: str = alloc_report_reply["ClientAllocID"]
        settl_date_expected = datetime.strftime(datetime.now() + timedelta(days=6), "%Y-%m-%d") + "T12:00"
        self.java_api_manager.compare_values(
            {
                JavaApiFields.AllocStatus.value: "APP",
                JavaApiFields.MatchStatus.value: "UNM",
                "SettlDate": settl_date_expected,
            },
            alloc_report_reply,
            "Step 6 - Checking SettlDate(+6 days) in MO after Book",
        )
        # endregion

        # region Step 7 - Approve
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
            "Step 7 - Comparing Status and Match Status after Approve",
        )
        # endregion

        # region Step 8 - Allocate block
        self.confirmation_request.set_default_allocation(alloc_id)
        settl_date = (datetime.now() + timedelta(days=10)).strftime("%Y-%m-%dT%H:%M")  # +10 days
        self.confirmation_request.update_fields_in_component(
            "ConfirmationBlock",
            {
                "AllocAccountID": self.alloc_account,
                "AllocQty": self.qty,
                "AvgPx": self.price,
                "InstrID": self.data_set.get_instrument_id_by_name("instrument_2"),
                "SettlDate": settl_date,
            },
        )
        responses = self.java_api_manager.send_message_and_receive_response(self.confirmation_request)
        print_message("Allocate", responses)

        conf_report_reply = self.java_api_manager.get_last_message(
            ORSMessageType.ConfirmationReport.value
        ).get_parameters()[JavaApiFields.ConfirmationReportBlock.value]

        settl_date_expected = datetime.strftime(datetime.now() + timedelta(days=10), "%Y-%m-%d") + "T12:00"
        self.java_api_manager.compare_values(
            {
                JavaApiFields.AffirmStatus.value: ConfirmationReportConst.ConfirmStatus_AFF.value,
                JavaApiFields.MatchStatus.value: ConfirmationReportConst.MatchStatus_MAT.value,
                "SettlDate": settl_date_expected,
            },
            conf_report_reply,
            "Step 8 - Checking SettlDate(+10 days) for Allocation after Allocate block",
        )
        # endregion

        logger.info(f"Case {self.test_id} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")
