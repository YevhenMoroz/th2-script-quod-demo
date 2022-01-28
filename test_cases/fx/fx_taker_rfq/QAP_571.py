from pathlib import Path
from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.win_gui_wrappers.forex.fx_order_book import FXOrderBook
from test_framework.win_gui_wrappers.forex.fx_quote_book import FXQuoteBook
from test_framework.win_gui_wrappers.forex.fx_quote_request_book import FXQuoteRequestBook
from test_framework.win_gui_wrappers.forex.rfq_tile import RFQTile

qty = '5000000'
qty1 = '1000000'
qty_1m = '1m'
qty2 = '1000'
qty_1k = '1k'


class QAP_571(TestCase):
    def __init__(self, report_id, session_id=None, data_set=None):
        super().__init__(report_id, session_id, data_set)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.rfq_tile = None
        self.order_book = None
        self.quote_request_book = None
        self.quote_book = None

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        self.rfq_tile = RFQTile(self.test_id, self.session_id)
        self.order_book = FXOrderBook(self.test_id, self.session_id)
        self.quote_request_book = FXQuoteRequestBook(self.test_id, self.session_id)
        self.quote_book = FXQuoteBook(self.test_id, self.session_id)
        eur_currency = self.data_set.get_currency_by_name('currency_eur')
        usd_currency = self.data_set.get_currency_by_name('currency_usd')
        default_currency = self.data_set.get_symbol_by_name('symbol_ndf_3')
        eur_usd_symbol = self.data_set.get_symbol_by_name('symbol_1')

        # region Step 1
        self.rfq_tile.crete_tile()
        self.rfq_tile.check_currency_pair(currency_pair=default_currency)
        # endregion
        # region Step 2
        # TODO Change currency pair from drop down
        # endregion
        # region Step 3
        self.rfq_tile.crete_tile().modify_rfq_tile(from_cur=eur_currency, to_cur=usd_currency)
        self.rfq_tile.check_currency_pair(currency_pair=eur_usd_symbol)
        # endregion
        # region Step 4
        self.rfq_tile.crete_tile().modify_rfq_tile(near_qty=qty)
        self.rfq_tile.check_qty(near_qty=qty)
        # endregion
        # region Step 5
        self.rfq_tile.crete_tile().modify_rfq_tile(near_qty=qty_1m)
        self.rfq_tile.check_qty(near_qty=qty1)
        self.rfq_tile.crete_tile().modify_rfq_tile(near_qty=qty_1k)
        self.rfq_tile.check_qty(near_qty=qty2)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.rfq_tile.close_tile()
