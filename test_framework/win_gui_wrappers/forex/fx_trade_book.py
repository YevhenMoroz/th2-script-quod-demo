from stubs import Stubs
from test_framework.win_gui_wrappers.base_trades_book import BaseTradesBook
from win_gui_modules.order_book_wrappers import OrdersDetails, OrderInfo


class FXTradeBook(BaseTradesBook):
    def __init__(self, case_id, session_id):
        super().__init__(case_id, session_id)
        self.order_details = OrdersDetails()
        self.order_info = OrderInfo()
        self.set_order_details()
        self.get_trade_book_details_call = Stubs.win_act_order_book.getTradeBookDetails
