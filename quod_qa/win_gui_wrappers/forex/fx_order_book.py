from quod_qa.win_gui_wrappers.base_order_book import BaseOrderBook
from stubs import Stubs
from win_gui_modules.order_book_wrappers import FXOrdersDetails, FXOrderInfo


class FXOrderBook(BaseOrderBook):
    def __init__(self, case_id, base_request):
        super().__init__(case_id, base_request)
        self.order_details = FXOrdersDetails()
        self.order_info = FXOrderInfo()
        self.set_order_details()
        self.grpc_call = Stubs.win_act_order_book_fx.getOrdersDetails
