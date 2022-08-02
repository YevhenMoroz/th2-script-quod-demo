from pathlib import Path
from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.environments.full_environment import FullEnvironment
from test_framework.win_gui_wrappers.fe_trading_constant import PriceNaming, \
    RatesColumnNames
from test_framework.win_gui_wrappers.forex.client_rates_tile import ClientRatesTile


class QAP_T2784(TestCase):
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)

        self.ask_spot = RatesColumnNames.ask_spot
        self.bid_spot = RatesColumnNames.bid_spot
        self.ask_pts = RatesColumnNames.ask_pts
        self.bid_pts = RatesColumnNames.bid_pts

        self.ask_pips = PriceNaming.ask_pips
        self.bid_pips = PriceNaming.bid_pips
        self.ask_large = PriceNaming.ask_large
        self.bid_large = PriceNaming.bid_large

        self.rates_tile_spot = ClientRatesTile(self.test_id, self.session_id, index=0)
        self.rates_tile_w1 = ClientRatesTile(self.test_id, self.session_id, index=1)

        self.silver = self.data_set.get_client_tier_by_name("client_tier_1")
        self.eur_usd = self.data_set.get_symbol_by_name("symbol_1")
        self.eur_usd_spot = self.eur_usd + "-Spot"
        self.eur_usd_1w = self.eur_usd + "-1W"
        self.spot_event = "spot value validation"
        self.pts_event = "pts value validation"

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region step 1
        self.rates_tile_spot.crete_tile()
        self.rates_tile_spot.modify_client_tile(instrument=self.eur_usd_spot, client_tier=self.silver)

        self.rates_tile_w1.crete_tile()
        self.rates_tile_w1.modify_client_tile(instrument=self.eur_usd_1w, client_tier=self.silver)
        # endregion

        # region step 2
        spot_values = self.rates_tile_spot.extract_prices_from_tile(self.bid_pips, self.ask_pips, self.bid_large,
                                                                    self.ask_large)
        spot_ask_pips = spot_values[self.ask_pips.value]
        spot_ask_large = spot_values[self.ask_large.value]
        spot_price = spot_ask_large + spot_ask_pips
        print("spot tile tob has extracted")

        w1_values = self.rates_tile_w1.extract_values_from_rates(self.bid_spot, self.ask_spot, self.bid_pts,
                                                                 self.ask_pts)
        w1_tile_spot_price = w1_values[str(self.ask_spot)]
        print("w1 tile rows has extracted")

        self.rates_tile_spot.compare_values(spot_price, w1_tile_spot_price,
                                            event_name=self.spot_event)

        w1_tob_values = self.rates_tile_w1.extract_prices_from_tile(self.bid_pips, self.ask_pips, self.bid_large,
                                                                    self.ask_large)
        w1_ask_pips = w1_tob_values[self.ask_pips.value]
        w1_ask_large = w1_tob_values[self.ask_large.value]
        w1_price = w1_ask_large + w1_ask_pips
        expected_pts = str(round((float(w1_price) - float(spot_price)) * 10000, 1))
        actual_pts = str(float(w1_values[str(self.ask_pts)]))
        print("w1 tile tob has extracted")
        self.rates_tile_spot.compare_values(expected_pts, actual_pts,
                                            event_name=self.pts_event)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.rates_tile_spot.close_tile()
        self.rates_tile_w1.close_tile()
