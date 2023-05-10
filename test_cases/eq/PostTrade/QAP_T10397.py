import logging
from datetime import datetime
from pathlib import Path

from custom import basic_custom_actions as bca
from custom.basic_custom_actions import timestamps
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.oms.FixMessageConfirmationReportOMS import FixMessageConfirmationReportOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import (
    ExecutionReportConst,
    JavaApiFields,
    AllocationReportConst,
    AllocationInstructionConst,
    ConfirmationReportConst,
)
from test_framework.java_api_wrappers.oms.es_messages.ExecutionReportOMS import ExecutionReportOMS
from test_framework.java_api_wrappers.oms.ors_messges.AllocationInstructionOMS import AllocationInstructionOMS
from test_framework.java_api_wrappers.oms.ors_messges.ConfirmationOMS import ConfirmationOMS
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


class QAP_T10397(TestCase):
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
        self.order_submit = OrderSubmitOMS(data_set)
        self.execution_report = ExecutionReportOMS(self.data_set)
        self.trade_request = TradeEntryOMS(self.data_set)
        self.allocation_instruction = AllocationInstructionOMS(self.data_set)
        self.approve_request = ForceAllocInstructionStatusRequestOMS(self.data_set)
        self.confirmation_request = ConfirmationOMS(self.data_set)
        self.fix_verifier_dc = FixVerifier(self.fix_env.drop_copy, self.test_id)
        self.confirmation_report = FixMessageConfirmationReportOMS(self.data_set)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Step 1 - Create DMA > Fill the order > Book > Allocate
        # Create DMA order
        self.order_submit.set_default_dma_limit()
        responses = self.java_api_manager.send_message_and_receive_response(self.order_submit)
        print_message("Create DMA order", responses)
        order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value
        ]
        ord_id = order_reply["OrdID"]
        cl_ord_id = order_reply["ClOrdID"]

        # region Execute DMA order
        self.execution_report.set_default_trade(ord_id)
        responses = self.java_api_manager.send_message_and_receive_response(self.execution_report)
        print_message("Execute DMA order", responses)
        execution_report_message = self.java_api_manager.get_last_message(
            ORSMessageType.ExecutionReport.value
        ).get_parameters()[JavaApiFields.ExecutionReportBlock.value]
        self.java_api_manager.compare_values(
            {
                JavaApiFields.TransExecStatus.value: ExecutionReportConst.TransExecStatus_FIL.value,
            },
            execution_report_message,
            "Checking status of DMA order after execution",
        )

        # Book order
        self.allocation_instruction.set_default_book(ord_id)
        self.allocation_instruction.update_fields_in_component(
            "AllocationInstructionBlock",
            {
                JavaApiFields.Qty.value: self.qty,
                JavaApiFields.AccountGroupID.value: self.client,
                JavaApiFields.GrossTradeAmt.value: "2000",
                JavaApiFields.AvgPx.value: self.price,
                JavaApiFields.SettlCurrAmt.value: "2000",
                JavaApiFields.SettlType.value: "NextDay",
            },
        )
        responses = self.java_api_manager.send_message_and_receive_response(self.allocation_instruction)
        print_message("BOOK", responses)

        # Checking AllocationReportBlock
        alloc_report_reply = self.java_api_manager.get_last_message(
            ORSMessageType.AllocationReport.value
        ).get_parameters()[JavaApiFields.AllocationReportBlock.value]
        alloc_id = alloc_report_reply["ClientAllocID"]
        self.java_api_manager.compare_values(
            {
                JavaApiFields.AllocStatus.value: AllocationReportConst.AllocStatus_APP.value,
                JavaApiFields.MatchStatus.value: AllocationReportConst.MatchStatus_UNM.value,
                JavaApiFields.SettlType.value: AllocationInstructionConst.SettlType_TOM.value,
            },
            alloc_report_reply,
            "Checking Statuses, SettlType in MO after Book",
        )

        #  Approve
        self.approve_request.set_default_approve(alloc_id)
        responses = self.java_api_manager.send_message_and_receive_response(self.approve_request)
        print_message("APPROVE", responses)

        # Allocate
        self.confirmation_request.set_default_allocation(alloc_id)
        self.confirmation_request.update_fields_in_component(
            "ConfirmationBlock",
            {
                JavaApiFields.AllocAccountID.value: self.alloc_account,
                JavaApiFields.AllocQty.value: self.qty,
                JavaApiFields.AvgPx.value: self.price,
            },
        )
        responses = self.java_api_manager.send_message_and_receive_response(self.confirmation_request)
        print_message("ALLOCATE", responses)
        conf_report_message = self.java_api_manager.get_last_message(
            ORSMessageType.ConfirmationReport.value
        ).get_parameters()[JavaApiFields.ConfirmationReportBlock.value]
        self.java_api_manager.compare_values(
            {
                JavaApiFields.ConfirmStatus.value: ConfirmationReportConst.ConfirmStatus_AFF.value,
                JavaApiFields.MatchStatus.value: ConfirmationReportConst.MatchStatus_MAT.value,
                JavaApiFields.SettlType.value: AllocationInstructionConst.SettlType_TOM.value,
            },
            conf_report_message,
            "Checking Statuses, SettlType for Allocation after Allocate block",
        )
        # endregion

        # Step 2 - Check 35=AK message in BO
        list_of_ignored_fields: list = ["TransactTime", "Side", "QuodTradeQualifier", "BookID", "SettlDate", "Currency",
                                        "NetMoney", "MatchStatus", "TradeDate", "NoParty", "AllocInstructionMiscBlock1",
                                        "AllocInstructionMiscBlock2", "tag11245", "tag5120", "CpctyConfGrp",
                                        "ReportedPx", "Instrument", "GrossTradeAmt", "ConfirmID"]
        self.confirmation_report.change_parameters(
            {
                "NoOrders": [{"ClOrdID": cl_ord_id, "OrderID": ord_id, "OrderAvgPx": self.price}],
                "ConfirmTransType": "0",
                "ConfirmType": "2",
                "AllocQty": self.qty,
                "AllocAccount": self.alloc_account,
                "AllocID": alloc_id,
                "ConfirmStatus": "1",
                "SettlType": "2",
                "AvgPx": self.price,
            }
        )
        self.fix_verifier_dc.check_fix_message_fix_standard(
            self.confirmation_report,
            key_parameters=["ConfirmTransType", "NoOrders", "ConfirmType", "AllocAccount"],
            ignored_fields=list_of_ignored_fields,
        )
        # endregion

        logger.info(f"Case {self.test_id} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")
