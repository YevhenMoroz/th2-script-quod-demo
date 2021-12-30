from th2_grpc_act_gui_quod.common_pb2 import ScrollingOperation

from test_framework.win_gui_wrappers.base_order_book import BaseOrderBook
from stubs import Stubs
from win_gui_modules.common_wrappers import GridScrollingDetails
from win_gui_modules.order_book_wrappers import FXOrdersDetails, FXOrderInfo, CancelFXOrderDetails


class FXOrderBook(BaseOrderBook):
    def __init__(self, case_id, session_id):
        super().__init__(case_id, session_id)
        self.order_details = FXOrdersDetails()
        self.order_info = FXOrderInfo()
        self.scrolling_details = GridScrollingDetails()
        self.cancel_order_details = CancelFXOrderDetails(self.base_request)
        self.set_order_details()
        self.get_orders_details_call = Stubs.win_act_order_book_fx.getOrdersDetails
        self.cancel_order_call = Stubs.win_act_order_book_fx.cancelOrder
        self.scrolling_operation = ScrollingOperation
        self.order_book_grid_scrolling_call = Stubs.win_act_order_book.orderBookGridScrolling






