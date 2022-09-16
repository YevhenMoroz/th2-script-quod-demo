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
    Status as st, QuoteStatus as qs, QuoteBookColumns as qb


class QAP_T3044(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.rfq_tile = RFQTile(self.test_id, self.session_id)
        self.order_book = FXOrderBook(self.test_id, self.session_id)
        self.quote_request_book = FXQuoteRequestBook(self.test_id, self.session_id)
        self.quote_book = FXQuoteBook(self.test_id, self.session_id)
        self.qty = '1234567'
        self.qty1 = '1,234,567'

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        eur_currency = self.data_set.get_currency_by_name('currency_eur')
        usd_currency = self.data_set.get_currency_by_name('currency_usd')
        eur_usd_symbol = self.data_set.get_symbol_by_name('symbol_1')
        near_tenor = self.data_set.get_tenor_by_name('tenor_spot')
        far_tenor = self.data_set.get_tenor_by_name('tenor_1w')
        client = self.data_set.get_client_by_name("client_1")
        venue = self.data_set.get_venue_by_name('venue_1')
        rfq_venue = self.data_set.get_venue_by_name('venue_rfq_1')

        # region Step 1
        self.rfq_tile.crete_tile().modify_rfq_tile(from_cur=eur_currency, to_cur=usd_currency, near_qty=self.qty,
                                                   single_venue=venue, near_tenor=near_tenor, far_tenor=far_tenor,
                                                   client=client)
        # endregion
        # region Step 2
        self.rfq_tile.send_rfq()
        self.quote_request_book.set_filter(
            [qrb.instrument_symbol.value, eur_usd_symbol, qrb.qty.value, self.qty]).check_quote_book_fields_list(
            {qrb.instrument_symbol.value: eur_usd_symbol,
             qrb.quote_status.value: qs.accepted.value,
             qrb.status.value: st.new.value,
             qrb.venue.value: rfq_venue}, 'Checking that regular currency RFQ is placed')

        self.quote_book.set_filter(
            [qb.security_id.value, eur_usd_symbol, qb.bid_size.value, self.qty]).check_quote_book_fields_list(
            {qb.security_id.value: eur_usd_symbol,
             qb.quote_status.value: qs.accepted.value,
             qb.bid_size.value: self.qty1}, 'Checking currency value in quote book')
        # endregion
        # region Step 3
        self.rfq_tile.cancel_rfq()
        self.quote_request_book.set_filter(
            [qrb.instrument_symbol.value, eur_usd_symbol, qrb.qty.value, self.qty]).check_quote_book_fields_list(
            {qrb.instrument_symbol.value: eur_usd_symbol,
             qrb.quote_status.value: qs.terminated.value,
             qrb.status.value: st.terminated.value,
             qrb.venue.value: rfq_venue}, 'Checking that regular currency RFQ is placed')

        self.quote_book.set_filter(
            [qb.security_id.value, eur_usd_symbol, qb.bid_size.value, self.qty]).check_quote_book_fields_list(
            {qb.security_id.value: eur_usd_symbol,
             qb.quote_status.value: qs.terminated.value,
             qb.bid_size.value: self.qty1}, 'Checking currency value in quote book')
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.rfq_tile.close_tile()
