import logging
from datetime import datetime
from pathlib import Path

from custom import basic_custom_actions as bca
from custom.basic_custom_actions import timestamps
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.oms.FixMessageAllocationInstructionReportOMS import (
    FixMessageAllocationInstructionReportOMS,
)
from test_framework.fix_wrappers.oms.FixMessageConfirmationReportOMS import FixMessageConfirmationReportOMS
from test_framework.fix_wrappers.oms.FixMessageExecutionReportOMS import FixMessageExecutionReportOMS
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import (
    OrderReplyConst,
    ExecutionReportConst,
    AllocationInstructionConst,
    AllocationReportConst,
    ConfirmationReportConst,
)
from test_framework.java_api_wrappers.oms.es_messages.ExecutionReportOMS import ExecutionReportOMS
from test_framework.java_api_wrappers.oms.ors_messges.AllocationInstructionOMS import AllocationInstructionOMS
from test_framework.java_api_wrappers.oms.ors_messges.ConfirmationOMS import ConfirmationOMS
from test_framework.java_api_wrappers.oms.ors_messges.DFDManagementBatchOMS import DFDManagementBatchOMS
from test_framework.java_api_wrappers.oms.ors_messges.ForceAllocInstructionStatusRequestOMS import (
    ForceAllocInstructionStatusRequestOMS,
)
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.java_api_wrappers.oms.ors_messges.TradeEntryOMS import TradeEntryOMS
from test_framework.win_gui_wrappers.fe_trading_constant import (
    OrderBookColumns,
    MiddleOfficeColumns,
)
from test_framework.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

seconds, nanos = timestamps()  # Test case start time


