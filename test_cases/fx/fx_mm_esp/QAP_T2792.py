from pathlib import Path
from custom import basic_custom_actions as bca
from test_cases.fx.fx_wrapper.common_tools import random_qty
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.environments.full_environment import FullEnvironment
from test_framework.win_gui_wrappers.fe_trading_constant import PriceNaming, \
    RatesColumnNames, OrderBookColumns as obc
from test_framework.win_gui_wrappers.forex.client_rates_tile import ClientRatesTile
from test_framework.win_gui_wrappers.forex.fx_order_book import FXOrderBook
from test_framework.win_gui_wrappers.forex.fx_order_ticket import FXOrderTicket
from win_gui_modules.client_pricing_wrappers import RatesTileTableOrdSide


class QAP_T2792(TestCase):
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.rates_tile = None

        self.ask_spot = RatesColumnNames.ask_spot
        self.bid_spot = RatesColumnNames.bid_spot
        self.ask_pts = RatesColumnNames.ask_pts
        self.bid_pts = RatesColumnNames.bid_pts

        self.ask_pips = PriceNaming.ask_pips
        self.bid_pips = PriceNaming.bid_pips
        self.ask_large = PriceNaming.ask_large
        self.bid_large = PriceNaming.bid_large

        self.rates_tile = ClientRatesTile(self.test_id, self.session_id)
        self.order_ticket = FXOrderTicket(self.test_id, self.session_id)
        self.order_book = FXOrderBook(self.test_id, self.session_id)

        self.client_tier_silver = self.data_set.get_client_tier_by_name("client_tier_1")
        self.client_silver = self.data_set.get_client_by_name("client_mm_1")
        self.eur_usd = self.data_set.get_symbol_by_name("symbol_1")
        self.eur_usd_spot = self.eur_usd + "-Spot"
        self.side = RatesTileTableOrdSide.SELL

        self.rand_qty1 = random_qty(8, 9, 6)
        self.rand_qty2 = random_qty(8, 9, 6)
        self.status = "Terminated"

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region step 1
        self.rates_tile.crete_tile()
        self.rates_tile.modify_client_tile(instrument=self.eur_usd_spot, client_tier=self.client_tier_silver)

        values = self.rates_tile.extract_prices_from_tile(self.bid_pips, self.ask_pips, self.bid_large,
                                                                    self.ask_large)

        spot_bid_pips = values[self.bid_pips.value]
        spot_bid_large = values[self.bid_large.value]
        bid_price = spot_bid_large + spot_bid_pips

        spot_ask_pips = values[self.ask_pips.value]
        spot_ask_large = values[self.ask_large.value]
        ask_price = spot_ask_large + spot_ask_pips

        self.rates_tile.place_order(client=self.client_silver, qty=self.rand_qty1)

        self.order_book.set_filter(
            [obc.qty.value, self.rand_qty1]).check_order_fields_list(
            {obc.qty.value: self.rand_qty1, obc.client_id.value: self.client_silver, obc.limit_price.value: ask_price,
             obc.sts.value: self.status})
        # endregion

        # region step 3
        self.rates_tile.open_order_ticket_by_row(row=1, side=self.side)
        self.order_ticket.set_order_details(place=True, client=self.client_silver, qty=self.rand_qty2)
        self.order_ticket.create_order(is_mm=True)

        self.order_book.set_filter(
            [obc.qty.value, self.rand_qty2]).check_order_fields_list(
            {obc.qty.value: self.rand_qty2, obc.client_id.value: self.client_silver, obc.limit_price.value: bid_price,
             obc.sts.value: self.status})
        # endregion


    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.rates_tile.close_tile()
