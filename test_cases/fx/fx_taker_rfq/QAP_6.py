import random
from pathlib import Path
from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.win_gui_wrappers.forex.fx_quote_request_book import FXQuoteRequestBook
from test_framework.win_gui_wrappers.forex.rfq_tile import RFQTile
from test_framework.win_gui_wrappers.fe_trading_constant import QuoteRequestBookColumns as qrb, QuoteStatus as qs, \
    Status


class QAP_6(TestCase):

    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None):
        super().__init__(report_id, session_id, data_set)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.rfq_tile = RFQTile(self.test_id, self.session_id)
        self.quote_request_book = FXQuoteRequestBook(self.test_id, self.session_id)
        self.qty = str(random.randint(1000000, 2000000))

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        eur_currency = self.data_set.get_currency_by_name('currency_eur')
        usd_currency = self.data_set.get_currency_by_name('currency_usd')
        ndf_currency = self.data_set.get_currency_by_name('currency_php')
        eur_usd_symbol = self.data_set.get_symbol_by_name('symbol_1')
        usd_php_symbol = self.data_set.get_symbol_by_name('symbol_ndf_1')
        near_tenor = self.data_set.get_tenor_by_name('tenor_spot')
        far_tenor = self.data_set.get_tenor_by_name('tenor_1w')
        venue = self.data_set.get_venue_by_name('venue_1')
        client = self.data_set.get_client_by_name("client_1")
        # region Step 1
        self.rfq_tile.crete_tile().modify_rfq_tile(from_cur=eur_currency, to_cur=usd_currency,
                                                   near_qty=self.qty, near_tenor=near_tenor,
                                                   client=client, single_venue=venue)
        self.rfq_tile.send_rfq()

        self.quote_request_book.set_filter(
            [qrb.instrument_symbol.value, usd_php_symbol]).check_quote_book_fields_list(
            {qrb.instrument_symbol.value: eur_usd_symbol,
             qrb.quote_status.value: qs.accepted.value,
             qrb.status.value: Status.new.value}, 'Checking that regular currency RFQ is placed')
        self.rfq_tile.close_tile()
        # endregion

        # region Step 2
        self.rfq_tile.crete_tile().modify_rfq_tile(from_cur=usd_currency, to_cur=ndf_currency,
                                                   near_qty=self.qty, near_tenor=near_tenor,
                                                   client=client, single_venue=venue)
        self.rfq_tile.send_rfq()

        self.quote_request_book.set_filter(
            [qrb.instrument_symbol.value, usd_php_symbol]).check_quote_book_fields_list(
            {qrb.instrument_symbol.value: usd_php_symbol,
             qrb.quote_status.value: qs.accepted.value,
             qrb.status.value: Status.new.value}, 'Checking that NDF currency RFQ is placed')
        self.rfq_tile.close_tile()
        # endregion

        # region Step 3
        self.rfq_tile.crete_tile().modify_rfq_tile(from_cur=usd_currency, to_cur=ndf_currency,
                                                   near_qty=self.qty, near_tenor=near_tenor,
                                                   client=client, single_venue=venue,
                                                   far_tenor=far_tenor, far_qty=self.qty)
        self.rfq_tile.send_rfq()
        self.quote_request_book.set_filter(
            [qrb.instrument_symbol.value, usd_php_symbol]).check_quote_book_fields_list(
            {qrb.instrument_symbol.value: usd_php_symbol,
             qrb.quote_status.value: qs.accepted.value,
             qrb.status.value: Status.new.value}, 'Checking that NDF currency SWAP RFQ is placed')
        # endregion

    @try_except
    def run_post_conditions(self):
        self.rfq_tile.close_tile()
