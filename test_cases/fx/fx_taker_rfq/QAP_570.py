from pathlib import Path
from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.win_gui_wrappers.forex.fx_order_book import FXOrderBook
from test_framework.win_gui_wrappers.forex.fx_quote_book import FXQuoteBook
from test_framework.win_gui_wrappers.forex.fx_quote_request_book import FXQuoteRequestBook
from test_framework.win_gui_wrappers.forex.rfq_tile import RFQTile
from test_framework.win_gui_wrappers.fe_trading_constant import OrderBookColumns as ob, Status as st, ExecSts, Side


class QAP_570(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None):
        super().__init__(report_id, session_id, data_set)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.rfq_tile = RFQTile(self.test_id, self.session_id)
        self.order_book = FXOrderBook(self.test_id, self.session_id)
        self.quote_request_book = FXQuoteRequestBook(self.test_id, self.session_id)
        self.quote_book = FXQuoteBook(self.test_id, self.session_id)
        self.qty1 = '1000000'
        self.qty2 = '11'
        self.qty3 = '111.5'

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        eur_currency = self.data_set.get_currency_by_name('currency_eur')
        usd_currency = self.data_set.get_currency_by_name('currency_usd')
        eur_usd_symbol = self.data_set.get_symbol_by_name('symbol_1')
        near_tenor = self.data_set.get_tenor_by_name('tenor_spot')
        venue = self.data_set.get_venue_by_name('venue_1')
        client = self.data_set.get_client_by_name("client_1")

        # region Step 1
        self.rfq_tile.crete_tile().modify_rfq_tile(from_cur=eur_currency, to_cur=usd_currency,
                                                   near_qty=self.qty1, near_tenor=near_tenor,
                                                   client=client, single_venue=venue)
        self.rfq_tile.crete_tile().modify_rfq_tile(near_qty=self.qty2)
        self.rfq_tile.send_rfq()
        # endregion
        # region Step 2
        self.rfq_tile.place_order(side=Side.buy.value)
        self.order_book.set_filter(
            [ob.symbol.value, eur_usd_symbol, ob.qty.value, self.qty2]).check_order_fields_list(
            {ob.symbol.value: eur_usd_symbol,
             ob.sts.value: st.terminated.value,
             ob.exec_sts.value: ExecSts.filled.value,
             ob.qty.value: self.qty2}, 'Checking currency value in order book')
        # endregion
        # region Step 3
        self.rfq_tile.crete_tile().modify_rfq_tile(near_qty=self.qty3)
        self.rfq_tile.send_rfq()
        # endregion
        # region Step 4
        self.rfq_tile.place_order(side=Side.buy.value)
        self.order_book.set_filter(
            [ob.symbol.value, eur_usd_symbol, ob.qty.value, self.qty3]).check_order_fields_list(
            {ob.symbol.value: eur_usd_symbol,
             ob.sts.value: st.terminated.value,
             ob.exec_sts.value: ExecSts.filled.value,
             ob.qty.value: self.qty3}, 'Checking currency value in order book')
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.rfq_tile.close_tile()
