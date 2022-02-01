import random
from pathlib import Path
from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.win_gui_wrappers.forex.fx_order_book import FXOrderBook
from test_framework.win_gui_wrappers.forex.fx_quote_book import FXQuoteBook
from test_framework.win_gui_wrappers.forex.fx_quote_request_book import FXQuoteRequestBook
from test_framework.win_gui_wrappers.forex.rfq_tile import RFQTile
from test_framework.win_gui_wrappers.fe_trading_constant import QuoteRequestBookColumns as qrb, \
    OrderBookColumns as ob, Status as st, QuoteStatus as qs, QuoteBookColumns as qb, Side, ExecSts

qty = str(random.randint(1000000, 2000000))


class QAP_591(TestCase):
    def __init__(self, report_id, session_id=None, data_set=None):
        super().__init__(report_id, session_id, data_set)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.rfq_tile = None
        self.quote_request_book = None
        self.order_book = None
        self.quote_book = None

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        self.rfq_tile = RFQTile(self.test_id, self.session_id)
        self.order_book = FXOrderBook(self.test_id, self.session_id)
        self.quote_request_book = FXQuoteRequestBook(self.test_id, self.session_id)
        self.quote_book = FXQuoteBook(self.test_id, self.session_id)
        eur_currency = self.data_set.get_currency_by_name('currency_eur')
        usd_currency = self.data_set.get_currency_by_name('currency_usd')
        eur_usd_symbol = self.data_set.get_symbol_by_name('symbol_1')
        near_tenor = self.data_set.get_tenor_by_name('tenor_spot')
        far_tenor = self.data_set.get_tenor_by_name('tenor_1w')
        client = self.data_set.get_client_by_name("client_1")
        venue = self.data_set.get_venue_by_name('venue_1')
        rfq_venue = self.data_set.get_venue_by_name('venue_rfq_1')

        # region Step 1
        self.rfq_tile.crete_tile().modify_rfq_tile(from_cur=eur_currency, to_cur=usd_currency, near_qty=qty,
                                                   single_venue=venue, near_tenor=near_tenor, far_tenor=far_tenor,
                                                   client=client)
        self.rfq_tile.send_rfq()
        self.quote_request_book.set_filter(
            [qrb.instrument_symbol.value, eur_usd_symbol, qrb.qty.value, qty]).check_quote_book_fields_list(
            {qrb.instrument_symbol.value: eur_usd_symbol,
             qrb.quote_status.value: qs.accepted.value,
             qrb.status.value: st.new.value,
             qrb.venue.value: rfq_venue}, 'Checking that regular currency RFQ is placed')
        # endregion
        # region Step 2
        self.rfq_tile.place_order(side=Side.sell.value)
        # endregion
        # region Step 3
        self.order_book.set_filter(
            [ob.symbol.value, eur_usd_symbol, ob.qty.value, qty]).check_order_fields_list(
            {ob.symbol.value: eur_usd_symbol,
             ob.sts.value: st.terminated.value,
             ob.exec_sts.value: ExecSts.filled.value,
             ob.qty.value: qty,
             ob.far_leg.value: far_tenor}, 'Checking currency value in order book')

        quote_id = self.order_book.set_filter([ob.symbol.value, eur_usd_symbol, ob.qty.value, qty]). \
            extract_field(ob.quote_id.value)

        self.quote_book.set_filter(
            [qb.security_id.value, eur_usd_symbol, qb.quote_id.value, quote_id]).check_quote_book_fields_list(
            {qb.security_id.value: eur_usd_symbol,
             qb.quote_status.value: st.terminated.value,
             qb.quote_id.value: quote_id}, 'Checking currency value in quote book')
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.rfq_tile.close_tile()
