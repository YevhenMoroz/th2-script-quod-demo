from quod_qa.win_gui_wrappers.base_order_book import BaseOrderBook
from stubs import Stubs
from win_gui_modules.order_book_wrappers import FXOrdersDetails, FXOrderInfo, OrdersDetails, OrderInfo


class FXChildBook(BaseOrderBook):
    def __init__(self, case_id, base_request):
        super().__init__(case_id, base_request)
        self.order_details = OrdersDetails()
        self.order_info = OrderInfo()
        self.set_order_details()
        self.get_orders_details_call = Stubs.win_act_order_book.getChildOrdersDetails
