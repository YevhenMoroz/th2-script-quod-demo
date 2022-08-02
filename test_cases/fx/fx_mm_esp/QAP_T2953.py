from pathlib import Path
from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.environments.full_environment import FullEnvironment
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.forex.FixMessageMarketDataSnapshotFullRefreshBuyFX import \
    FixMessageMarketDataSnapshotFullRefreshBuyFX
from test_framework.win_gui_wrappers.fe_trading_constant import ClientPrisingTileAction, PriceNaming
from test_framework.win_gui_wrappers.forex.client_rates_tile import ClientRatesTile


class QAP_T2953(TestCase):
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.fix_md = FixMessageMarketDataSnapshotFullRefreshBuyFX()
        self.fix_manager_fh = FixManager(self.fix_env.feed_handler, self.test_id)
        self.rates_tile = ClientRatesTile(self.test_id, self.session_id)

        self.client = self.data_set.get_client_tier_by_name("client_tier_1")
        self.symbol = self.data_set.get_symbol_by_name("symbol_1")
        self.instrument = self.symbol + "-Spot"

        self.market_data_event = "MD effected the tile"
        self.modify_spread_event = "Spread is modified"
        self.use_defaults_event = "Use Defaults effected the tile"
        self.pips_1 = "1"
        self.ask_pips = PriceNaming.ask_pips
        self.bid_pips = PriceNaming.bid_pips
        self.widen_spread = ClientPrisingTileAction.widen_spread
        self.expected_default_bid = "150"
        self.expected_modified_bid = "140"

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Step Precondition
        self.fix_md.set_market_data().\
            update_MDReqID(self.fix_md.get_parameter("MDReqID"), self.fix_env.feed_handler, 'FX')
        self.fix_manager_fh.send_message(self.fix_md, "Send MD HSBC EUR/USD")
        self.sleep(10)
        # endregion
        # region step 1
        self.rates_tile.crete_tile()
        self.rates_tile.modify_client_tile(instrument=self.instrument, client_tier=self.client)
        self.rates_tile.press_use_default()

        bid_n_ask_values = self.rates_tile.extract_prices_from_tile(self.bid_pips, self.ask_pips)
        actual_default_bid = bid_n_ask_values[self.bid_pips.value]
        self.rates_tile.compare_values(self.expected_default_bid, actual_default_bid,
                                       event_name=self.market_data_event)

        self.rates_tile.modify_client_tile(pips=self.pips_1)
        self.rates_tile.modify_spread(self.widen_spread)

        bid_n_ask_values = self.rates_tile.extract_prices_from_tile(self.bid_pips, self.ask_pips)
        actual_modified_bid = bid_n_ask_values[self.bid_pips.value]
        self.rates_tile.compare_values(self.expected_modified_bid, actual_modified_bid,
                                       event_name=self.modify_spread_event)

        self.rates_tile.press_use_default()
        bid_n_ask_values = self.rates_tile.extract_prices_from_tile(self.bid_pips, self.ask_pips)
        self.actual_default_bid = bid_n_ask_values[self.bid_pips.value]

        self.rates_tile.compare_values(self.expected_default_bid, self.actual_default_bid,
                                       event_name=self.use_defaults_event)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.rates_tile.close_tile()
