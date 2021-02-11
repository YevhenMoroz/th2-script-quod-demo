from th2_grpc_act_gui_quod import order_book_pb2

from utils.order_book_wrappers import ModifyOrderDetails, SubOrdersDetails, SubOrder
from utils.services import Services
from utils.base_test import BaseTest
from utils.wrappers import *
from utils.order_ticket_wrappers import OrderTicketDetails, NewOrderDetails
from grpc_modules.verifier_pb2_grpc import VerifierStub
from grpc_modules.verifier_pb2 import CheckpointRequest


class QAP_1641(BaseTest):

    def __init__(self, services: Services, parent_event):
        super().__init__(services)
        self.create_test_event(parent_event, "QAP-1641", "[TWAP] Check implement of MaxParticipation for TWAP")

    def create_checkpoint(self):
        verifier = VerifierStub(self._channels.verifier_channel)
        request = CheckpointRequest(description="TestCheckpoint", parent_event_id=self._event_id)
        return verifier.createCheckpoint(request).checkpoint

    def execute(self):
        qty = "10000"
        limit = "1.2"
        lookup = "PARA_L"

        order_ticket = OrderTicketDetails()
        order_ticket.set_quantity(qty)
        order_ticket.set_limit(limit)
        order_ticket.set_client("CLIENT1")
        order_ticket.set_order_type("Limit")
        order_ticket.set_care_order("yaroslavk", True)

        new_order_details = NewOrderDetails()
        new_order_details.set_lookup_instr(lookup)
        new_order_details.set_order_details(order_ticket)
        new_order_details.set_default_params(self.get_base_request())

        call = self.call

        set_base(self._session_id, self._event_id)

        act = self._services.order_ticket_service
        act2 = self._services.order_book_service

        call(act.placeOrder, new_order_details.build())

        order_ticket = OrderTicketDetails()
        twap_strategy = order_ticket.add_twap_strategy("Quod TWAP")
        twap_strategy.set_start_date("Now", "0.1")
        twap_strategy.set_end_date("Now", "0.6")
        twap_strategy.set_waves("5")
        twap_strategy.set_max_participation("20")

        modify_order_details = ModifyOrderDetails()
        modify_order_details.set_default_params(self.get_base_request())
        modify_order_details.set_order_details(order_ticket)

        call(act2.splitOrder, modify_order_details.build())

        sub_order1 = SubOrder()
        sub_order1.set_order_details(["subOrder1.qty", "Qty"])
        sub_order2 = SubOrder()
        sub_order2.set_order_details(["subOrder2.qty", "Qty"])

        sub_order_details = SubOrdersDetails()
        sub_order_details.set_default_params(self.get_base_request())
        sub_order_details.set_sub_orders_type(order_book_pb2.SubOrdersDetails.SubOrdersType.CHILD_ORDERS)
        sub_order_details.set_extraction_id("order.subOrder")
        sub_order_details.set_order_info([sub_order1, sub_order2])

        call(act2.getSubOrdersDetails, sub_order_details.build())
