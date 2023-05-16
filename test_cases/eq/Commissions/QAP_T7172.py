import logging
import time
from datetime import datetime
from pathlib import Path

from custom.basic_custom_actions import create_event
from custom.basic_custom_actions import timestamps
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.oms.FixMessageExecutionReportOMS import FixMessageExecutionReportOMS
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import (
    OrderReplyConst,
    AllocationReportConst,
    ConfirmationReportConst,
    CommissionAmountTypeConst, CommissionBasisConst, JavaApiFields,
)
from test_framework.java_api_wrappers.oms.ors_messges.AllocationInstructionOMS import AllocationInstructionOMS
from test_framework.java_api_wrappers.oms.ors_messges.ConfirmationOMS import ConfirmationOMS
from test_framework.java_api_wrappers.oms.ors_messges.ForceAllocInstructionStatusRequestOMS import (
    ForceAllocInstructionStatusRequestOMS,
)
from test_framework.rest_api_wrappers.oms.rest_commissions_sender import RestCommissionsSender
from test_framework.win_gui_wrappers.fe_trading_constant import (
    OrderBookColumns,
    MiddleOfficeColumns,
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

seconds, nanos = timestamps()  # Test case start time


class QAP_T7172(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        # region Declarations
        self.test_id = create_event(self.__class__.__name__, self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.ss_connectivity = self.fix_env.sell_side
        self.bs_connectivity = self.fix_env.buy_side
        self.wa_connectivity = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.qty = "100"
        self.price = "10"
        self.client = self.data_set.get_client_by_name("client_com_1")  # CLIENT_COMM_1
        self.account = self.data_set.get_account_by_name("client_com_1_acc_4")  # CLIENT_COMM_1_EXEMPTED
        self.venue = self.data_set.get_mic_by_name("mic_2")  # EUREX
        self.venue_client_names = self.data_set.get_venue_client_names_by_name(
            "client_com_1_venue_2"
        )  # CLIENT_COMM_1_EUREX
        self.currency_minor = self.data_set.get_currency_by_name("currency_3")  # GBp
        self.currency_major = self.data_set.get_currency_by_name("currency_2")  # GBP
        self.rule_manager = RuleManager(sim=Simulators.equity)
        self.fix_manager = FixManager(self.ss_connectivity, self.test_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set)
        self.fix_verifier = FixVerifier(self.ss_connectivity, self.test_id)
        self.exec_report = FixMessageExecutionReportOMS(self.data_set)
        self.commission_sender = RestCommissionsSender(self.wa_connectivity, self.test_id, self.data_set)
        self.perc_amt = self.data_set.get_comm_profile_by_name("perc_amt")
        self.java_api_connectivity = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.allocation_instruction = AllocationInstructionOMS(self.data_set)
        self.approve_message = ForceAllocInstructionStatusRequestOMS(self.data_set)
        self.confirmation_request = ConfirmationOMS(self.data_set)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Precondition - Send commission
        class_name = QAP_T7172
        self.commission_sender.clear_commissions()
        self.commission_sender.clear_fees()
        self.commission_sender.set_modify_client_commission_message(account=self.account, comm_profile=self.perc_amt)
        self.commission_sender.send_post_request()
        time.sleep(3)
        # endregion

        # region Precondition - Create DMA order via FIX
        try:
            no_allocs: dict = {"NoAllocs": [{"AllocAccount": self.account, "AllocQty": self.qty}]}
            trade_rule = self.rule_manager.add_NewOrdSingleExecutionReportTrade_FIXStandard(
                self.bs_connectivity, self.venue_client_names, self.venue, float(self.price), int(self.qty), 0
            )

            self.fix_message.set_default_dma_limit(instr="instrument_3")
            self.fix_message.change_parameters(
                {
                    "Side": "1",
                    "OrderQtyData": {"OrderQty": self.qty},
                    "Account": self.client,
                    "Price": self.price,
                    "Currency": self.currency_minor,
                    "ExDestination": self.venue,
                    "PreAllocGrp": no_allocs,
                }
            )
            response = self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message)
            # get Client Order ID and Order ID
            cl_ord_id = response[0].get_parameters()["ClOrdID"]
            order_id = response[0].get_parameters()["OrderID"]
        except Exception:
            logger.error("Error execution", exc_info=True)
        finally:
            time.sleep(2)
            self.rule_manager.remove_rule(trade_rule)
        # endregion

        # region Check ExecutionReports
        self.exec_report.set_default_new(self.fix_message)
        self.exec_report.change_parameters(
            {"SecondaryOrderID": "*", "Text": "*", "LastMkt": "*", "Currency": self.currency_minor}
        )
        list_ignored_fields = ['GatingRuleCondName', 'GatingRuleName']
        self.fix_verifier.check_fix_message_fix_standard(self.exec_report, ignored_fields=list_ignored_fields)
        # endregion

        # region Step 1 - Book order
        self.allocation_instruction.set_default_book(order_id)
        self.allocation_instruction.update_fields_in_component(
            "AllocationInstructionBlock",
            {
                "InstrID": self.data_set.get_instrument_id_by_name("instrument_3"),
                "Currency": self.currency_major,
                "AccountGroupID": self.client,
                "GrossTradeAmt": "10",
                "AvgPx": "0.1",
                "Qty": self.qty,
                "SettlCurrAmt": "10.5",
                "ClientCommissionList": {
                    "ClientCommissionBlock": [
                        {
                            "CommissionAmountType": CommissionAmountTypeConst.CommissionAmountType_BRK.value,
                            "CommissionAmount": "0.5",
                            "CommissionBasis": CommissionBasisConst.CommissionBasis_PCT.value,
                            "CommissionCurrency": self.currency_major,
                            "CommissionRate": "5",
                        }
                    ]
                },
            },
        )

        responses = self.java_api_manager.send_message_and_receive_response(self.allocation_instruction)
        class_name.print_message("BOOK", responses)

        order_update_message = self.java_api_manager.get_last_message(ORSMessageType.OrdUpdate.value)
        post_trade_status = order_update_message.get_parameter("OrdUpdateBlock")["PostTradeStatus"]

        alloc_report_message = self.java_api_manager.get_last_message(ORSMessageType.AllocationReport.value,
                                                                      JavaApiFields.BookingAllocInstructionID.value)
        alloc_id = alloc_report_message.get_parameter("AllocationReportBlock")["ClientAllocID"]
        status = alloc_report_message.get_parameter("AllocationReportBlock")["AllocStatus"]
        match_status = alloc_report_message.get_parameter("AllocationReportBlock")["MatchStatus"]
        # client_comm = alloc_report_message.get_parameter("AllocationReportBlock")["ClientCommissionList"]["ClientCommissionBlock"][0]['CommissionAmount']
        client_comm = alloc_report_message.get_parameter("AllocationReportBlock")["ClientCommissionDataBlock"][
            "ClientCommission"
        ]
        self.java_api_manager.compare_values(
            {
                OrderBookColumns.post_trade_status.value: OrderReplyConst.PostTradeStatus_BKD.value,
                MiddleOfficeColumns.sts.value: AllocationReportConst.AllocStatus_APP.value,
                MiddleOfficeColumns.match_status.value: ConfirmationReportConst.MatchStatus_UNM.value,
                MiddleOfficeColumns.client_comm.value: "0.5",
            },
            {
                OrderBookColumns.post_trade_status.value: post_trade_status,
                MiddleOfficeColumns.sts.value: status,
                MiddleOfficeColumns.match_status.value: match_status,
                MiddleOfficeColumns.client_comm.value: client_comm,
            },
            "Comparing Statuses after Book",
        )
        # endregion

        # region Step 2 - Approve block
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
                "AllocAccountID": self.account,
                "AllocQty": self.qty,
                "AvgPx": "0.1",
                "InstrID": self.data_set.get_instrument_id_by_name("instrument_3"),
            },
        )
        responses = self.java_api_manager.send_message_and_receive_response(self.confirmation_request)
        class_name.print_message("ALLOCATE", responses)

        # Comparing values for Allocation after Allocate block
        conf_report_message = self.java_api_manager.get_last_message(
            ORSMessageType.ConfirmationReport.value
        ).get_parameters()["ConfirmationReportBlock"]
        self.java_api_manager.compare_values(
            {
                "ConfirmStatus": ConfirmationReportConst.ConfirmStatus_AFF.value,
                "MatchStatus": ConfirmationReportConst.MatchStatus_MAT.value,
            },
            conf_report_message,
            "Comparing values for Allocation after Allocate block",
        )

        # Check that Allocation has no commissions
        commission_is_absent = not JavaApiFields.ClientCommission.value in conf_report_message
        self.java_api_manager.compare_values({"ClientCommissionIsAbsent": True},
                                             {'ClientCommissionIsAbsent': commission_is_absent},
                                             "Check ClientCommission field")

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

    @staticmethod
    def print_message(message, responses):
        logger.info(message)
        for i in responses:
            logger.info(i)
            logger.info(i.get_parameters())
