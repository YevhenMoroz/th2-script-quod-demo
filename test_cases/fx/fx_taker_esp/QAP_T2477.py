import time
from pathlib import Path

from rule_management import RuleManager
from test_framework.data_sets.constants import GatewaySide, Status, DirectionEnum
from custom.tenor_settlement_date import spo
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.environments.full_environment import FullEnvironment
from custom import basic_custom_actions as bca
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.forex.FixMessageExecutionReportAlgoFX import FixMessageExecutionReportAlgoFX
from test_framework.fix_wrappers.forex.FixMessageExternalExecutionReport import FixMessageExternalExecutionReport
from test_framework.fix_wrappers.forex.FixMessageMarketDataSnapshotFullRefreshBuyFX import \
    FixMessageMarketDataSnapshotFullRefreshBuyFX
from test_framework.fix_wrappers.forex.FixMessageNewOrderSingleTaker import FixMessageNewOrderSingleTaker


class QAP_T2477(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.external_check_connectivity = self.environment.get_list_fix_environment()[0].external_validation
        self.esp_t_connectivity = self.environment.get_list_fix_environment()[0].buy_side_esp
        self.fx_fh_connectivity = self.environment.get_list_fix_environment()[0].feed_handler
        self.fix_md = FixMessageMarketDataSnapshotFullRefreshBuyFX()
        self.fix_manager = FixManager(self.esp_t_connectivity, self.test_id)
        self.fix_manager_fh_314 = FixManager(self.fx_fh_connectivity, self.test_id)
        self.fix_verifier = FixVerifier(self.external_check_connectivity, self.test_id)
        self.new_order_single = FixMessageNewOrderSingleTaker(data_set=self.data_set)
        self.execution_report = FixMessageExecutionReportAlgoFX()
        self.execution_report = FixMessageExecutionReportAlgoFX()
        self.external_execution_report = FixMessageExternalExecutionReport()
        self.rm = RuleManager()

        self.reject = Status.Reject
        self.no_strategy_parameters = [{"StrategyParameterName": "AllowedVenues", "StrategyParameterType": "14",
                                        "StrategyParameterValue": "BNP"}]

        self.aspect_db = "ASPECT_DB"
        self.rule_list = []

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Precondition
        eva_rule = self.rm.add_External_Reject("fix-buy-extern-314-stand")
        self.rule_list = [eva_rule]
        self.sleep(3)
        # region 3
        self.new_order_single.set_default_mo()
        self.new_order_single.change_parameters(
            {"Account": self.aspect_db, "ExDestination": "BNP-SW"})
        self.fix_manager.send_message_and_receive_response(self.new_order_single)
        # endregion
        # region 4-5
        self.execution_report.set_params_from_new_order_single(self.new_order_single, status=self.reject)
        self.execution_report.remove_fields_from_component("Instrument",
                                                           ["SecurityType", "Product", "SecurityExchange"])
        self.execution_report.remove_parameters(
            ["SettlCurrency", "SettlDate", "HandlInst", "NoParty", "OrdType", "Text", "LastMkt", "OrderCapacity",
             "QtyType", "ExecRestatementReason", "SettlType", "TargetStrategy"])
        self.execution_report.change_parameter("LeavesQty", "1000000")
        self.fix_verifier.check_fix_message(fix_message=self.execution_report, direction=DirectionEnum.ToQuod)
        # endregion
        time.sleep(3)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.rm = RuleManager()
        self.rm.remove_rules(self.rule_list)
