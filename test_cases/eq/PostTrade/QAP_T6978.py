import logging
import time
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
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, AllocationReportConst, \
    ConfirmationReportConst
from test_framework.java_api_wrappers.oms.ors_messges.AllocationInstructionOMS import AllocationInstructionOMS
from test_framework.java_api_wrappers.oms.ors_messges.ConfirmationOMS import ConfirmationOMS
from test_framework.java_api_wrappers.oms.ors_messges.ForceAllocInstructionStatusRequestOMS import \
    ForceAllocInstructionStatusRequestOMS
from test_framework.java_api_wrappers.ors_messages.BlockChangeConfirmationServiceRequest import \
    BlockChangeConfirmationServiceRequest
from test_framework.rest_api_wrappers.RestApiManager import RestApiManager
from test_framework.rest_api_wrappers.oms.RestApiModifyInstitutionMessage import RestApiModifyInstitutionMessage
from test_framework.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

seconds, nanos = timestamps()  # Test case start time


class QAP_T6978(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        # region Declarations
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.rest_api_connectivity = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.ss_connectivity = self.fix_env.sell_side
        self.qty = '100'
        self.price = '10'
        self.client = self.data_set.get_client('client_pt_9')
        self.venue_client_name = self.data_set.get_venue_client_names_by_name('client_pt_9_venue_1')
        self.account = self.data_set.get_account_by_name("client_pt_9_acc_1")
        self.ex_destination = self.data_set.get_mic_by_name('mic_1')
        self.fix_manager = FixManager(self.ss_connectivity, self.test_id)
        self.client_inbox = OMSClientInbox(self.test_id, self.session_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set)
        self.fix_verifier = FixVerifier(self.fix_env.drop_copy, self.test_id)
        self.execution_report = FixMessageExecutionReportOMS(self.data_set)
        self.rule_manager = RuleManager(Simulators.equity)
        self.wa_connectivity = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.api_manager = RestApiManager(self.wa_connectivity, self.test_id)
        self.java_api = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api, self.test_id)
        self.rest_institution_message = RestApiModifyInstitutionMessage(self.data_set)
        self.book_request = AllocationInstructionOMS(self.data_set)
        self.approve_request = ForceAllocInstructionStatusRequestOMS(self.data_set)
        self.alloc_request = ConfirmationOMS(self.data_set)
        self.change_confirm = BlockChangeConfirmationServiceRequest()
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Precondition
        self.fix_message.set_default_dma_limit()
        self.fix_message.change_parameters(
            {'Side': '1', 'OrderQtyData': {'OrderQty': self.qty}, 'Account': self.client, 'Price': self.price})
        trade_rule = False
        try:
            trade_rule = self.rule_manager.add_NewOrdSingleExecutionReportTrade_FIXStandard(self.fix_env.buy_side,
                                                                                            self.venue_client_name,
                                                                                            self.ex_destination,
                                                                                            float(self.price),
                                                                                            int(self.qty), delay=0
                                                                                            )
            self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message)
            exex_rep = self.fix_manager.get_last_message("ExecutionReport").get_parameters()
            order_id = exex_rep["OrderID"]
        except Exception as e:
            logger.error(f'{e}', exc_info=True)

        finally:
            time.sleep(3)
            self.rule_manager.remove_rule(trade_rule)
        # endregion

        # region Step 1
        self.book_request.set_default_book(order_id)
        self.book_request.update_fields_in_component("AllocationInstructionBlock",
                                                     {"InstrID": self.data_set.get_instrument_id_by_name(
                                                         "instrument_2"), "AccountGroupID": self.client})
        self.java_api_manager.send_message_and_receive_response(self.book_request)
        allocation_report = \
            self.java_api_manager.get_last_message(ORSMessageType.AllocationReport.value).get_parameters()[
                JavaApiFields.AllocationReportBlock.value]
        alloc_id = allocation_report[JavaApiFields.ClientAllocID.value]
        self.java_api_manager.compare_values(
            {JavaApiFields.AllocStatus.value: AllocationReportConst.AllocStatus_APP.value,
             JavaApiFields.MatchStatus.value: ConfirmationReportConst.MatchStatus_UNM.value},
            allocation_report, 'Check booking')
        # endregion
        # region Step 2
        self.approve_request.set_default_approve(alloc_id)
        self.java_api_manager.send_message_and_receive_response(self.approve_request)
        expected_result = {JavaApiFields.AllocStatus.value: AllocationReportConst.AllocStatus_REC.value,
                           JavaApiFields.MatchStatus.value: ConfirmationReportConst.MatchStatus_UNM.value}
        allocation_report = \
            self.java_api_manager.get_last_message(ORSMessageType.AllocationReport.value).get_parameters()[
                JavaApiFields.AllocationReportBlock.value]
        actually_result = {JavaApiFields.AllocStatus.value: allocation_report[JavaApiFields.AllocStatus.value],
                           JavaApiFields.MatchStatus.value: allocation_report[JavaApiFields.MatchStatus.value]}
        self.java_api_manager.compare_values(expected_result, actually_result, 'Check approve')
        # endregion
        # region Step 3
        self.change_confirm.set_default(alloc_id)
        self.java_api_manager.send_message(self.change_confirm)
        # endregion
        # region Step 4
        self.approve_request.set_default_approve(alloc_id)
        self.java_api_manager.send_message_and_receive_response(self.approve_request)
        expected_result = {JavaApiFields.AllocStatus.value: AllocationReportConst.AllocStatus_ACK.value,
                           JavaApiFields.MatchStatus.value: ConfirmationReportConst.MatchStatus_MAT.value}
        allocation_report = \
            self.java_api_manager.get_last_message(ORSMessageType.AllocationReport.value).get_parameters()[
                JavaApiFields.AllocationReportBlock.value]
        actually_result = {JavaApiFields.AllocStatus.value: allocation_report[JavaApiFields.AllocStatus.value],
                           JavaApiFields.MatchStatus.value: allocation_report[JavaApiFields.MatchStatus.value]}
        self.java_api_manager.compare_values(expected_result, actually_result, 'Check approve 2')

        self.alloc_request.set_default_allocation(alloc_id)
        self.alloc_request.update_fields_in_component("ConfirmationBlock", {
            "AllocAccountID": self.account, "InstrID": self.data_set.get_instrument_id_by_name("instrument_2")})
        self.java_api_manager.send_message_and_receive_response(self.alloc_request)
        confirm_report = \
            self.java_api_manager.get_last_message(ORSMessageType.ConfirmationReport.value).get_parameters()[
                JavaApiFields.ConfirmationReportBlock.value]
        expected_result_confirmation = {
            JavaApiFields.ConfirmStatus.value: ConfirmationReportConst.ConfirmStatus_AFF.value,
            JavaApiFields.MatchStatus.value: ConfirmationReportConst.MatchStatus_MAT.value}
        actually_result = {
            JavaApiFields.ConfirmStatus.value: confirm_report[JavaApiFields.ConfirmStatus.value],
            JavaApiFields.MatchStatus.value: confirm_report[JavaApiFields.MatchStatus.value]}
        self.java_api_manager.compare_values(expected_result_confirmation, actually_result,
                                             f'Check statuses of confirmation of {self.account}')
        # endregion