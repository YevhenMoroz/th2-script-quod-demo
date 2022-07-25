from pathlib import Path
from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.environments.full_environment import FullEnvironment
from test_framework.win_gui_wrappers.fe_trading_constant import PriceNaming
from test_framework.win_gui_wrappers.forex.client_rates_tile import ClientRatesTile


class QAP_1601(TestCase):
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.ask_pips = PriceNaming.ask_pips
        self.bid_pips = PriceNaming.bid_pips
        self.spread = PriceNaming.spread
        self.rates_tile = ClientRatesTile(self.test_id, self.session_id)
        self.silver = self.data_set.get_client_tier_by_name("client_tier_1")
        self.eur_usd = self.data_set.get_symbol_by_name("symbol_1")
        self.eur_usd_spot = self.eur_usd + "-Spot"
        self.spread_event = "Spread validation"

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region step 1
        self.rates_tile.crete_tile()
        self.rates_tile.modify_client_tile(instrument=self.eur_usd_spot, client_tier=self.silver)
        self.rates_tile.press_use_default()
        bid_n_ask_values = self.rates_tile.extract_prices_from_tile(self.bid_pips, self.ask_pips)
        actual_spread = self.rates_tile.extract_prices_from_tile(self.spread)[self.spread.value]
        expected_spread = str(
            round((float(bid_n_ask_values[self.bid_pips.value]) - float(bid_n_ask_values[self.ask_pips.value])) * -0.1, 1))
        self.rates_tile.compare_values(expected_spread, actual_spread,
                                       event_name=self.spread_event)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.rates_tile.close_tile()
