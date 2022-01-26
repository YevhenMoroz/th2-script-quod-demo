from pathlib import Path
import random
from custom import basic_custom_actions as bca
from custom.verifier import Verifier
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.win_gui_wrappers.forex.fx_quote_request_book import FXQuoteRequestBook
from test_framework.win_gui_wrappers.forex.rfq_tile import RFQTile
from test_framework.win_gui_wrappers.fe_trading_constant import QuoteRequestBookColumns as qrb, QuoteStatus as qs, \
    Status


case_qty = str(random.randint(1000000, 2000000))


class QAP_566(TestCase):
    def __init__(self, report_id, session_id=None, data_set=None):
        super().__init__(report_id, session_id, data_set)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.rfq_tile = RFQTile(self.test_id, self.session_id)
        self.quote_request_book = FXQuoteRequestBook(self.test_id, self.session_id)
        self.verifier = Verifier(self.test_id)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        case_eur_currency = self.data_set.get_currency_by_name('currency_eur')
        case_usd_currency = self.data_set.get_currency_by_name('currency_usd')
        case_eur_usd_symbol = self.data_set.get_symbol_by_name('symbol_1')
        case_near_tenor = self.data_set.get_tenor_by_name('tenor_spot')
        case_venue = self.data_set.get_venue_by_name('venue_1')
        case_client = self.data_set.get_client_by_name("client_1")
        # region Step 1
        self.rfq_tile.crete_tile().modify_rfq_tile(from_cur=case_eur_currency, to_cur=case_usd_currency,
                                                   near_qty=case_qty, near_tenor=case_near_tenor,
                                                   client=case_client, single_venue=case_venue)
        self.rfq_tile.send_rfq()

        self.quote_request_book.set_filter(
            [qrb.instrument_symbol.value, case_eur_usd_symbol, qrb.qty.value, case_qty]).check_quote_book_fields_list(
            {qrb.instrument_symbol.value: case_eur_usd_symbol,
             qrb.quote_status.value: qs.accepted.value,
             qrb.status.value: Status.new.value}, 'Checking that regular currency RFQ is placed')
        # endregion

        # region Step 2
        bid = self.rfq_tile.extract_price(best_bid='best_bid')
        tob_len = len(bid['best_bid'][2:])
        self.verifier.set_event_name("Check digits in TOB")
        self.verifier.compare_values("Number of digits in TOB", "5", str(tob_len))
        self.verifier.verify()
        # endregion

    @try_except
    def run_post_conditions(self):
        self.rfq_tile.close_tile()


