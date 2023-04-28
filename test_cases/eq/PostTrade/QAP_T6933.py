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
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields
from test_framework.java_api_wrappers.oms.ors_messges.FixAllocationInstructionOMS import FixAllocationInstructionOMS

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP_T6933(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.bs_connectivity = self.fix_env.buy_side
        self.fix_manager42 = FixManager(self.fix_env.sell_side_fix42, self.test_id)
        self.java_api_connectivity = self.java_api = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.fix_alloc = FixAllocationInstructionOMS(self.data_set)
        self.fix_verifier = FixVerifier(self.fix_env.sell_side_fix42, self.test_id)
        self.alloc_ack = FixAllocationACK()

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Precondition
        client = self.data_set.get_client_by_name("client_pt_8")
        account1 = "DUMMY_AKK"
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
        self.java_api_manager.send_message_and_receive_response(self.fix_alloc)
        alloc_report = self.java_api_manager.get_last_message(ORSMessageType.AllocationReport.value).get_parameter(
            JavaApiFields.AllocationReportBlock.value)
        self.java_api_manager.compare_values({"AllocAccountID": "DummyAccount"}, alloc_report["AllocAccountList"][
            "AllocAccountBlock"][0], "Step 1")
        # endregion
        # region Step 2
        alloc_id = self.fix_alloc.get_parameter("AllocationInstructionBlock")["ClientAllocID"]
        self.alloc_ack.set_default(alloc_id, "3")
        self.fix_verifier.check_fix_message(self.alloc_ack, message_name="Step 2")
        # endregion
