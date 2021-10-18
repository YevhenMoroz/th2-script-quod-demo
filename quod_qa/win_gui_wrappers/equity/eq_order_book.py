from quod_qa.win_gui_wrappers.base_order_book import BaseOrderBook
from stubs import Stubs
from win_gui_modules.order_book_wrappers import OrdersDetails, OrderInfo, CancelOrderDetails


class EQOrderBook(BaseOrderBook):
    def __init__(self, case_id, base_request):
        super().__init__(case_id, base_request)
        self.order_details = OrdersDetails()
        self.order_info = OrderInfo()
        self.set_order_details()
        self.grpc_call_cancel_order = None

    def cancel_order(self, cancel_children: bool):
        self.grpc_call = Stubs.win_act_order_book.cancelOrder
        self.request_details = CancelOrderDetails()
        super().cancel_order(cancel_children)


