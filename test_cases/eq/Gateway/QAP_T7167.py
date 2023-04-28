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
    SubmitRequestConst,
    OrderReplyConst,
    ExecutionReportConst,
    AllocationReportConst,
    ConfirmationReportConst,
)
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
    AllocationsColumns,
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

seconds, nanos = timestamps()  # Test case start time


class QAP_T7167(TestCase):
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
        self.rule_manager = RuleManager(sim=Simulators.equity)
        self.client = self.data_set.get_client("client_pt_1")  # MOClient
        self.alloc_account = self.data_set.get_account_by_name("client_pt_1_acc_1")  # MOClient_SA1
        self.fix_manager = FixManager(self.ss_connectivity, self.test_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set)
        self.fix_verifier_dc = FixVerifier(self.fix_env.drop_copy, self.test_id)
        self.exec_report = FixMessageExecutionReportOMS(self.data_set)
        self.allocation_report = FixMessageAllocationInstructionReportOMS()
        self.confirmation_report = FixMessageConfirmationReportOMS(self.data_set)
        self.java_api_connectivity = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.submit_request = OrderSubmitOMS(self.data_set)
        self.trade_request = TradeEntryOMS(self.data_set)
        self.allocation_instruction = AllocationInstructionOMS(self.data_set)
        self.complete_order = DFDManagementBatchOMS(self.data_set)
        self.approve_message = ForceAllocInstructionStatusRequestOMS(self.data_set)
        self.confirmation_request = ConfirmationOMS(self.data_set)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        class_name = QAP_T7167
        # region Precondition - Create CO order
        self.submit_request.set_default_care_limit(
            recipient=self.environment.get_list_fe_environment()[0].user_1,
            desk=self.environment.get_list_fe_environment()[0].desk_ids[0],
            role=SubmitRequestConst.USER_ROLE_1.value,
        )
        self.submit_request.update_fields_in_component(
            "NewOrderSingleBlock",
            {
                "OrdCapacity": SubmitRequestConst.OrdCapacity_Agency.value,
                "OrdQty": self.qty,
                "AccountGroupID": self.client,
                "Price": self.price,
            },
        )
        responses = self.java_api_manager.send_message_and_receive_response(self.submit_request)
        class_name.print_message("CREATE", responses)
        order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value)
        ord_id = order_reply.get_parameter("OrdReplyBlock")["OrdID"]
        cl_ord_id = order_reply.get_parameter("OrdReplyBlock")["ClOrdID"]
        status = order_reply.get_parameter("OrdReplyBlock")["TransStatus"]
        self.java_api_manager.compare_values(
            {OrderBookColumns.sts.value: OrderReplyConst.TransStatus_OPN.value},
            {OrderBookColumns.sts.value: status},
            "Comparing Status of Care order",
        )
        # endregion

        # region Precondition - Execution of Care order
        self.trade_request.set_default_trade(ord_id, self.price, self.qty)
        responses = self.java_api_manager.send_message_and_receive_response(self.trade_request)
        class_name.print_message("TRADE", responses)
        exec_report = self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value)
        exec_sts = exec_report.get_parameters()["ExecutionReportBlock"]["TransExecStatus"]
        self.java_api_manager.compare_values(
            {OrderBookColumns.exec_sts.value: ExecutionReportConst.TransExecStatus_FIL.value},
            {OrderBookColumns.exec_sts.value: exec_sts},
            "Comparing Execution status",
        )
        # endregion

        # region Step 1 - Complete CO
        self.complete_order.set_default_complete(ord_id)
        responses = self.java_api_manager.send_message_and_receive_response(self.complete_order)
        class_name.print_message("COMPLETE", responses)
        order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value)
        post_trade_status = order_reply.get_parameter("OrdReplyBlock")["PostTradeStatus"]
        done_for_day = order_reply.get_parameter("OrdReplyBlock")["DoneForDay"]
        self.java_api_manager.compare_values(
            {
                OrderBookColumns.post_trade_status.value: OrderReplyConst.PostTradeStatus_RDY.value,
                OrderBookColumns.done_for_day.value: OrderReplyConst.DoneForDay_YES.value,
            },
            {
                OrderBookColumns.post_trade_status.value: post_trade_status,
                OrderBookColumns.done_for_day.value: done_for_day,
            },
            "Comparing values after Complete",
        )
        # endregion

        # region Step 2-4 - Book CO
        self.allocation_instruction.set_default_book(ord_id)
        settl_currency_amt = str(int(self.qty) * int(self.price) * 2)
        settl_currency = self.data_set.get_currency_by_name("currency_5")  # UAH
        self.allocation_instruction.update_fields_in_component(
            "AllocationInstructionBlock",
            {
                "SettlCurrFxRate": "2",
                "SettlCurrFxRateCalc": "M",
                "SettlCurrAmt": settl_currency_amt,
                "SettlCurrency": settl_currency,
            },
        )
        responses = self.java_api_manager.send_message_and_receive_response(self.allocation_instruction)
        class_name.print_message("BOOK", responses)
        order_update = self.java_api_manager.get_last_message(ORSMessageType.OrdUpdate.value)
        post_trade_status = order_update.get_parameter("OrdUpdateBlock")["PostTradeStatus"]
        alloc_report_message = self.java_api_manager.get_last_message(ORSMessageType.AllocationReport.value)
        alloc_id = alloc_report_message.get_parameter("AllocationReportBlock")["ClientAllocID"]
        self.java_api_manager.compare_values(
            {OrderBookColumns.post_trade_status.value: OrderReplyConst.PostTradeStatus_BKD.value},
            {OrderBookColumns.post_trade_status.value: post_trade_status},
            "Comparing PostTradeStatus after Book",
        )
        # endregion

        # region Step 5 - Checking Allocation Report 35=J message with tag 10119
        list_of_ignored_fields = ["TransactTime", "QuodTradeQualifier", "BookID", "SettlDate", "Currency", "NetMoney",
                                  "TradeDate", "BookingType", "NoParty", "AllocInstructionMiscBlock1", "tag5120",
                                  "ReportedPx", "GrossTradeAmt", 'OrderAvgPx', 'tag11245', 'ExecAllocGrp',
                                  'AllocInstructionMiscBlock2']
        change_parameters = {
            "Instrument": "*",
            "AllocID": "*",
            "RootSettlCurrency": settl_currency,
            "AllocType": "5",
            "RootSettlCurrFxRateCalc": "M",
            "RootSettlCurrFxRate": "2",
            "RootSettlCurrAmt": settl_currency_amt,  # 10119 tag
            "Quantity": self.qty,
            "Side": "1",
            "AvgPx": self.price,
            "AllocTransType": "0",
            "NoOrders": [{"ClOrdID": cl_ord_id, "OrderID": ord_id, "OrderAvgPx": "*"}],
        }
        self.allocation_report.change_parameters(change_parameters)
        self.fix_verifier_dc.check_fix_message_fix_standard(
            self.allocation_report, key_parameters=["NoOrders", "AllocType", "AllocTransType"],
            ignored_fields=list_of_ignored_fields
        )
        # endregion

        # region Step 6 - Approve block
        self.approve_message.set_default_approve(alloc_id)
        responses = self.java_api_manager.send_message_and_receive_response(self.approve_message)
        class_name.print_message("APPROVE", responses)
        alloc_report_message = self.java_api_manager.get_last_message(ORSMessageType.AllocationReport.value)
        actual_alloc_status = alloc_report_message.get_parameters()["AllocationReportBlock"]["AllocStatus"]
        actual_match_status = alloc_report_message.get_parameters()["AllocationReportBlock"]["MatchStatus"]
        self.java_api_manager.compare_values(
            {
                MiddleOfficeColumns.sts.value: AllocationReportConst.AllocStatus_ACK.value,
                MiddleOfficeColumns.match_status.value: AllocationReportConst.MatchStatus_MAT.value,
            },
            {
                MiddleOfficeColumns.sts.value: actual_alloc_status,
                MiddleOfficeColumns.match_status.value: actual_match_status,
            },
            "Comparing statuses after Approve block",
        )
        # endregion

        # region Step 7 - Allocate block
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
        class_name.print_message("ALLOCATE", responses)
        confirmation_report = self.java_api_manager.get_last_message(ORSMessageType.ConfirmationReport.value)
        actual_allocation_status = confirmation_report.get_parameter("ConfirmationReportBlock")["ConfirmStatus"]
        actual_allocation_match_status = confirmation_report.get_parameter("ConfirmationReportBlock")["MatchStatus"]
        self.java_api_manager.compare_values(
            {
                AllocationsColumns.sts.value: ConfirmationReportConst.ConfirmStatus_AFF.value,
                AllocationsColumns.match_status.value: ConfirmationReportConst.MatchStatus_MAT.value,
            },
            {
                AllocationsColumns.sts.value: actual_allocation_status,
                AllocationsColumns.match_status.value: actual_allocation_match_status,
            },
            "Comparing statuses for Allocation after Allocate block",
        )

        allocation_report_message = self.java_api_manager.get_last_message(ORSMessageType.AllocationReport.value)
        status = allocation_report_message.get_parameters()["AllocationReportBlock"]["AllocStatus"]
        match_status = allocation_report_message.get_parameters()["AllocationReportBlock"]["MatchStatus"]
        summary_status = allocation_report_message.get_parameters()["AllocationReportBlock"]["AllocSummaryStatus"]
        self.java_api_manager.compare_values(
            {
                MiddleOfficeColumns.sts.value: AllocationReportConst.AllocStatus_ACK.value,
                MiddleOfficeColumns.match_status.value: AllocationReportConst.MatchStatus_MAT.value,
                MiddleOfficeColumns.summary_status.value: AllocationReportConst.AllocSummaryStatus_MAG.value,
            },
            {
                MiddleOfficeColumns.sts.value: status,
                MiddleOfficeColumns.match_status.value: match_status,
                MiddleOfficeColumns.summary_status.value: summary_status,
            },
            "Comparing statuses for Block after Allocate block",
        )
        # endregion

        # region Step 8 - Checking 35=J and 35=AK messages
        # Checking Allocation Report 35=J message with tag 10119 (RootSettlCurrAmt)
        list_of_ignored_fields.extend(
            ["AllocSettlCurrAmt", "IndividualAllocID", "AllocNetPrice", "AllocSettlCurrency", "SettlCurrFxRate",
             "SettlCurrency", "SettlCurrFxRateCalc"])
        no_alloc_list = [
            {
                "AllocAccount": self.alloc_account,
                "AllocQty": self.qty,
                "AllocPrice": self.price,
                "SettlCurrAmt": '*',
            }
        ]
        self.allocation_report.change_parameters({"AllocType": "2", "NoAllocs": no_alloc_list, "AllocID": alloc_id})
        self.fix_verifier_dc.check_fix_message_fix_standard(
            self.allocation_report,
            key_parameters=["NoOrders", "AllocType", "AllocID"],
            ignored_fields=list_of_ignored_fields,
        )

        # Checking Confirmation Report 35=AK message with tag 119 (SettlCurrAmt)
        list_of_ignored_fields.extend(
            ["SettlCurrFxRate", "SettlCurrFxRateCalc", "ConfirmType", "SettlCurrency", "MatchStatus", "ConfirmStatus",
             "CpctyConfGrp", "ConfirmID", "AllocTransType"])
        change_parameters.update(
            {
                "SettlCurrAmt": settl_currency_amt,
                "AllocQty": self.qty,
                "AllocAccount": self.alloc_account,
                "ConfirmTransType": "0",
                "AllocID": alloc_id,
            }
        )
        self.confirmation_report.change_parameters(change_parameters).remove_parameters(
            [
                "RootSettlCurrFxRateCalc",
                "RootSettlCurrency",
                "Quantity",
                "AllocType",
                "RootSettlCurrFxRate",
                "RootSettlCurrAmt",
            ]
        )
        self.fix_verifier_dc.check_fix_message_fix_standard(
            self.confirmation_report,
            key_parameters=["NoOrders", "ConfirmTransType", "AllocAccount", "AllocID"],
            ignored_fields=list_of_ignored_fields,
        )
        # endregion

        logger.info(f"Case {self.test_id} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")

    @staticmethod
    def print_message(message, responses):
        logger.info(message)
        for i in responses:
            logger.info(i)
            logger.info(i.get_parameters())
