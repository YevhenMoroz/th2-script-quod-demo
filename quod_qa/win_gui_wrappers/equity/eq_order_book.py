from th2_grpc_act_gui_quod.order_book_pb2 import ReassignOrderDetails

from quod_qa.win_gui_wrappers.base_order_book import BaseOrderBook
from stubs import Stubs
from win_gui_modules.order_book_wrappers import OrdersDetails, OrderInfo, CancelOrderDetails, ModifyOrderDetails
from win_gui_modules.order_ticket_wrappers import NewOrderDetails


class EQOrderBook(BaseOrderBook):
    def __init__(self, case_id, base_request):
        super().__init__(case_id, base_request)
        self.order_info = OrderInfo()
        self.order_details = OrdersDetails()
        self.new_order_details = NewOrderDetails()
        self.modify_order_details = ModifyOrderDetails()
        self.cancel_order_details = CancelOrderDetails(base_request)
        self.reassign_order_details = ReassignOrderDetails()
        self.get_orders_details_call = Stubs.win_act_order_book.getOrdersDetails
        self.groupModifyOrder_call = Stubs.win_act_order_book.groupModify
        self.unCompleteOrder_call = Stubs.win_act_order_book.unCompleteOrder
        self.notifyDFDOrder_call = Stubs.win_act_order_book.notifyDFD
        self.reassignOrder_call = Stubs.win_act_order_book.reassignOrder
        self.completeOrder_call = Stubs.win_act_order_book.completeOrder
        self.cancel_order_call = Stubs.win_act_order_book


