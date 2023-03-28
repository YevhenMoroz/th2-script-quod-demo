import logging
from pathlib import Path

from custom import basic_custom_actions as bca
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.oms.FixMessageAllocationInstructionReportOMS import \
    FixMessageAllocationInstructionReportOMS
from test_framework.fix_wrappers.oms.FixMessageConfirmationReportOMS import FixMessageConfirmationReportOMS
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


class QAP_T7188(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.ss_connectivity = self.fix_env.sell_side
        self.bs_connectivity = self.fix_env.buy_side
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.java_api_connectivity = self.java_api = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.all_instr = AllocationInstructionOMS(self.data_set)
        self.approve = ForceAllocInstructionStatusRequestOMS(self.data_set)
        self.confirm = ConfirmationOMS(self.data_set)
        self.alloc_report = FixMessageAllocationInstructionReportOMS()
        self.conf_report = FixMessageConfirmationReportOMS(self.data_set)
        self.dc_connectivity = self.fix_env.drop_copy
        self.fix_verifier_dc = FixVerifier(self.dc_connectivity, self.test_id)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Variables
        client = self.data_set.get_client_by_name("client_pt_1")
        account1 = self.data_set.get_account_by_name("client_pt_1_acc_1")
        account2 = self.data_set.get_account_by_name("client_pt_1_acc_2")
        venue_client = self.data_set.get_venue_client_names_by_name("client_pt_1_venue_1")
        mic = self.data_set.get_mic_by_name("mic_1")
        # endregion
        # region Create care order
        change_params = {'Account': client}
        nos = FixMessageNewOrderSingleOMS(self.data_set).set_default_dma_limit().change_parameters(change_params)
        qty = nos.get_parameters()["OrderQtyData"]["OrderQty"]
        price = nos.get_parameters()["Price"]
        try:
            rule_manager = RuleManager(Simulators.equity)
            new_order_single_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(
                self.fix_env.buy_side, venue_client, mic, float(price))
            trade_rele = rule_manager.add_NewOrdSingleExecutionReportTrade_FIXStandard(self.bs_connectivity,
                                                                                       venue_client, mic,
                                                                                       int(price),
                                                                                       int(qty), 0)
            response = self.fix_manager.send_message_and_receive_response_fix_standard(nos)
        finally:
            rule_manager.remove_rules([new_order_single_rule, trade_rele])
        # endregion
        # region book order
        order_id = response[0].get_parameters()['OrderID']
        self.all_instr.set_default_book(order_id)
        self.all_instr.update_fields_in_component("AllocationInstructionBlock",
                                                  {"InstrID": self.data_set.get_instrument_id_by_name(
                                                      "instrument_2"),
                                                      "AccountGroupID": client,
                                                      "AvgPx": price})
        self.java_api_manager.send_message_and_receive_response(self.all_instr)
        allocation_report = \
            self.java_api_manager.get_last_message(ORSMessageType.AllocationReport.value).get_parameters()[
                JavaApiFields.AllocationReportBlock.value]
        alloc_id = allocation_report[JavaApiFields.ClientAllocID.value]

        alloc_ignored_fields = ['Account', 'tag5120', 'Currency', 'RootCommTypeClCommBasis',
                                'RootOrClientCommission', 'RootOrClientCommissionCurrency', 'RootSettlCurrAmt','tag11245']
        self.alloc_report.set_default_ready_to_book(nos)
        self.fix_verifier_dc.check_fix_message_fix_standard(self.alloc_report, ignored_fields=alloc_ignored_fields)
        # endregion
        # region approve block
        self.approve.set_default_approve(alloc_id)
        self.java_api_manager.send_message_and_receive_response(self.approve)
        expected_result = {JavaApiFields.AllocStatus.value: AllocationReportConst.AllocStatus_ACK.value,
                           JavaApiFields.MatchStatus.value: ConfirmationReportConst.MatchStatus_MAT.value}
        allocation_report = \
            self.java_api_manager.get_last_message(ORSMessageType.AllocationReport.value).get_parameters()[
                JavaApiFields.AllocationReportBlock.value]
        actually_result = {JavaApiFields.AllocStatus.value: allocation_report[JavaApiFields.AllocStatus.value],
                           JavaApiFields.MatchStatus.value: allocation_report[JavaApiFields.MatchStatus.value]}
        self.java_api_manager.compare_values(expected_result, actually_result, 'Check approve')
        # endregion
        # region allocate block acc1
        self.confirm.set_default_allocation(alloc_id)
        self.confirm.update_fields_in_component("ConfirmationBlock", {"AllocAccountID": account1,
                                                                      "InstrID": self.data_set.get_instrument_id_by_name(
                                                                          "instrument_2"),
                                                                      "AllocQty": "50",
                                                                      "AvgPx": "15"})
        self.java_api_manager.send_message_and_receive_response(self.confirm)
        alloc_ignored_fields = ['tag5120', 'CommissionData','tag11245']
        self.conf_report.set_default_confirmation_new(nos)
        self.conf_report.change_parameters(
            {"AllocQty": "50", "AllocAccount": account1, "AvgPx": "15",
             "Currency": "*", "tag5120": "*"})
        self.fix_verifier_dc.check_fix_message_fix_standard(self.conf_report, ignored_fields=alloc_ignored_fields,
                                                            key_parameters=["AllocAccount"])
        # endregion
        # region allocate block acc2
        self.confirm.set_default_allocation(alloc_id)
        self.confirm.update_fields_in_component("ConfirmationBlock", {"AllocAccountID": account2,
                                                                      "InstrID": self.data_set.get_instrument_id_by_name(
                                                                          "instrument_2"),
                                                                      "AllocQty": "50",
                                                                      "AvgPx": "25"})
        self.java_api_manager.send_message_and_receive_response(self.confirm)
        self.conf_report.change_parameters({"AllocAccount": account2, "AvgPx": "25"})
        self.fix_verifier_dc.check_fix_message_fix_standard(self.conf_report, ignored_fields=alloc_ignored_fields,
                                                            key_parameters=["AllocAccount"])
        # endregion
