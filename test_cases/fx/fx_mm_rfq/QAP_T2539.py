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


class QAP_T2539(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.quote_request_book = FXQuoteRequestBook(self.test_id, self.session_id)
        self.quote_book = FXQuoteBook(self.test_id, self.session_id)
        self.order_book = FXOrderBook(self.test_id, self.session_id)
        self.qty_column = OrderBookColumns.qty.value
        self.side_column = OrderBookColumns.side.value
        self.avgprice_column = OrderBookColumns.avg_price.value
        self.sts_column = OrderBookColumns.sts.value
        self.tenor_column = OrderBookColumns.tenor.value

        self.client_rfq_tile = ClientRFQTile(self.test_id, self.session_id)
        self.dealer_intervention = FXDealerIntervention(self.test_id, self.session_id)
        self.argentina = self.data_set.get_client_by_name("client_mm_2")
        self.eur = self.data_set.get_currency_by_name("currency_eur")
        self.usd = self.data_set.get_currency_by_name("currency_usd")
        self.spot_tenor = self.data_set.get_tenor_by_name("tenor_spot")
        self.settle_date_spot = self.data_set.get_settle_date_by_name("spot")
        self.qty_1m = random_qty(1)
        self.quote_sts_column = QuoteBookColumns.quote_status.value
        self.quote_px_column = QuoteBookColumns.offer_px.value
        self.quote_request_px_column = QuoteRequestBookColumns.offer_px.value
        self.quote_status_column = QuoteRequestBookColumns.status.value
        self.bid_size_column = QuoteBookColumns.bid_size.value
        self.filled_sts = QuoteStatus.filled.value
        self.new_sts = Status.new.value
        self.terminated_sts = Status.terminated.value
        self.px = "1.18151"
        self.side_buy = Side.buy.value
        self.side_sell = Side.sell.value
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.fx_fh_connectivity = self.fix_env.feed_handler
        self.fix_md = FixMessageMarketDataSnapshotFullRefreshBuyFX()
        self.fix_manager_fh_314 = FixManager(self.fx_fh_connectivity, self.test_id)
        self.no_md_entries = [
            {"MDEntryType": "0",
             "MDEntryPx": 1.1815,
             "MDEntrySize": 1000000,
             "MDEntryPositionNo": 1,
             'SettlDate': self.settle_date_spot,
             "MDEntryTime": datetime.utcnow().strftime('%Y%m%d')},
            {"MDEntryType": "1",
             "MDEntryPx": 1.18151,
             "MDEntrySize": 1000000,
             "MDEntryPositionNo": 1,
             'SettlDate': self.settle_date_spot,
             "MDEntryTime": datetime.utcnow().strftime('%Y%m%d')}]
        self.eur_usd = self.data_set.get_symbol_by_name("symbol_1")
        self.ms = self.data_set.get_venue_by_name("venue_3")

        self.md_req_id = f"{self.eur_usd}:SPO:REG:{self.ms}"

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Precondition
        self.fix_md.set_market_data()
        self.fix_md.update_repeating_group("NoMDEntries", self.no_md_entries)
        self.fix_md.update_MDReqID(self.md_req_id, self.fx_fh_connectivity, "FX")
        self.fix_manager_fh_314.send_message(self.fix_md)
        # endregion
        # region Step 1
        self.client_rfq_tile.modify_rfq_tile(from_cur=self.eur, to_cur=self.usd, client=self.argentina,
                                             clientTier=self.argentina, near_qty=self.qty_1m,
                                             near_tenor=self.spot_tenor)
        self.client_rfq_tile.send_rfq()
        self.client_rfq_tile.place_order(Side.buy)
        # endregion

        # region Step 2
        self.quote_book.set_filter([self.bid_size_column, self.qty_1m]).check_quote_book_fields_list({
            self.quote_px_column: self.px})
        self.quote_request_book.set_filter([self.qty_column, self.qty_1m]).check_quote_book_fields_list({
            self.quote_request_px_column: self.px})
        self.order_book.set_filter([self.qty_column, self.qty_1m]).check_order_fields_list({
            self.avgprice_column: self.px})
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.client_rfq_tile.close_tile()

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.fix_md.set_market_data()
        self.fix_md.update_MDReqID(self.md_req_id, self.fx_fh_connectivity, "FX")
        self.fix_manager_fh_314.send_message(self.fix_md)
        self.sleep(2)
