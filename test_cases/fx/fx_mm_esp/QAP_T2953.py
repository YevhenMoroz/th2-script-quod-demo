from pathlib import Path
from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.environments.full_environment import FullEnvironment
from test_framework.win_gui_wrappers.fe_trading_constant import ClientPrisingTileAction, PriceNaming
from test_framework.win_gui_wrappers.forex.client_rates_tile import ClientRatesTile


class QAP_T2953(TestCase):
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.rates_tile = ClientRatesTile(self.test_id, self.session_id)

        self.client = self.data_set.get_client_tier_by_name("client_tier_1")
        self.symbol = self.data_set.get_symbol_by_name("symbol_1")
        self.instrument = self.symbol + "-Spot"

        self.use_defaults_check_event = "Use Defaults validation"
        self.pips_1 = "1"
        self.ask_pips = PriceNaming.ask_pips
        self.bid_pips = PriceNaming.bid_pips
        self.widen_spread = ClientPrisingTileAction.widen_spread

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region step 1
        self.rates_tile.crete_tile()
        self.rates_tile.modify_client_tile(instrument=self.instrument, client_tier=self.client)
        self.rates_tile.press_use_default()

        bid_n_ask_values = self.rates_tile.extract_prices_from_tile(self.bid_pips, self.ask_pips)
        initial_bid = bid_n_ask_values[self.bid_pips.value]

        self.rates_tile.modify_client_tile(pips=self.pips_1)
        self.rates_tile.modify_spread(self.widen_spread)

        self.rates_tile.press_use_default()
        bid_n_ask_values = self.rates_tile.extract_prices_from_tile(self.bid_pips, self.ask_pips)
        eventual_bid = bid_n_ask_values[self.bid_pips.value]

        self.rates_tile.compare_values(initial_bid, eventual_bid,
                                       event_name=self.use_defaults_check_event)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.rates_tile.close_tile()
