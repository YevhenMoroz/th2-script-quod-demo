import logging
from datetime import datetime
from pathlib import Path

from custom import basic_custom_actions as bca
from custom.basic_custom_actions import timestamps
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, AllocationReportConst, \
    ConfirmationReportConst
from test_framework.java_api_wrappers.oms.ors_messges.AllocationInstructionOMS import AllocationInstructionOMS
from test_framework.java_api_wrappers.oms.ors_messges.ConfirmationOMS import ConfirmationOMS
from test_framework.java_api_wrappers.oms.ors_messges.ForceAllocInstructionStatusRequestOMS import \
    ForceAllocInstructionStatusRequestOMS
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

seconds, nanos = timestamps()  # Test case start time


class QAP_T7082(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        # region Declarations
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.client = self.data_set.get_client('client_pt_1')
        self.rule_manager = RuleManager(Simulators.equity)
        self.java_api_connectivity = self.java_api = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.order_submit = OrderSubmitOMS(self.data_set)
        self.all_instr = AllocationInstructionOMS(self.data_set)
        self.approve = ForceAllocInstructionStatusRequestOMS(self.data_set)
        self.confirm = ConfirmationOMS(self.data_set)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region create order via fix (step 1 , 2)
        qty = '100'
        alloc_qty = "50"
        price = '20'
        new_order_rule = trade_rule = None
        venue = self.data_set.get_mic_by_name('mic_1')
        client = self.data_set.get_venue_client_names_by_name('client_pt_1_venue_1')
        self.order_submit.set_default_dma_limit()
        self.order_submit.update_fields_in_component("NewOrderSingleBlock", {"AccountGroupID": self.client,
                                                                             "PreTradeAllocationBlock": {
                                                                                 "PreTradeAllocationList": {
                                                                                     "PreTradeAllocAccountBlock": [{
                                                                                         'AllocFreeAccountID': "test1",
                                                                                         'AllocQty': alloc_qty}, {
                                                                                         'AllocFreeAccountID': "test2",
                                                                                         'AllocQty': alloc_qty}
                                                                                     ]}}})
        try:
            new_order_rule = self.rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(
                self.fix_env.buy_side, client, venue, float(price))
            trade_rule = self.rule_manager.add_NewOrdSingleExecutionReportTrade_FIXStandard(self.fix_env.buy_side,
                                                                                            client, venue, float(price),
                                                                                            int(qty), delay=0
                                                                                            )
            self.java_api_manager.send_message_and_receive_response(self.order_submit)
        except Exception as e:
            logger.error(f"{e}", exc_info=True, stack_info=True)
        finally:
            self.rule_manager.remove_rule(new_order_rule)
            self.rule_manager.remove_rule(trade_rule)
        # endregion
        # region book order
        order_id = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value][JavaApiFields.OrdID.value]
        self.all_instr.set_default_book(order_id)
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
        self.confirm.update_fields_in_component("ConfirmationBlock", {"AllocFreeAccountID": "test1","AllocQty": alloc_qty})
        self.java_api_manager.send_message_and_receive_response(self.confirm)
        confirm_report = \
            self.java_api_manager.get_last_message(ORSMessageType.ConfirmationReport.value, "test1").get_parameters()[
                JavaApiFields.ConfirmationReportBlock.value]
        expected_result_confirmation = {
            JavaApiFields.ConfirmStatus.value: ConfirmationReportConst.ConfirmStatus_AFF.value,
            JavaApiFields.MatchStatus.value: ConfirmationReportConst.MatchStatus_MAT.value,
            "AllocFreeAccountID": "test1"}
        actually_result = {
            JavaApiFields.ConfirmStatus.value: confirm_report[JavaApiFields.ConfirmStatus.value],
            JavaApiFields.MatchStatus.value: confirm_report[JavaApiFields.MatchStatus.value],
            "AllocFreeAccountID": confirm_report["AllocFreeAccountID"]}
        self.java_api_manager.compare_values(expected_result_confirmation, actually_result,
                                             'Check statuses of confirmation of test1')
        self.confirm.update_fields_in_component("ConfirmationBlock",
                                                {"AllocFreeAccountID": "test2", "AllocQty": alloc_qty})
        self.java_api_manager.send_message_and_receive_response(self.confirm)
        confirm_report = \
            self.java_api_manager.get_last_message(ORSMessageType.ConfirmationReport.value, "test2").get_parameters()[
                JavaApiFields.ConfirmationReportBlock.value]
        expected_result_confirmation = {
            JavaApiFields.ConfirmStatus.value: ConfirmationReportConst.ConfirmStatus_AFF.value,
            JavaApiFields.MatchStatus.value: ConfirmationReportConst.MatchStatus_MAT.value,
            "AllocFreeAccountID": "test2"}
        actually_result = {
            JavaApiFields.ConfirmStatus.value: confirm_report[JavaApiFields.ConfirmStatus.value],
            JavaApiFields.MatchStatus.value: confirm_report[JavaApiFields.MatchStatus.value],
            "AllocFreeAccountID": confirm_report["AllocFreeAccountID"]}
        self.java_api_manager.compare_values(expected_result_confirmation, actually_result,
                                             'Check statuses of confirmation of test2')
        # endregion
        logger.info(f"Case {self.test_id} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")
