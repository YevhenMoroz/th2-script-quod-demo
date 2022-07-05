import time
from pathlib import Path

from custom import basic_custom_actions as bca
from test_cases.fx.fx_wrapper.common_tools import random_qty
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.win_gui_wrappers.fe_trading_constant import OrderBookColumns, Status, Side, QuoteBookColumns, \
    QuoteStatus, QuoteRequestBookColumns, TradeBookColumns
from test_framework.win_gui_wrappers.forex.client_rfq_tile import ClientRFQTile
from test_framework.win_gui_wrappers.forex.fx_dealer_intervention import FXDealerIntervention
from test_framework.win_gui_wrappers.forex.fx_order_book import FXOrderBook
from test_framework.win_gui_wrappers.forex.fx_quote_book import FXQuoteBook
from test_framework.win_gui_wrappers.forex.fx_trade_book import FXTradeBook


class QAP_3501(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None):
        super().__init__(report_id, session_id, data_set)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.order_book = FXOrderBook(self.test_id, self.session_id)
        self.quote_book = FXQuoteBook(self.test_id, self.session_id)

        self.trade_book = FXTradeBook(self.test_id, self.session_id)
        self.qty_column = TradeBookColumns.qty.value
        self.side_column = TradeBookColumns.side.value
        self.side_buy = Side.buy.value
        self.side_sell = Side.sell.value
        self.exec_id = TradeBookColumns.exec_id.value
        self.contra_exec_id = TradeBookColumns.contra_exec_id.value
        self.order_id = OrderBookColumns.order_id.value
        self.quote_id = OrderBookColumns.quote_id.value

        self.client_rfq_tile = ClientRFQTile(self.test_id, self.session_id)
        self.dealer_intervention = FXDealerIntervention(self.test_id, self.session_id)
        self.client = self.data_set.get_client_by_name("client_mm_1")
        self.symbol = self.data_set.get_symbol_by_name("symbol_2")
        self.gbp_cur = self.data_set.get_currency_by_name("currency_gbp")
        self.usd_cur = self.data_set.get_currency_by_name("currency_usd")
        self.spot_tenor = self.data_set.get_tenor_by_name("tenor_spot")
        self.wk1_tenor = self.data_set.get_tenor_by_name("tenor_1w")
        self.qty = random_qty(1, 3, 7)
        self.qty_for_di = random_qty(2, 3, 8)
        # self.qty_column = OrderBookColumns.qty.value
        # self.side_column = OrderBookColumns.side.value
        self.sts_column = OrderBookColumns.sts.value
        self.tenor_column = OrderBookColumns.tenor.value
        self.quote_sts_column = QuoteBookColumns.quote_status.value
        self.quote_status_column = QuoteRequestBookColumns.status.value
        self.bid_size_column = QuoteBookColumns.bid_size.value
        self.terminated_sts = Status.terminated.value
        self.accepted_sts = QuoteStatus.accepted.value
        self.new_sts = Status.new.value


    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Step 1
        self.client_rfq_tile.crete_tile()
        self.client_rfq_tile.modify_rfq_tile(from_cur=self.gbp_cur, to_cur=self.usd_cur, client=self.client,
                                             clientTier=self.client, near_qty=self.qty, near_tenor=self.spot_tenor)
        self.client_rfq_tile.send_rfq()
        self.trade_book.set_filter([self.bid_size_column, self.qty, self.side_column, self.side_buy]).check_trade_fields_list({})
        self.trade_book.set_filter([self.bid_size_column, self.qty, self.side_column, self.side_sell]).check_trade_fields_list({})

        # self.quote_book.set_filter([self.bid_size_column, self.qty, self.side_column, self.side_sell]).check_quote_book_fields_list({
        #     self.quote_sts_column: self.accepted_sts})
        # endregion
        # region Step 2
        # TODO Add extraction from Client RFQ tile
        # endregion
        # region Step 3
        self.client_rfq_tile.place_order(Side.buy)
        self.order_book.set_filter([self.qty_column, self.qty]).check_order_fields_list({
            self.sts_column: self.terminated_sts, self.side_column: self.side_buy, self.tenor_column: self.spot_tenor})
        # endregion
        # region step 4
        self.client_rfq_tile.modify_rfq_tile(from_cur=self.gbp_cur, to_cur=self.usd_cur, client=self.client,
                                             clientTier=self.client, near_qty=self.qty, near_tenor=self.wk1_tenor)
        self.client_rfq_tile.send_rfq()
        self.quote_book.set_filter([self.bid_size_column, self.qty]).check_quote_book_fields_list({
            self.quote_sts_column: self.accepted_sts})
        # endregion
        # region Step 5
        self.client_rfq_tile.place_order(Side.sell)
        self.order_book.set_filter([self.qty_column, self.qty]).check_order_fields_list({
            self.sts_column: self.terminated_sts, self.side_column: self.side_sell, self.tenor_column: self.wk1_tenor})
        # endregion
        # region Step 6
        self.client_rfq_tile.modify_rfq_tile(from_cur=self.gbp_cur, to_cur=self.usd_cur, client=self.client,
                                             clientTier=self.client, near_qty=self.qty_for_di, near_tenor=self.spot_tenor)
        self.client_rfq_tile.send_rfq()
        self.dealer_intervention.set_list_filter([self.qty_column, self.qty_for_di]).check_unassigned_fields({
            self.quote_status_column: self.new_sts})
        # endregion
        # region Step 7
        self.dealer_intervention.assign_quote()
        self.dealer_intervention.estimate_quote()
        time.sleep(3)
        self.dealer_intervention.send_quote()
        self.dealer_intervention.close_window()
        # endregion
        # region Step 8
        self.client_rfq_tile.place_order(Side.buy)
        self.order_book.set_filter([self.qty_column, self.qty_for_di]).check_order_fields_list({
            self.sts_column: self.terminated_sts, self.side_column: self.side_buy, self.tenor_column: self.spot_tenor})
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.client_rfq_tile.close_tile()
