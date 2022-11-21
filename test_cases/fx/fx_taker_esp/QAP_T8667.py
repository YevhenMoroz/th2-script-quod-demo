from pathlib import Path
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from custom import basic_custom_actions as bca
from test_framework.environments.full_environment import FullEnvironment
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.forex.FixMessageExecutionReportAlgoFX import FixMessageExecutionReportAlgoFX
from test_framework.fix_wrappers.forex.FixMessageNewOrderSingleTaker import FixMessageNewOrderSingleTaker


class QAP_T8667(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.esp_t_connectivity = self.environment.get_list_fix_environment()[0].buy_side_esp
        self.fix_manager = FixManager(self.esp_t_connectivity, self.test_id)
        self.fix_verifier = FixVerifier(self.esp_t_connectivity, self.test_id)
        self.new_order = FixMessageNewOrderSingleTaker(data_set=self.data_set)
        self.execution_report = FixMessageExecutionReportAlgoFX()
        self.venue_city = self.data_set.get_venue_by_name("venue_1")
        self.market_citi = "CITI-ID"
        self.venue_d3 = self.data_set.get_venue_by_name("venue_9")
        self.qty = "10000000"
        self.no_strategy_parameters = [{"StrategyParameterName": "AllowedVenues", "StrategyParameterType": "14",
                                        "StrategyParameterValue": f"{self.venue_city}/{self.venue_d3}"}]

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Step 1
        self.new_order.set_default_SOR().update_repeating_group("NoStrategyParameters", self.no_strategy_parameters)
        self.new_order.change_parameter("OrderQty", self.qty)
        response = self.fix_manager.send_message_and_receive_response(self.new_order)
        # endregion
        # regions Step 2
        self.execution_report.set_params_from_new_order_single(self.new_order, response=response[-1])
        self.execution_report.change_parameters({"LastMkt": self.market_citi})
        self.fix_verifier.check_fix_message(self.execution_report)
        # endregion
