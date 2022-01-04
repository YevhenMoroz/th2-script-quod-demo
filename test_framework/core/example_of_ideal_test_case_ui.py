from pathlib import Path

from test_framework.core.test_case import TestCase
from test_framework.win_gui_wrappers.base_window import decorator_try_except
from test_framework.win_gui_wrappers.fe_trading_constant import Side
from test_framework.win_gui_wrappers.fe_trading_constant import ExecSts
from test_framework.win_gui_wrappers.fe_trading_constant import OrderBookColumns as ob
from test_framework.win_gui_wrappers.forex.fx_order_book import FXOrderBook
from test_framework.win_gui_wrappers.forex.rfq_tile import RFQTile

case_from_currency = "EUR"
case_to_currency = "USD"
case_qty = "1000000"
case_near_tenor = "SPOT"
sell_side = Side.sell.value


class QAP_Example(TestCase):
    def __init__(self, report_id, session_id=None, data_set=None):
        super().__init__(report_id, session_id, data_set)
        self.rfq_tile = None
        self.order_book = None

    @decorator_try_except(test_id=Path(__file__).name[:-3])
    def pre_conditions_and_run(self):
        client = self.data_set.get_client_by_name("client_1")
        venue = self.data_set.get_venue_by_name("venue_1")
        self.rfq_tile = RFQTile(self.test_id, self.session_id)
        self.rfq_tile.crete_tile().modify_rfq_tile(from_cur=case_from_currency, to_cur=case_to_currency,
                                                   near_qty=case_qty, near_tenor=case_near_tenor,
                                                   client=client, single_venue=venue)
        self.rfq_tile.send_rfq()
        self.rfq_tile.place_order(sell_side)
        self.order_book = FXOrderBook(self.test_id, self.session_id)
        self.order_book.check_order_fields_list({ob.sts.value: ExecSts.terminated.value})

    @decorator_try_except(test_id=Path(__file__).name[:-3])
    def post_conditions(self):
        self.rfq_tile.close_tile()
