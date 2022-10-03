from pathlib import Path
from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.environments.full_environment import FullEnvironment
from test_framework.win_gui_wrappers.fe_trading_constant import PricingButtonColor
from test_framework.win_gui_wrappers.forex.client_rates_tile import ClientRatesTile


class QAP_T2801(TestCase):
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.rates_tile = ClientRatesTile(self.test_id, self.session_id)
        self.client = self.data_set.get_client_tier_by_name("client_tier_1")
        self.symbol = self.data_set.get_symbol_by_name("symbol_1")
        self.instrument = self.symbol + "-Spot"

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region step 1
        self.rates_tile.crete_tile()
        self.rates_tile.modify_client_tile(instrument=self.instrument, client_tier=self.client)
        self.rates_tile.switch_to_tired()
        self.rates_tile.press_executable()
        self.rates_tile.check_color_of_executable_button(expected_color=str(PricingButtonColor.red_button.value))
        self.rates_tile.press_executable()
        self.rates_tile.check_color_of_executable_button(expected_color=str(PricingButtonColor.green_button.value))
        self.rates_tile.press_pricing()
        self.rates_tile.switch_to_sweepable()
        self.rates_tile.check_color_of_pricing_button(expected_color=str(PricingButtonColor.red_button.value))
        self.rates_tile.press_pricing()
        self.rates_tile.check_color_of_executable_button(expected_color=str(PricingButtonColor.green_button.value))
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.rates_tile.close_tile()
