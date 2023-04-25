import logging
from pathlib import Path

from custom import basic_custom_actions as bca
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.fix_wrappers.FixAllocationACK import FixAllocationACK
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, AllocationReportConst, \
    ConfirmationReportConst
from test_framework.java_api_wrappers.oms.ors_messges.AllocationInstructionOMS import AllocationInstructionOMS
from test_framework.java_api_wrappers.oms.ors_messges.ConfirmationOMS import ConfirmationOMS
from test_framework.java_api_wrappers.oms.ors_messges.FixAllocationInstructionOMS import FixAllocationInstructionOMS
from test_framework.java_api_wrappers.oms.ors_messges.ForceAllocInstructionStatusRequestOMS import \
    ForceAllocInstructionStatusRequestOMS
from test_framework.java_api_wrappers.ors_messages.CptyBlockRejectRequest import CptyBlockRejectRequest

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP_T7467(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.bs_connectivity = self.fix_env.buy_side
        self.fix_manager42 = FixManager(self.fix_env.sell_side_fix42, self.test_id)
        self.java_api_connectivity = self.java_api = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.fix_verifier = FixVerifier(self.fix_env.sell_side_fix42, self.test_id)
        self.all_instr = AllocationInstructionOMS(self.data_set)
        self.confirm = ConfirmationOMS(self.data_set)
        self.approve = ForceAllocInstructionStatusRequestOMS(self.data_set)
        self.fix_alloc = FixAllocationInstructionOMS(self.data_set)
        self.alloc_rej = CptyBlockRejectRequest()

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Precondition
        client = self.data_set.get_client_by_name("client_pt_8")
        account1 = self.data_set.get_account_by_name("client_pt_8_acc_1")
        venue_client = self.data_set.get_venue_client_names_by_name("client_pt_8_venue_1")
        mic = self.data_set.get_mic_by_name("mic_1")
        price = "10"
        change_params = {'Account': client, "Price": price}
        nos = FixMessageNewOrderSingleOMS(self.data_set).set_fix42_dma_limit().change_parameters(change_params)
        qty = nos.get_parameters()["OrderQty"]

        try:
            rule_manager = RuleManager(Simulators.equity)
            trade_rele = rule_manager.add_NewOrdSingleExecutionReportTrade_FIXStandard(self.bs_connectivity,
                                                                                       venue_client, mic,
                                                                                       int(price), int(qty), 0)
            self.fix_manager42.send_message_and_receive_response_fix_standard(nos)
        finally:
            rule_manager.remove_rule(trade_rele)

        ord_id = self.fix_manager42.get_last_message("ExecutionReport").get_parameter("OrderID")
        # endregion
        # region Step 1
        self.fix_alloc.set_default_preliminary(ord_id)
        self.fix_alloc.base_parameters["AllocationInstructionBlock"]["AllocAccountList"]["AllocAccountBlock"][0][
            "AllocClientAccountID"] = account1
        self.fix_alloc.base_parameters["AllocationInstructionBlock"]["ClientAccountGroupID"] = client
        self.java_api_manager.send_message_and_receive_response(self.fix_alloc)
        allocation_report = \
            self.java_api_manager.get_last_message(ORSMessageType.AllocationReport.value).get_parameters()[
                JavaApiFields.AllocationReportBlock.value]
        expected_result = ({JavaApiFields.AllocStatus.value: AllocationReportConst.AllocStatus_REC.value,
                            JavaApiFields.MatchStatus.value: ConfirmationReportConst.MatchStatus_UNM.value,
                            JavaApiFields.ConfirmationService.value: AllocationReportConst.ConfirmationService_INT.value,
                            JavaApiFields.AllocType.value: "P"})
        self.java_api_manager.compare_values(expected_result, allocation_report, 'Step 1')
        fix_alloc_id1 = allocation_report["AllocInstructionID"]
        # endregion
        # region Step 2-3
        self.alloc_rej.set_default(fix_alloc_id1)
        self.java_api_manager.send_message_and_receive_response(self.alloc_rej)
        allocation_report = \
            self.java_api_manager.get_last_message(ORSMessageType.AllocationReport.value).get_parameters()[
                JavaApiFields.AllocationReportBlock.value]
        expected_result = ({"AllocReportType": "REJ", JavaApiFields.AllocStatus.value: "REJ"})
        self.java_api_manager.compare_values(expected_result, allocation_report, 'Step 2-3')
        # endregion
