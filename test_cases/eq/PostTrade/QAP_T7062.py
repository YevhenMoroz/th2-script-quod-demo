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
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, AllocationReportConst, \
    ConfirmationReportConst
from test_framework.java_api_wrappers.oms.ors_messges.AllocationInstructionOMS import AllocationInstructionOMS
from test_framework.java_api_wrappers.oms.ors_messges.ConfirmationOMS import ConfirmationOMS
from test_framework.java_api_wrappers.oms.ors_messges.ForceAllocInstructionStatusRequestOMS import \
    ForceAllocInstructionStatusRequestOMS

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

seconds, nanos = timestamps()  # Test case start time


class QAP_T7062(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        # region Declarations
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.ss_connectivity = self.fix_env.sell_side
        self.bs_connectivity = self.fix_env.buy_side
        self.qty = '100'
        self.price = '20'
        self.rule_manager = RuleManager(sim=Simulators.equity)
        self.venue_client_names = self.data_set.get_venue_client_names_by_name('client_pt_1_venue_1')  # MOClient_PARIS
        self.venue = self.data_set.get_mic_by_name('mic_1')  # XPAR
        self.client = self.data_set.get_client('client_pt_1')  # MOClient
        self.alloc_account = self.data_set.get_account_by_name('client_pt_1_acc_1')  # MOClient_SA1
        self.alt_account = 'test'
        self.fix_manager = FixManager(self.ss_connectivity, self.test_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set)
        self.exec_destination = self.data_set.get_mic_by_name('mic_1')
        self.account_ven = self.data_set.get_venue_client_names_by_name('client_pt_1_venue_1')
        self.rule_manager = RuleManager(Simulators.equity)
        self.trade_rule = None
        self.new_order_single_rule = None
        self.java_api_connectivity = self.java_api = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.all_instr = AllocationInstructionOMS(self.data_set)
        self.approve = ForceAllocInstructionStatusRequestOMS(self.data_set)
        self.confirm = ConfirmationOMS(self.data_set)
        self.account = self.data_set.get_account_by_name('client_pt_1_acc_1')
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Create CO via FIX
        self.fix_message.set_default_dma_limit()
        self.fix_message.change_parameters(
            {'OrderQtyData': {'OrderQty': self.qty}, 'Account': self.client})
        try:
            self.new_order_single_rule = self.rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(
                self.fix_env.buy_side, self.account_ven, self.exec_destination, float(self.price))
            self.trade_rule = self.rule_manager.add_NewOrdSingleExecutionReportTrade_FIXStandard(self.fix_env.buy_side,
                                                                                                 self.account_ven,
                                                                                                 self.exec_destination,
                                                                                                 float(self.price),
                                                                                                 int(self.qty), 0)
            response = self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message)
            order_id = response[0].get_parameter("OrderID")
        except Exception as ex:
            logger.exception(f'{ex} - your exception')
        finally:
            self.rule_manager.remove_rule(self.trade_rule)
            self.rule_manager.remove_rule(self.new_order_single_rule)

        # endregion

        # region book order
        self.all_instr.set_default_book(order_id)
        self.all_instr.update_fields_in_component("AllocationInstructionBlock",
                                                  {"InstrID": self.data_set.get_instrument_id_by_name(
                                                      "instrument_2")})
        self.java_api_manager.send_message_and_receive_response(self.all_instr)
        allocation_report = \
            self.java_api_manager.get_last_message(ORSMessageType.AllocationReport.value).get_parameters()[
                JavaApiFields.AllocationReportBlock.value]
        alloc_id = allocation_report[JavaApiFields.ClientAllocID.value]
        expected_result = ({JavaApiFields.AllocStatus.value: AllocationReportConst.AllocStatus_APP.value,
                            JavaApiFields.MatchStatus.value: ConfirmationReportConst.MatchStatus_UNM.value})
        actually_result = {JavaApiFields.AllocStatus.value: allocation_report[JavaApiFields.AllocStatus.value],
                           JavaApiFields.MatchStatus.value: allocation_report[JavaApiFields.MatchStatus.value]}
        self.java_api_manager.compare_values(expected_result, actually_result, 'Check booking')
        # endregion
        # region approve block
        self.approve.set_default_approve(alloc_id)
        self.java_api_manager.send_message_and_receive_response(self.approve)
        expected_result.update({JavaApiFields.AllocStatus.value: AllocationReportConst.AllocStatus_ACK.value,
                                JavaApiFields.MatchStatus.value: ConfirmationReportConst.MatchStatus_MAT.value})
        allocation_report = \
            self.java_api_manager.get_last_message(ORSMessageType.AllocationReport.value).get_parameters()[
                JavaApiFields.AllocationReportBlock.value]
        actually_result = {JavaApiFields.AllocStatus.value: allocation_report[JavaApiFields.AllocStatus.value],
                           JavaApiFields.MatchStatus.value: allocation_report[JavaApiFields.MatchStatus.value]}
        self.java_api_manager.compare_values(expected_result, actually_result, 'Check approve')
        # endregion
        # region allocate block
        self.confirm.set_default_allocation(alloc_id)
        self.confirm.update_fields_in_component("ConfirmationBlock", {"AllocAccountID": self.account,
                                                                      "AllocFreeAccountID": "test",
                                                                      "InstrID": self.data_set.get_instrument_id_by_name(
                                                                          "instrument_2")})
        self.java_api_manager.send_message_and_receive_response(self.confirm)
        confirm_report = \
            self.java_api_manager.get_last_message(ORSMessageType.ConfirmationReport.value).get_parameters()[
                JavaApiFields.ConfirmationReportBlock.value]
        expected_result_confirmation = {
            JavaApiFields.ConfirmStatus.value: ConfirmationReportConst.ConfirmStatus_AFF.value,
            JavaApiFields.MatchStatus.value: ConfirmationReportConst.MatchStatus_MAT.value,
            "AllocFreeAccountID": "test"}
        actually_result = {
            JavaApiFields.ConfirmStatus.value: confirm_report[JavaApiFields.ConfirmStatus.value],
            JavaApiFields.MatchStatus.value: confirm_report[JavaApiFields.MatchStatus.value],
            "AllocFreeAccountID": confirm_report["AllocFreeAccountID"]}
        self.java_api_manager.compare_values(expected_result_confirmation, actually_result,
                                             f'Check statuses of confirmation of {self.account}')
        # endregion
        logger.info(f"Case {self.test_id} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")
