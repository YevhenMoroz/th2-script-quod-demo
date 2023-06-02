import logging
import time
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
from test_framework.fix_wrappers.oms.FixMessageExecutionReportOMS import FixMessageExecutionReportOMS
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import OrderReplyConst, JavaApiFields, ConfirmationReportConst
from test_framework.java_api_wrappers.oms.ors_messges.AllocationInstructionOMS import AllocationInstructionOMS
from test_framework.java_api_wrappers.oms.ors_messges.ConfirmationOMS import ConfirmationOMS
from test_framework.java_api_wrappers.oms.ors_messges.ForceAllocInstructionStatusRequestOMS import (
    ForceAllocInstructionStatusRequestOMS,
)
from test_framework.rest_api_wrappers.RestApiManager import RestApiManager
from test_framework.rest_api_wrappers.oms.RestApiModifyInstitutionMessage import RestApiModifyInstitutionMessage
from test_framework.ssh_wrappers.ssh_client import SshClient

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

seconds, nanos = timestamps()  # Test case start time


def print_message(message, responses):
    logger.info(message)
    for i in responses:
        logger.info(i)
        logger.info(i.get_parameters())


class QAP_T6900(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        # region Declarations
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.wa_connectivity = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.ss_connectivity = self.fix_env.sell_side
        self.qty = "100"
        self.price = "20"
        self.alloc_account = "AltAccount"
        self.client = self.data_set.get_client("client_pt_1")  # MOClient
        self.venue_client_name = self.data_set.get_venue_client_names_by_name("client_pt_1_venue_1")  # MOClient_PARIS
        self.ex_destination = self.data_set.get_mic_by_name("mic_1")  # "XPAR"
        self.fix_manager = FixManager(self.ss_connectivity, self.test_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set)
        self.fix_verifier = FixVerifier(self.fix_env.sell_side, self.test_id)
        self.execution_report = FixMessageExecutionReportOMS(self.data_set)
        self.rule_manager = RuleManager(sim=Simulators.equity)
        self.rest_api_manager = RestApiManager(session_alias=self.wa_connectivity, case_id=self.test_id)
        self.rest_institution_message = RestApiModifyInstitutionMessage(self.data_set)
        self.java_api = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api, self.test_id)
        self.allocation_instruction = AllocationInstructionOMS(self.data_set)
        self.approve_request = ForceAllocInstructionStatusRequestOMS(self.data_set)
        self.confirmation_request = ConfirmationOMS(self.data_set)
        self.ssh_client_env = self.environment.get_list_ssh_client_environment()[0]
        self.ssh_client = SshClient(self.ssh_client_env.host, self.ssh_client_env.port, self.ssh_client_env.user,
                                    self.ssh_client_env.password, self.ssh_client_env.su_user,
                                    self.ssh_client_env.su_password)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Precondition - Update Institution via RestApi, enable "Enable Unknown Accounts"
        self.rest_institution_message.modify_enable_unknown_accounts(True)
        self.rest_api_manager.send_post_request(self.rest_institution_message)
        self.ssh_client.send_command("qrestart ORS")
        time.sleep(30)
        # endregion

        # region Step 1-4 - Creating a DMA order and its execution with 79 tag
        try:
            trade_rule = self.rule_manager.add_NewOrdSingleExecutionReportTrade_FIXStandard(
                self.fix_env.buy_side,
                self.venue_client_name,
                self.ex_destination,
                float(self.price),
                int(self.qty),
                delay=0,
            )
            no_allocs: dict = {"NoAllocs": [{"AllocAccount": self.alloc_account, "AllocQty": self.qty}]}
            self.fix_message.set_default_dma_limit()
            self.fix_message.change_parameters(
                {
                    "Side": "1",
                    "OrderQtyData": {"OrderQty": self.qty},
                    "Account": self.client,
                    "Price": self.price,
                    "PreAllocGrp": no_allocs,
                }
            )
            response = self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message)
            # get Client Order ID and Order ID
            order_id: str = response[0].get_parameters()["OrderID"]
            cl_ord_id: str = response[0].get_parameters()["ClOrdID"]

        except Exception as e:
            logger.error(f"{e}", exc_info=True)

        finally:
            time.sleep(2)
            self.rule_manager.remove_rule(trade_rule)
        # endregion

        # region Checking Execution report
        self.execution_report.set_default_filled(self.fix_message)
        self.execution_report.change_parameters({"Account": self.alloc_account})
        list_of_ignored_fields: list = ["ReplyReceivedTime", "LastMkt", "Text", "Instrument", "GatingRuleCondName",
                                        "GatingRuleName", "SettlCurrency"]
        self.fix_verifier.check_fix_message_fix_standard(self.execution_report, ignored_fields=list_of_ignored_fields)
        # endregion

        # region Step 5 - Book order
        self.allocation_instruction.set_default_book(order_id)
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
            {
                JavaApiFields.PostTradeStatus.value: OrderReplyConst.PostTradeStatus_BKD.value,
                JavaApiFields.DoneForDay.value: OrderReplyConst.DoneForDay_YES.value,
            },
            order_update_reply,
            "Step 5 - Checking PostTradeStatus after Book",
        )

        # Checking AllocationReportBlock
        alloc_report_reply = self.java_api_manager.get_last_message(
            ORSMessageType.AllocationReport.value
        ).get_parameters()[JavaApiFields.AllocationReportBlock.value]
        alloc_id = alloc_report_reply["ClientAllocID"]
        self.java_api_manager.compare_values(
            {JavaApiFields.AllocStatus.value: "APP", JavaApiFields.MatchStatus.value: "UNM"},
            alloc_report_reply,
            "Step 5 - Checking Status and Match Status in MO after Book",
        )
        # endregion

        # region Step 6 - Approve
        self.approve_request.set_default_approve(alloc_id)
        responses = self.java_api_manager.send_message_and_receive_response(self.approve_request)
        print_message("APPROVE", responses)
        # endregion

        # region Step 6 - Allocate
        self.confirmation_request.set_default_allocation(alloc_id)
        self.confirmation_request.remove_fields_from_component("ConfirmationBlock", ["AllocAccountID"])
        self.confirmation_request.update_fields_in_component(
            "ConfirmationBlock",
            {
                "AllocFreeAccountID": self.alloc_account,
                "AllocQty": self.qty,
                "AvgPx": self.price,
                "InstrID": self.data_set.get_instrument_id_by_name("instrument_2"),
            },
        )
        responses = self.java_api_manager.send_message_and_receive_response(self.confirmation_request)
        print_message(f"ALLOCATE", responses)

        conf_report_reply = self.java_api_manager.get_last_message(
            ORSMessageType.ConfirmationReport.value
        ).get_parameters()[JavaApiFields.ConfirmationReportBlock.value]

        self.java_api_manager.compare_values(
            {
                JavaApiFields.AffirmStatus.value: ConfirmationReportConst.ConfirmStatus_AFF.value,
                JavaApiFields.MatchStatus.value: ConfirmationReportConst.MatchStatus_MAT.value,
                "AllocFreeAccountID": self.alloc_account,
                "AllocQty": str(float(self.qty)),
            },
            conf_report_reply,
            "Step 6 - Checking values for Allocation after Allocate block",
        )
        # endregion

        logger.info(f"Case {self.test_id} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.rest_institution_message.modify_enable_unknown_accounts(False)
        self.rest_api_manager.send_post_request(self.rest_institution_message)
        self.ssh_client.send_command("qrestart ORS")
