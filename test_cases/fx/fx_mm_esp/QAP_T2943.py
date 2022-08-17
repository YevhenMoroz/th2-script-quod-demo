from pathlib import Path
from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.environments.full_environment import FullEnvironment
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.forex.FixMessageMarketDataSnapshotFullRefreshBuyFX import \
    FixMessageMarketDataSnapshotFullRefreshBuyFX
from test_framework.win_gui_wrappers.fe_trading_constant import ClientPrisingTileAction, PriceNaming, RatesColumnNames
from test_framework.win_gui_wrappers.forex.client_rates_tile import ClientRatesTile


class QAP_T2943(TestCase):
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.rates_tile = ClientRatesTile(self.test_id, self.session_id)
        self.silver = self.data_set.get_client_tier_by_name("client_tier_1")
        self.gbp_usd = self.data_set.get_symbol_by_name("symbol_2")
        self.gbp_usd_spot = self.gbp_usd + "-Spot"
        self.ask_base = RatesColumnNames.ask_base
        self.bid_base = RatesColumnNames.bid_base
        self.spread = PriceNaming.spread
        self.expected_bid_base = "1.1"
        self.expected_ask_base = "1.2"
        self.expected_spread = "2.1"
        self.bid_base_event = "bid_base_validation"
        self.ask_base_event = "ask_base_validation"
        self.spread_validation = "spread_validation"

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region step 2
        self.rates_tile.crete_tile()
        self.rates_tile.modify_client_tile(instrument=self.gbp_usd_spot, client_tier=self.silver)
        self.rates_tile.press_use_default()

        row_values = self.rates_tile.extract_values_from_rates(self.bid_base, self.ask_base)
        actual_bid_base = row_values[str(self.bid_base)]
        actual_ask_base = row_values[str(self.ask_base)]
        self.rates_tile.compare_values(self.expected_bid_base, actual_bid_base,
                                       event_name=self.bid_base_event)
        self.rates_tile.compare_values(self.expected_ask_base, actual_ask_base,
                                       event_name=self.ask_base_event)

        tob_values = self.rates_tile.extract_prices_from_tile(self.spread)
        actual_spread = tob_values[self.spread.value]
        self.rates_tile.compare_values(self.expected_spread, actual_spread,
                                       event_name=self.spread_validation)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.rates_tile.close_tile()
