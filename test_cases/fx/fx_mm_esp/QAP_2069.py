from pathlib import Path
from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.win_gui_wrappers.fe_trading_constant import ClientPrisingTileAction, PriceNaming
from test_framework.win_gui_wrappers.forex.client_rates_tile import ClientRatesTile


class QAP_2069(TestCase):
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None):
        super().__init__(report_id, session_id, data_set)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.rates_tile = ClientRatesTile(self.test_id, self.session_id)
        # endregion
        # region Variables
        self.client = self.data_set.get_client_tier_by_name("client_tier_1")
        symbol = self.data_set.get_symbol_by_name("symbol_1")
        self.instrument = symbol + "-1W"
        self.spread_event = "Spread validation"
        self.ask_event = "Ask validation"
        self.bid_event = "Bid validation"
        self.pips_1 = "1"
        self.pips_2 = "2"
        self.pips_3 = "3"
        self.pips_4 = "4"
        self.pips_5 = "5"

        self.ask_pips = PriceNaming.ask_pips
        self.bid_pips = PriceNaming.bid_pips

        self.spread = PriceNaming.spread
        self.widen_spread = ClientPrisingTileAction.widen_spread
        self.narrow_spread = ClientPrisingTileAction.narrow_spread
        self.increase_ask = ClientPrisingTileAction.increase_ask
        self.decrease_bid = ClientPrisingTileAction.decrease_bid
        self.skew_towards_bid = ClientPrisingTileAction.skew_towards_bid
        self.skew_towards_ask = ClientPrisingTileAction.skew_towards_ask

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region step 1-2
        self.rates_tile.crete_tile()
        self.rates_tile.modify_client_tile(instrument=self.instrument, client_tier=self.client)
        self.rates_tile.press_use_default()
        bid_n_ask_values = self.rates_tile.extract_prices_from_tile(self.bid_pips, self.ask_pips)
        actual_spread = self.rates_tile.extract_prices_from_tile(self.spread)[self.spread.value]
        expected_spread = str(
            round((float(bid_n_ask_values[self.bid_pips.value]) - float(bid_n_ask_values[self.ask_pips.value])) * -0.1,
                  1))
        self.rates_tile.compare_values(expected_spread, actual_spread,
                                       event_name=self.spread_event)
        # endregion

        # region step 3
        self.rates_tile.modify_client_tile(pips=self.pips_2)
        self.rates_tile.modify_spread(self.widen_spread)
        prev_spread = actual_spread
        actual_spread = self.rates_tile.extract_prices_from_tile(self.spread)[self.spread.value]
        expected_spread = str(float(prev_spread) + int(self.pips_2) * 2)
        self.rates_tile.compare_values(expected_spread, actual_spread,
                                       event_name=self.spread_event)
        # endregion

        # region step 4
        self.rates_tile.modify_client_tile(pips=self.pips_1)
        self.rates_tile.modify_spread(self.narrow_spread)
        prev_spread = actual_spread
        actual_spread = self.rates_tile.extract_prices_from_tile(self.spread)[self.spread.value]
        expected_spread = str(round(float(prev_spread) - int(self.pips_1) * 2, 1))
        self.rates_tile.compare_values(expected_spread, actual_spread,
                                       event_name=self.spread_event)
        # endregion

        # region step 5
        self.rates_tile.modify_client_tile(pips=self.pips_2)
        self.rates_tile.modify_spread(self.increase_ask)
        prev_spread = actual_spread
        actual_spread = self.rates_tile.extract_prices_from_tile(self.spread)[self.spread.value]
        expected_spread = str(round(float(prev_spread) - int(self.pips_2), 1))
        self.rates_tile.compare_values(expected_spread, actual_spread,
                                       event_name=self.spread_event)
        # endregion

        # region step 6
        self.rates_tile.modify_client_tile(pips=self.pips_3)
        self.rates_tile.modify_spread(self.decrease_bid)
        prev_spread = actual_spread
        actual_spread = self.rates_tile.extract_prices_from_tile(self.spread)[self.spread.value]
        expected_spread = str(round(float(prev_spread) + int(self.pips_3), 1))
        self.rates_tile.compare_values(expected_spread, actual_spread,
                                       event_name=self.spread_event)
        # endregion

        # region step 7
        bid_n_ask_values = self.rates_tile.extract_prices_from_tile(self.bid_pips, self.ask_pips)
        expected_bid = str(int(bid_n_ask_values[self.bid_pips.value]) - 40)
        expected_ask = str(int(bid_n_ask_values[self.ask_pips.value]) - 40)
        self.rates_tile.modify_client_tile(pips=self.pips_4)
        self.rates_tile.modify_spread(self.skew_towards_bid)
        bid_n_ask_values = self.rates_tile.extract_prices_from_tile(self.bid_pips, self.ask_pips)
        actual_bid = str(int(bid_n_ask_values[self.bid_pips.value]))
        actual_ask = bid_n_ask_values[self.ask_pips.value]
        self.rates_tile.compare_values(expected_ask, actual_ask,
                                       event_name=self.ask_event)
        self.rates_tile.compare_values(expected_bid, actual_bid,
                                       event_name=self.bid_event)
        # endregion

        # region step 8
        bid_n_ask_values = self.rates_tile.extract_prices_from_tile(self.bid_pips, self.ask_pips)
        expected_bid = str(int(bid_n_ask_values[self.bid_pips.value]) + 50)
        expected_ask = str(int(bid_n_ask_values[self.ask_pips.value]) + 50)
        self.rates_tile.modify_client_tile(pips=self.pips_5)
        self.rates_tile.modify_spread(self.skew_towards_ask)
        bid_n_ask_values = self.rates_tile.extract_prices_from_tile(self.bid_pips, self.ask_pips)
        actual_bid = bid_n_ask_values[self.bid_pips.value]
        actual_ask = bid_n_ask_values[self.ask_pips.value]
        self.rates_tile.compare_values(expected_ask, actual_ask,
                                       event_name=self.ask_event)
        self.rates_tile.compare_values(expected_bid, actual_bid,
                                       event_name=self.bid_event)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.rates_tile.press_use_default()
        self.rates_tile.close_tile()
