from utils.order_book_wrappers import OrdersDetails, OrderInfo
from grpc_modules import order_ticket_pb2_grpc, order_book_pb2, order_book_pb2_grpc, win_act_pb2_grpc
from channels import Channels
from utils.base_test import BaseTest
from utils.wrappers import *


class DifferentOrderLevelVerification(BaseTest):

    def __init__(self, channels: Channels, parent_event):
        super().__init__(channels)
        self.create_test_event(parent_event, "TestN-1234", "Different Order Level Verification")

    def execute(self):
        call = self.call

        set_base(self._session_id, self._event_id)

        act2 = order_book_pb2_grpc.OrderBookServiceStub(self._channels.ui_act_channel)
        common_act = win_act_pb2_grpc.HandWinActStub(self._channels.ui_act_channel)

        main_order_info = OrderInfo.from_data(["mainOrderQty", "Qty"])
        sub_order1 = OrderInfo.from_data(["subOrder1Qty", "Qty"])
        sub_order2 = OrderInfo.from_data(["subOrder2Qty", "Qty"])

        sub_order1.set_sub_orders_details(OrdersDetails.from_info([sub_order2]))
        main_order_info.set_sub_orders_details(OrdersDetails.from_info([sub_order1]))

        sub_order_details = OrdersDetails()
        sub_order_details.set_default_params(self.get_base_request())
        sub_order_details.set_extraction_id("order.subOrder")
        sub_order_details.set_filter(["Order ID", "AO1201210140907080001"])
        sub_order_details.set_order_info([main_order_info])

        call(act2.getOrdersDetails, sub_order_details.request())

        call(common_act.verifyEntities, verification("order.subOrder", "checking order",
                                                     [verify_ent("Main order quantity", "mainOrderQty", "200"),
                                                      verify_ent("Order lvl 2 quantity", "subOrder1Qty", "200"),
                                                      verify_ent("Order lvl 3 quantity", "subOrder2Qty", "200")]))

