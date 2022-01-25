import random
from pathlib import Path
from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.win_gui_wrappers.forex.fx_quote_request_book import FXQuoteRequestBook
from test_framework.win_gui_wrappers.forex.rfq_tile import RFQTile
from test_framework.win_gui_wrappers.fe_trading_constant import QuoteRequestBookColumns as qrb, QuoteStatus as qs, \
    Status

case_qty = str(random.randint(1000000, 2000000))

class QAP_6(TestCase):
    def __init__(self, report_id, session_id=None, data_set=None):
        super().__init__(report_id, session_id, data_set)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.rfq_tile = RFQTile(self.test_id, self.session_id)
        self.quote_request_book = FXQuoteRequestBook(self.test_id, self.session_id)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        case_eur_currency = self.data_set.get_currency_by_name('currency_eur')
        case_usd_currency = self.data_set.get_currency_by_name('currency_usd')
        case_ndf_currency = self.data_set.get_currency_by_name('currency_php')
        case_eur_usd_symbol = self.data_set.get_symbol_by_name('symbol_1')
        case_usd_php_symbol = self.data_set.get_symbol_by_name('symbol_ndf_1')
        case_near_tenor = self.data_set.get_tenor_by_name('tenor_spot')
        case_far_tenor = self.data_set.get_tenor_by_name('tenor_1w')
        case_venue = self.data_set.get_venue_by_name('venue_1')
        case_client = self.data_set.get_client_by_name("client_1")
        # region Step 1
        self.rfq_tile.crete_tile().modify_rfq_tile(from_cur=case_eur_currency, to_cur=case_usd_currency,
                                                   near_qty=case_qty, near_tenor=case_near_tenor,
                                                   client=case_client, single_venue=case_venue)
        self.rfq_tile.send_rfq()

        self.quote_request_book.set_filter(
            [qrb.instrument_symbol.value, case_usd_php_symbol]).check_quote_book_fields_list(
            {qrb.instrument_symbol.value: case_eur_usd_symbol,
             qrb.quote_status.value: qs.accepted.value,
             qrb.status.value: Status.new.value}, 'Checking that regular currency RFQ is placed')
        self.rfq_tile.close_tile()
        # endregion

        # region Step 2
        self.rfq_tile.crete_tile().modify_rfq_tile(from_cur=case_usd_currency, to_cur=case_ndf_currency,
                                                   near_qty=case_qty, near_tenor=case_near_tenor,
                                                   client=case_client, single_venue=case_venue)
        self.rfq_tile.send_rfq()

        self.quote_request_book.set_filter(
            [qrb.instrument_symbol.value, case_usd_php_symbol]).check_quote_book_fields_list(
            {qrb.instrument_symbol.value: case_usd_php_symbol,
             qrb.quote_status.value: qs.accepted.value,
             qrb.status.value: Status.new.value}, 'Checking that NDF currency RFQ is placed')
        self.rfq_tile.close_tile()
        # endregion

        # region Step 3
        self.rfq_tile.crete_tile().modify_rfq_tile(from_cur=case_usd_currency, to_cur=case_ndf_currency,
                                                   near_qty=case_qty, near_tenor=case_near_tenor,
                                                   client=case_client, single_venue=case_venue,
                                                   far_tenor=case_far_tenor, far_qty=case_qty)
        self.rfq_tile.send_rfq()
        self.quote_request_book.set_filter(
            [qrb.instrument_symbol.value, case_usd_php_symbol]).check_quote_book_fields_list(
            {qrb.instrument_symbol.value: case_usd_php_symbol,
             qrb.quote_status.value: qs.accepted.value,
             qrb.status.value: Status.new.value}, 'Checking that NDF currency SWAP RFQ is placed')
        # endregion
    @try_except
    def run_post_conditions(self):
        self.rfq_tile.close_tile()