class QAP_T7552(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        # region Declarations
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.ss_connectivity = self.fix_env.sell_side
        self.bs_connectivity = self.fix_env.buy_side
        self.qty = "100"
        self.price = "10"
        self.price_for_allocation = '55'
        self.rule_manager = RuleManager(sim=Simulators.equity)
        self.client = self.data_set.get_client("client_pt_1")  # MOClient
        self.alloc_account = self.data_set.get_account_by_name("client_pt_1_acc_1")  # MOClient_SA1
        self.venue_client_names = self.data_set.get_venue_client_names_by_name("client_pt_1_venue_1")  # MOClient_PARIS
        self.exec_destination = self.data_set.get_mic_by_name("mic_1")  # XPAR
        self.order_book = OMSOrderBook(self.test_id, self.session_id)
        self.client_inbox = OMSClientInbox(self.test_id, self.session_id)
        self.fix_manager = FixManager(self.ss_connectivity, self.test_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set)
        self.fix_verifier = FixVerifier(self.ss_connectivity, self.test_id)
        self.fix_verifier_dc = FixVerifier(self.fix_env.drop_copy, self.test_id)
        self.exec_report = FixMessageExecutionReportOMS(self.data_set)
        self.allocation_report = FixMessageAllocationInstructionReportOMS()
        self.confirmation_report = FixMessageConfirmationReportOMS(self.data_set)
        self.java_api_connectivity = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.order_submit = OrderSubmitOMS(data_set)
        self.trade_entry_request = TradeEntryOMS(self.data_set)
        self.allocation_instruction = AllocationInstructionOMS(self.data_set)
        self.complete_order = DFDManagementBatchOMS(self.data_set)
        self.approve_message = ForceAllocInstructionStatusRequestOMS(self.data_set)
        self.confirmation_request = ConfirmationOMS(self.data_set)
        self.execution_report = ExecutionReportOMS(self.data_set)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        class_name = QAP_T7552
        # region Precondition - Create DMA order
        self.order_submit.set_default_dma_limit()
        self.order_submit.update_fields_in_component(
            "NewOrderSingleBlock", {"OrdQty": self.qty, "AccountGroupID": self.client, "Price": self.price}
        )
        responses = self.java_api_manager.send_message_and_receive_response(self.order_submit)
        class_name.print_message("CREATE", responses)
        order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value)
        ord_id = order_reply.get_parameter("OrdReplyBlock")["OrdID"]
        cl_ord_id = order_reply.get_parameter("OrdReplyBlock")["ClOrdID"]
        status = order_reply.get_parameter("OrdReplyBlock")["TransStatus"]
        self.java_api_manager.compare_values(
            {OrderBookColumns.sts.value: OrderReplyConst.TransStatus_SEN.value},
            {OrderBookColumns.sts.value: status},
            "Comparing Status of DMA order",
        )
        # endregion

        # region Precondition - Trade DMA order
        self.execution_report.set_default_trade(ord_id)
        self.execution_report.update_fields_in_component(
            "ExecutionReportBlock", {"Price": self.price, "AvgPrice": self.price, "LastPx": self.price}
        )
        responses = self.java_api_manager.send_message_and_receive_response(self.execution_report)
        class_name.print_message("TRADE", responses)
        execution_report_message = self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value)
        trans_exec_sts = execution_report_message.get_parameters()["ExecutionReportBlock"]["TransExecStatus"]
        post_trade_sts = execution_report_message.get_parameters()["ExecutionReportBlock"]["PostTradeStatus"]

        self.java_api_manager.compare_values(
            {
                OrderBookColumns.exec_sts.value: ExecutionReportConst.TransExecStatus_FIL.value,
                OrderBookColumns.post_trade_status.value: OrderReplyConst.PostTradeStatus_RDY.value,
            },
            {OrderBookColumns.exec_sts.value: trans_exec_sts, OrderBookColumns.post_trade_status.value: post_trade_sts},
            "Comparing ExecSts and PostTradeStatus of DMA order after Trade",
        )
        # endregion

        # region Step 1,2 - Book order
        self.allocation_instruction.set_default_book(ord_id)
        self.allocation_instruction.update_fields_in_component(
            "AllocationInstructionBlock", {"SettlType": AllocationInstructionConst.SettlType_REG.value}
        )
        responses = self.java_api_manager.send_message_and_receive_response(self.allocation_instruction)
        class_name.print_message("BOOK", responses)
        order_update_message = self.java_api_manager.get_last_message(ORSMessageType.OrdUpdate.value)
        post_trade_status = order_update_message.get_parameter("OrdUpdateBlock")["PostTradeStatus"]
        alloc_report_message = self.java_api_manager.get_last_message(ORSMessageType.AllocationReport.value)
        alloc_id = alloc_report_message.get_parameter("AllocationReportBlock")["ClientAllocID"]
        status = alloc_report_message.get_parameter("AllocationReportBlock")["AllocStatus"]
        match_status = alloc_report_message.get_parameter("AllocationReportBlock")["MatchStatus"]
        settl_type = alloc_report_message.get_parameter("AllocationReportBlock")["SettlType"]
        self.order_book.compare_values(
            {
                OrderBookColumns.post_trade_status.value: OrderReplyConst.PostTradeStatus_BKD.value,
                MiddleOfficeColumns.sts.value: AllocationReportConst.AllocStatus_APP.value,
                MiddleOfficeColumns.match_status.value: ConfirmationReportConst.MatchStatus_UNM.value,
                MiddleOfficeColumns.settltype.value: AllocationInstructionConst.SettlType_REG.value,
            },
            {
                OrderBookColumns.post_trade_status.value: post_trade_status,
                MiddleOfficeColumns.sts.value: status,
                MiddleOfficeColumns.match_status.value: match_status,
                MiddleOfficeColumns.settltype.value: settl_type,
            },
            "Comparing Statuses after Book",
        )
        # endregion

        # region Step 3 - Approve block
        self.approve_message.set_default_approve(alloc_id)
        responses = self.java_api_manager.send_message_and_receive_response(self.approve_message)
        class_name.print_message("APPROVE", responses)
        alloc_report_message = self.java_api_manager.get_last_message(ORSMessageType.AllocationReport.value)
        status = alloc_report_message.get_parameters()["AllocationReportBlock"]["AllocStatus"]
        match_status = alloc_report_message.get_parameters()["AllocationReportBlock"]["MatchStatus"]
        self.java_api_manager.compare_values(
            {
                MiddleOfficeColumns.sts.value: AllocationReportConst.AllocStatus_ACK.value,
                MiddleOfficeColumns.match_status.value: AllocationReportConst.MatchStatus_MAT.value,
            },
            {
                MiddleOfficeColumns.sts.value: status,
                MiddleOfficeColumns.match_status.value: match_status,
            },
            "Comparing statuses after Approve block",
        )
        # endregion

        # region Step 4,5 - Allocate block
        self.confirmation_request.set_default_allocation(alloc_id)
        self.confirmation_request.update_fields_in_component(
            "ConfirmationBlock",
            {
                "AllocAccountID": self.alloc_account,
                "AllocQty": self.qty,
                "AvgPx": self.price_for_allocation,
            },
        )
        responses = self.java_api_manager.send_message_and_receive_response(self.confirmation_request)
        class_name.print_message("ALLOCATE", responses)
        conf_report_message = self.java_api_manager.get_last_message(
            ORSMessageType.ConfirmationReport.value
        ).get_parameters()["ConfirmationReportBlock"]
        self.java_api_manager.compare_values(
            {
                "ConfirmStatus": ConfirmationReportConst.ConfirmStatus_AFF.value,
                "MatchStatus": ConfirmationReportConst.MatchStatus_MAT.value,
                "AvgPx": str(float(self.price_for_allocation)),
                "AllocQty": str(float(self.qty)),
                "SettlType": AllocationInstructionConst.SettlType_REG.value,
            },
            conf_report_message,
            "Comparing values for Allocation after Allocate block",
        )

        allocation_report_message = self.java_api_manager.get_last_message(
            ORSMessageType.AllocationReport.value
        ).get_parameters()["AllocationReportBlock"]
        self.java_api_manager.compare_values(
            {
                "AllocStatus": AllocationReportConst.AllocStatus_ACK.value,
                "MatchStatus": AllocationReportConst.MatchStatus_MAT.value,
                "AllocSummaryStatus": AllocationReportConst.AllocSummaryStatus_MAG.value,
                "SettlType": AllocationInstructionConst.SettlType_REG.value,
            },
            allocation_report_message,
            "Comparing values for Block after Allocate block",
        )
        # endregion

        logger.info(f"Case {self.test_id} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")

    @staticmethod
    def print_message(message, responses):
        logger.info(message)
        for i in responses:
            logger.info(i)
            logger.info(i.get_parameters())
