from pathlib import Path
from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.win_gui_wrappers.fe_trading_constant import PriceNaming, RatesColumnNames
from test_framework.win_gui_wrappers.forex.client_rates_tile import ClientRatesTile


class QAP_6499(TestCase):
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None):
        super().__init__(report_id, session_id, data_set)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.rates_tile = None

        self.ask_pts = RatesColumnNames.ask_pts
        self.bid_pts = RatesColumnNames.bid_pts

        self.expected_pts = "0.000"

        self.ask_pips = PriceNaming.ask_pips
        self.bid_pips = PriceNaming.bid_pips

        self.rates_tile_tom = ClientRatesTile(self.test_id, self.session_id, index=0)
        self.rates_tile_spot = ClientRatesTile(self.test_id, self.session_id, index=1)

        self.client = self.data_set.get_client_tier_by_name("client_tier_1")
        self.symbol = self.data_set.get_symbol_by_name("symbol_12")
        self.instrument_tom = self.symbol + "-TOM"
        self.instrument_spot = self.symbol + "-Spot"
        self.pts_event = "pts value validation"
        self.prices_event = "prices validation"

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region step 1
        self.rates_tile_tom.crete_tile()
        self.rates_tile_tom.modify_client_tile(instrument=self.instrument_tom, client_tier=self.client)
        # endregion

        # region step 2
        row_values = self.rates_tile_tom.extract_values_from_rates(self.ask_pts, self.bid_pts)
        bid_pts_tom = row_values[str(self.bid_pts)]
        ask_pts_tom = row_values[str(self.ask_pts)]
        self.rates_tile_tom.compare_values(self.expected_pts, bid_pts_tom,
                                           event_name=self.pts_event)
        self.rates_tile_tom.compare_values(self.expected_pts, ask_pts_tom,
                                           event_name=self.pts_event)
        # endregion

        # region step 3
        self.rates_tile_spot.crete_tile()
        self.rates_tile_spot.modify_client_tile(instrument=self.instrument_spot, client_tier=self.client)
        # endregion

        # region step 4
        bid_n_ask_tom_values = self.rates_tile_tom.extract_prices_from_tile(self.bid_pips, self.ask_pips)
        bid_tom_price = bid_n_ask_tom_values[self.bid_pips.value]
        ask_tom_price = bid_n_ask_tom_values[self.ask_pips.value]
        bid_n_ask_spot_values = self.rates_tile_tom.extract_prices_from_tile(self.bid_pips, self.ask_pips)
        bid_spot_price = bid_n_ask_spot_values[self.bid_pips.value]
        ask_spot_price = bid_n_ask_spot_values[self.ask_pips.value]

        self.rates_tile_tom.compare_values(bid_tom_price, bid_spot_price,
                                           event_name=self.prices_event)
        self.rates_tile_tom.compare_values(ask_tom_price, ask_spot_price,
                                           event_name=self.prices_event)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.rates_tile_tom.close_tile()
        self.rates_tile_spot.close_tile()
