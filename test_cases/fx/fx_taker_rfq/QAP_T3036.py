import random
from pathlib import Path
from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.environments.full_environment import FullEnvironment
from test_framework.win_gui_wrappers.forex.fx_order_book import FXOrderBook
from test_framework.win_gui_wrappers.forex.fx_quote_book import FXQuoteBook
from test_framework.win_gui_wrappers.forex.fx_quote_request_book import FXQuoteRequestBook
from test_framework.win_gui_wrappers.forex.rfq_tile import RFQTile
from test_framework.win_gui_wrappers.fe_trading_constant import QuoteRequestBookColumns as qrb, \
    OrderBookColumns as ob, Status as st, QuoteStatus as qs, QuoteBookColumns as qb, Side


class QAP_T3036(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.rfq_tile = RFQTile(self.test_id, self.session_id)
        self.rfq_tile_1 = RFQTile(self.test_id, self.session_id, index=1)
        self.order_book = FXOrderBook(self.test_id, self.session_id)
        self.quote_request_book = FXQuoteRequestBook(self.test_id, self.session_id)
        self.quote_book = FXQuoteBook(self.test_id, self.session_id)
        self.qty = str(random.randint(1000000, 2000000))

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        php_currency = self.data_set.get_currency_by_name('currency_php')
        usd_currency = self.data_set.get_currency_by_name('currency_usd')
        cad_currency = self.data_set.get_currency_by_name('currency_cad')
        near_tenor = self.data_set.get_tenor_by_name('tenor_1m')
        near_tenor_1 = self.data_set.get_tenor_by_name('tenor_2m')
        venue = self.data_set.get_venue_by_name('venue_1')
        venue_1 = self.data_set.get_venue_by_name('venue_2')
        rfq_venue = self.data_set.get_venue_by_name('venue_rfq_1')
        rfq_venue_1 = self.data_set.get_venue_by_name('venue_rfq_2')
        usd_php_symbol = self.data_set.get_symbol_by_name('symbol_ndf_1')
        usd_cad_symbol = self.data_set.get_symbol_by_name('symbol_12')
        client = self.data_set.get_client_by_name("client_1")

        # region Step 1
        self.rfq_tile.crete_tile().modify_rfq_tile(from_cur=usd_currency, to_cur=php_currency,
                                                   near_qty=self.qty, near_tenor=near_tenor,
                                                   client=client, single_venue=venue_1)
        self.rfq_tile_1.crete_tile().modify_rfq_tile(from_cur=usd_currency, to_cur=cad_currency,
                                                     near_qty=self.qty, near_tenor=near_tenor_1,
                                                     client=client, single_venue=venue)
        # endregion
        # region Step 2
        self.rfq_tile.send_rfq()
        self.rfq_tile_1.send_rfq()

        self.quote_request_book.set_filter(
            [qrb.instrument_symbol.value, usd_php_symbol, qrb.qty.value, self.qty]).check_quote_book_fields_list(
            {qrb.instrument_symbol.value: usd_php_symbol,
             qrb.quote_status.value: qs.accepted.value,
             qrb.status.value: st.new.value,
             qrb.venue.value: rfq_venue_1}, 'Checking that regular currency RFQ is placed')
        self.quote_request_book.set_filter(
            [qrb.instrument_symbol.value, usd_cad_symbol, qrb.qty.value, self.qty]).check_quote_book_fields_list(
            {qrb.instrument_symbol.value: usd_cad_symbol,
             qrb.quote_status.value: qs.accepted.value,
             qrb.status.value: st.new.value,
             qrb.venue.value: rfq_venue}, 'Checking that regular currency RFQ is placed')
        # endregion
        # region Step 3
        self.rfq_tile.place_order(side=Side.buy.value)
        self.rfq_tile_1.place_order(side=Side.buy.value)

        quote_id = self.order_book.set_filter([ob.symbol.value, usd_php_symbol, ob.qty.value, self.qty]). \
            extract_field(ob.quote_id.value)

        self.quote_book.set_filter(
            [qb.quote_id.value, quote_id]).check_quote_book_fields_list(
            {qb.quote_status.value: st.terminated.value,
             qb.quote_id.value: quote_id}, 'Checking currency value in quote book')

        quote_id1 = self.order_book.set_filter([ob.symbol.value, usd_cad_symbol, ob.qty.value, self.qty]). \
            extract_field(ob.quote_id.value)

        self.quote_book.set_filter(
            [qb.quote_id.value, quote_id1]).check_quote_book_fields_list(
            {qb.quote_status.value: st.terminated.value,
             qb.quote_id.value: quote_id1}, 'Checking currency value in quote book')
        # endregion
        # region Step 4
        self.rfq_tile.send_rfq()
        self.rfq_tile_1.send_rfq()

        self.quote_request_book.set_filter(
            [qrb.instrument_symbol.value, usd_php_symbol, qrb.qty.value, self.qty]).check_quote_book_fields_list(
            {qrb.instrument_symbol.value: usd_php_symbol,
             qrb.quote_status.value: qs.accepted.value,
             qrb.status.value: st.new.value,
             qrb.venue.value: rfq_venue_1}, 'Checking that regular currency RFQ is placed')
        self.quote_request_book.set_filter(
            [qrb.instrument_symbol.value, usd_cad_symbol, qrb.qty.value, self.qty]).check_quote_book_fields_list(
            {qrb.instrument_symbol.value: usd_cad_symbol,
             qrb.quote_status.value: qs.accepted.value,
             qrb.status.value: st.new.value,
             qrb.venue.value: rfq_venue}, 'Checking that regular currency RFQ is placed')
        # endregion
        # region Step 5
        self.rfq_tile.place_order(side=Side.buy.value)
        self.rfq_tile_1.place_order(side=Side.buy.value)

        quote_id = self.order_book.set_filter([ob.symbol.value, usd_php_symbol, ob.qty.value, self.qty]). \
            extract_field(ob.quote_id.value)

        self.quote_book.set_filter(
            [qb.quote_id.value, quote_id]).check_quote_book_fields_list(
            {qb.quote_status.value: st.terminated.value,
             qb.quote_id.value: quote_id}, 'Checking currency value in quote book')

        quote_id1 = self.order_book.set_filter([ob.symbol.value, usd_cad_symbol, ob.qty.value, self.qty]). \
            extract_field(ob.quote_id.value)

        self.quote_book.set_filter(
            [qb.quote_id.value, quote_id1]).check_quote_book_fields_list(
            {qb.quote_status.value: st.terminated.value,
             qb.quote_id.value: quote_id1}, 'Checking currency value in quote book')
        # endregion
        # region Step 6
        self.rfq_tile.send_rfq()
        self.rfq_tile_1.send_rfq()

        self.quote_request_book.set_filter(
            [qrb.instrument_symbol.value, usd_php_symbol, qrb.qty.value, self.qty]).check_quote_book_fields_list(
            {qrb.instrument_symbol.value: usd_php_symbol,
             qrb.quote_status.value: qs.accepted.value,
             qrb.status.value: st.new.value,
             qrb.venue.value: rfq_venue_1}, 'Checking that regular currency RFQ is placed')
        self.quote_request_book.set_filter(
            [qrb.instrument_symbol.value, usd_cad_symbol, qrb.qty.value, self.qty]).check_quote_book_fields_list(
            {qrb.instrument_symbol.value: usd_cad_symbol,
             qrb.quote_status.value: qs.accepted.value,
             qrb.status.value: st.new.value,
             qrb.venue.value: rfq_venue}, 'Checking that regular currency RFQ is placed')
        # endregion
        # region Step 7
        self.rfq_tile.cancel_rfq()
        # endregion
        # region Step 8
        self.rfq_tile_1.place_order(side=Side.buy.value)

        quote_id1 = self.order_book.set_filter([ob.symbol.value, usd_cad_symbol, ob.qty.value, self.qty]). \
            extract_field(ob.quote_id.value)

        self.quote_book.set_filter(
            [qb.quote_id.value, quote_id1]).check_quote_book_fields_list(
            {qb.quote_status.value: st.terminated.value,
             qb.quote_id.value: quote_id1}, 'Checking currency value in quote book')
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.rfq_tile.close_tile()
        self.rfq_tile_1.close_tile()
