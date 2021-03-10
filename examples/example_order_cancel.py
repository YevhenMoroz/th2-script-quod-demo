from utils.order_book_wrappers import CancelOrderDetails
from utils.services import Services
from utils.base_test import BaseTest
from utils.wrappers import *
from utils.order_ticket_wrappers import OrderTicketDetails, TWAPStrategy, NewOrderDetails
from grpc_modules.verifier_pb2_grpc import VerifierStub
from grpc_modules.verifier_pb2 import CheckpointRequest
from custom import basic_custom_actions as bca


class OrderCancelExample(BaseTest):

    def __init__(self, services: Services, parent_event):
        super().__init__(services)
        self.create_test_event(parent_event, "TestN-1234", "[Care] Order Cancel Example")

    def check_fix(self, checkpoint, params):
        verifier = VerifierStub(self._channels.verifier_channel)

        verifier.submitCheckRule(
            bca.create_check_rule(
                'Check Transmitted NewOrderSingle',
                bca.filter_to_grpc('NewOrderSingle', params),
                checkpoint, 'fix-bs-eq-trqx', self._event_id
            )
        )

    def create_checkpoint(self):
        verifier = VerifierStub(self._channels.verifier_channel)
        request = CheckpointRequest(description="TestCheckpoint", parent_event_id=self._event_id)
        return verifier.createCheckpoint(request).checkpoint

    def execute(self):

        qty = "300"
        limit = "50"
        lookup = "PAR_ST"

        order_ticket = OrderTicketDetails()
        order_ticket.set_quantity(qty)
        order_ticket.set_limit(limit)
        order_ticket.set_stop_price("20")
        order_ticket.set_client("CLIENT1")
        order_ticket.set_order_type("Limit")
        order_ticket.set_care_order("Desk of SalesDealers 1 (CL)")

        new_order_details = NewOrderDetails()
        new_order_details.set_lookup_instr(lookup)
        new_order_details.set_order_details(order_ticket)
        new_order_details.set_default_params(self.get_base_request())

        call = self.call

        set_base(self._session_id, self._event_id)

        act = self._services.order_ticket_service
        common_act = self._services.main_win_service

        call(act.placeOrder, new_order_details.build())
        order_info_extraction = "getOrderInfo"
        res_map = call(common_act.getOrderFields, fields_request(order_info_extraction, ["order.id", "Order ID"]))
        print(res_map)
        order_id = res_map["order.id"]
        call(common_act.acceptOrder, accept_order_request(lookup, qty, limit))
        direct_params = direct_order_request(lookup, qty, limit, "100")
        call(common_act.directOrder, direct_params)

        act_book = self._services.order_book_service
        cancel_order_details = CancelOrderDetails()
        cancel_order_details.set_default_params(self.get_base_request())
        cancel_order_details.set_filter(["Order ID", order_id, "Lookup", "PAR_ST.[TRQX]", "Venue",
                                      "TRQX", "Security Id", "SE0000818569"])
        cancel_order_details.set_comment("Order cancelled by script")
        cancel_order_details.set_cancel_children(True)
        call(act_book.cancelOrder, cancel_order_details.build())