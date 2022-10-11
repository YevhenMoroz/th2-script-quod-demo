from datetime import datetime
from pathlib import Path

from custom import basic_custom_actions as bca
from test_cases.fx.fx_wrapper.common_tools import random_qty
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.environments.full_environment import FullEnvironment
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.forex.FixMessageMarketDataSnapshotFullRefreshBuyFX import \
    FixMessageMarketDataSnapshotFullRefreshBuyFX
from test_framework.win_gui_wrappers.fe_trading_constant import OrderBookColumns, Status, Side, QuoteBookColumns, \
    QuoteStatus, QuoteRequestBookColumns
from test_framework.win_gui_wrappers.forex.client_rfq_tile import ClientRFQTile
from test_framework.win_gui_wrappers.forex.fx_dealer_intervention import FXDealerIntervention
from test_framework.win_gui_wrappers.forex.fx_order_book import FXOrderBook
from test_framework.win_gui_wrappers.forex.fx_quote_book import FXQuoteBook
from test_framework.win_gui_wrappers.forex.fx_quote_request_book import FXQuoteRequestBook


class QAP_T2566(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.quote_request_book = FXQuoteRequestBook(self.test_id, self.session_id)
        self.quote_book = FXQuoteBook(self.test_id, self.session_id)
        self.order_book = FXOrderBook(self.test_id, self.session_id)

        self.avgprice_column = OrderBookColumns.avg_price.value
        self.sts_column = OrderBookColumns.sts.value
        self.tenor_column = OrderBookColumns.tenor.value

        self.client_rfq_tile = ClientRFQTile(self.test_id, self.session_id)
        self.dealer_intervention = FXDealerIntervention(self.test_id, self.session_id)
        self.argentina = self.data_set.get_client_by_name("client_mm_2")
        self.eur = self.data_set.get_currency_by_name("currency_eur")
        self.usd = self.data_set.get_currency_by_name("currency_usd")
        self.tenor_1w = self.data_set.get_tenor_by_name("tenor_1w")
        self.tenor_2w = self.data_set.get_tenor_by_name("tenor_2w")
        self.settle_date_spot = self.data_set.get_settle_date_by_name("spot")
        self.qty_1m = random_qty(1)
        self.qty_1m_doubler = random_qty(1)
        self.qty_2m = random_qty(2)
        self.quote_sts_column = QuoteBookColumns.quote_status.value
        self.quote_px_column = QuoteBookColumns.offer_px.value
        self.near_leg_tenor_column = OrderBookColumns.near_leg.value
        self.far_leg_tenor_column = OrderBookColumns.far_leg.value
        self.side_column = OrderBookColumns.side.value
        self.qty_column = OrderBookColumns.qty.value
        self.near_qty_column = OrderBookColumns.near_qty.value
        self.venue_column = OrderBookColumns.venue.value
        self.ordtype_column = OrderBookColumns.ord_type.value

        self.near_leg_tenor = "1W"
        self.far_leg_tenor = "2W"
        self.terminated_sts = Status.terminated.value
        self.px = "1.18151"
        self.side_buy = Side.buy.value
        self.side_sell = Side.sell.value
        self.venue = "QUODFX"
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.fx_fh_connectivity = self.fix_env.feed_handler
        self.fix_md = FixMessageMarketDataSnapshotFullRefreshBuyFX()
        self.fix_manager_fh_314 = FixManager(self.fx_fh_connectivity, self.test_id)
        self.eur_usd = self.data_set.get_symbol_by_name("symbol_1")
        self.ms = self.data_set.get_venue_by_name("venue_3")
        self.ordtype = "PreviouslyQuoted"

        self.md_req_id = f"{self.eur_usd}:SPO:REG:{self.ms}"

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Step 1
        self.client_rfq_tile.modify_rfq_tile(from_cur=self.eur, to_cur=self.usd, client=self.argentina,
                                             clientTier=self.argentina, near_qty=self.qty_1m,
                                             near_tenor=self.tenor_1w, far_tenor=self.tenor_2w)
        self.client_rfq_tile.send_rfq()
        # endregion
        # region Step 3
        self.client_rfq_tile.place_order(Side.buy)
        # endregion
        # region Step 4
        self.client_rfq_tile.modify_rfq_tile(near_qty=self.qty_1m_doubler, far_qty=self.qty_2m, client=self.argentina)
        self.client_rfq_tile.send_rfq()
        # endregion
        # region Step 5
        self.client_rfq_tile.place_order(Side.sell)
        # endregion

        # region Step Order Book verifier
        self.order_book.set_filter([self.qty_column, self.qty_1m]).check_order_fields_list({
            self.sts_column: self.terminated_sts, self.near_leg_tenor_column: self.near_leg_tenor,
            self.far_leg_tenor_column: self.far_leg_tenor,
            self.side_column: self.side_buy, self.qty_column: self.qty_1m, self.venue_column: self.venue,
            self.ordtype_column: self.ordtype})
        self.order_book.set_filter([self.near_qty_column, self.qty_1m_doubler]).check_order_fields_list({
            self.sts_column: self.terminated_sts, self.near_leg_tenor_column: self.near_leg_tenor,
            self.far_leg_tenor_column: self.far_leg_tenor,
            self.side_column: self.side_sell, self.qty_column: self.qty_2m, self.venue_column: self.venue,
            self.ordtype_column: self.ordtype})
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.client_rfq_tile.close_tile()
