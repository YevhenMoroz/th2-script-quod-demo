import random
from pathlib import Path
from custom import basic_custom_actions as bca
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.environments.full_environment import FullEnvironment
from test_framework.win_gui_wrappers.forex.fx_order_book import FXOrderBook
from test_framework.win_gui_wrappers.forex.fx_trade_book import FXTradeBook
from test_framework.win_gui_wrappers.forex.fx_quote_request_book import FXQuoteRequestBook
from test_framework.core.test_case import TestCase
from test_framework.win_gui_wrappers.forex.rfq_tile import RFQTile
from test_framework.win_gui_wrappers.fe_trading_constant import QuoteRequestBookColumns as qrb
from test_framework.win_gui_wrappers.fe_trading_constant import OrderBookColumns as ob, Side, \
    TradeBookColumns as tb


class QAP_T2708(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.rfq_tile = RFQTile(self.test_id, self.session_id)
        self.order_book = FXOrderBook(self.test_id, self.session_id)
        self.quote_request_book = FXQuoteRequestBook(self.test_id, self.session_id)
        self.trade_book = FXTradeBook(self.test_id, self.session_id)
        self.qty = str(random.randint(1000000, 2000000))

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        eur_currency = self.data_set.get_currency_by_name('currency_eur')
        usd_currency = self.data_set.get_currency_by_name('currency_usd')
        eur_usd_symbol = self.data_set.get_symbol_by_name('symbol_1')
        tenor_spot = self.data_set.get_tenor_by_name('tenor_spot')
        tenor_1w = self.data_set.get_tenor_by_name('tenor_1w')
        tenor_2w = self.data_set.get_tenor_by_name('tenor_2w')
        tenor_tom = self.data_set.get_tenor_by_name('tenor_tom')
        venue = self.data_set.get_venue_by_name('venue_1')
        client = self.data_set.get_client_by_name("client_1")

        # region Step 1
        self.rfq_tile.crete_tile().modify_rfq_tile(from_cur=eur_currency, to_cur=usd_currency,
                                                   near_qty=self.qty, near_tenor=tenor_spot,
                                                   client=client, single_venue=venue)
        # endregion
        # region Step 2
        self.rfq_tile.send_rfq()
        self.rfq_tile.place_order(side=Side.buy.value)

        self.quote_request_book.set_filter(
            [qrb.instrument_symbol.value, eur_usd_symbol, qrb.qty.value, self.qty]).check_quote_book_fields_list(
            {qrb.tenor.value: tenor_spot}, 'Checking tenor value in quote request book')

        self.order_book.set_filter(
            [ob.symbol.value, eur_usd_symbol, ob.qty.value, self.qty]).check_order_fields_list(
            {ob.tenor.value: tenor_spot}, 'Checking tenor value in order book')

        exec_id1 = self.order_book.set_filter([ob.symbol.value, eur_usd_symbol, ob.qty.value, self.qty]). \
            extract_second_lvl_fields_list({ob.exec_id.value: ''})

        self.trade_book.set_filter(
            [tb.exec_id.value, exec_id1[ob.exec_id.value]]).check_trade_fields_list(
            {tb.tenor.value: tenor_spot}, 'Checking tenor value in trade book')
        # endregion
        # region Step 3
        self.rfq_tile.modify_rfq_tile(near_tenor=tenor_1w)
        self.rfq_tile.send_rfq()
        self.rfq_tile.place_order(side=Side.buy.value)

        self.quote_request_book.set_filter(
            [qrb.instrument_symbol.value, eur_usd_symbol, qrb.qty.value, self.qty]).check_quote_book_fields_list(
            {qrb.tenor.value: tenor_1w}, 'Checking tenor value in quote request book')

        self.order_book.set_filter(
            [ob.symbol.value, eur_usd_symbol, ob.qty.value, self.qty]).check_order_fields_list(
            {ob.tenor.value: tenor_1w}, 'Checking tenor value in order book')

        exec_id2 = self.order_book.set_filter([ob.symbol.value, eur_usd_symbol, ob.qty.value, self.qty]). \
            extract_second_lvl_fields_list({ob.exec_id.value: ''})

        self.trade_book.set_filter(
            [tb.exec_id.value, exec_id2[ob.exec_id.value]]).check_trade_fields_list(
            {tb.tenor.value: tenor_1w}, 'Checking tenor value in trade book')
        # endregion
        # region Step 4
        self.rfq_tile.modify_rfq_tile(near_tenor=tenor_spot, far_tenor=tenor_1w)
        self.rfq_tile.send_rfq()
        self.rfq_tile.place_order(side=Side.buy.value)

        self.quote_request_book.set_filter(
            [qrb.instrument_symbol.value, eur_usd_symbol, qrb.qty.value, self.qty]).check_quote_book_fields_list(
            {qrb.tenor.value: tenor_spot,
             qrb.near_tenor.value: tenor_spot,
             qrb.far_tenor.value: tenor_1w}, 'Checking tenor value in quote request book')

        self.order_book.set_filter(
            [ob.symbol.value, eur_usd_symbol, ob.qty.value, self.qty]).check_order_fields_list(
            {ob.tenor.value: tenor_spot,
             ob.near_tenor.value: tenor_spot,
             ob.far_tenor.value: tenor_1w}, 'Checking tenor value in order book')

        exec_id3 = self.order_book.set_filter([ob.symbol.value, eur_usd_symbol, ob.qty.value, self.qty]). \
            extract_second_lvl_fields_list({ob.exec_id.value: ''})

        self.trade_book.set_filter(
            [tb.exec_id.value, exec_id3[ob.exec_id.value]]).check_trade_fields_list(
            {tb.tenor.value: tenor_spot,
             tb.near_tenor.value: tenor_spot,
             tb.far_tenor.value: tenor_1w}, 'Checking tenor value in trade book')
        # endregion
        # region Step 5
        self.rfq_tile.modify_rfq_tile(near_tenor=tenor_tom, far_tenor=tenor_2w)
        self.rfq_tile.send_rfq()
        self.rfq_tile.place_order(side=Side.buy.value)

        self.quote_request_book.set_filter(
            [qrb.instrument_symbol.value, eur_usd_symbol, qrb.qty.value, self.qty]).check_quote_book_fields_list(
            {qrb.tenor.value: tenor_tom,
             qrb.near_tenor.value: tenor_tom,
             qrb.far_tenor.value: tenor_2w}, 'Checking tenor value in quote request book')

        self.order_book.set_filter(
            [ob.symbol.value, eur_usd_symbol, ob.qty.value, self.qty]).check_order_fields_list(
            {ob.tenor.value: tenor_tom,
             ob.near_tenor.value: tenor_tom,
             ob.far_tenor.value: tenor_2w}, 'Checking tenor value in order book')

        exec_id4 = self.order_book.set_filter([ob.symbol.value, eur_usd_symbol, ob.qty.value, self.qty]). \
            extract_second_lvl_fields_list({ob.exec_id.value: ''})

        self.trade_book.set_filter(
            [tb.exec_id.value, exec_id4[ob.exec_id.value]]).check_trade_fields_list(
            {tb.tenor.value: tenor_tom,
             tb.near_tenor.value: tenor_tom,
             tb.far_tenor.value: tenor_2w}, 'Checking tenor value in trade book')
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.rfq_tile.close_tile()
