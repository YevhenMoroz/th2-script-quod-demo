from utils.services import Services
from utils.base_test import BaseTest
from utils.wrappers import *
from utils.order_ticket_wrappers import OrderTicketDetails, NewOrderDetails
from grpc_modules.verifier_pb2_grpc import VerifierStub
from grpc_modules.verifier_pb2 import CheckpointRequest
from custom import basic_custom_actions as bca


class ExampleCareFix(BaseTest):

    def __init__(self, services: Services, parent_event):
        super().__init__(services)
        self.create_test_event(parent_event, "TestN-1234", "[Care][Fix] Usage example")

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
        order_ticket.set_client("CLIENT1")
        order_ticket.set_order_type("Limit")
        order_ticket.set_care_order("Desk of SalesDealers 1 (CL)")

        new_order_details = NewOrderDetails()
        new_order_details.set_lookup_instr(lookup)
        new_order_details.set_order_details(order_ticket)
        new_order_details.set_default_params(self.get_base_request())

        NOS_1_params = {
            'Side': '1',
            'OrderQty': qty,
            'Price': limit,
            'OrdType': '2',
            'ClOrdID': '*',
            'ChildOrderID': '*',
            'TransactTime': '*',
            'ExDestination': 'TRQX',
            'Instrument': {
                'Symbol': lookup
            }
        }

        call = self.call

        checkpoint = self.create_checkpoint()
        set_base(self._session_id, self._event_id)

        act = self._services.order_ticket_service
        common_act = self._services.main_win_service

        call(act.placeOrder, new_order_details.build())
        order_info_extraction = "getOrderInfo"
        call(common_act.getOrderFields, fields_request(order_info_extraction, ["order.status", "Sts"]))
        call(common_act.verifyEntities, verification(order_info_extraction, "checking order",
                                                     [verify_ent("Order Status", "order.status", "Sent")]))
        call(common_act.acceptOrder, accept_order_request(lookup, qty, limit))
        direct_params = direct_order_request(lookup, qty, limit, "100")
        call(common_act.directOrder, direct_params)

        self.check_fix(checkpoint, NOS_1_params)

        child_info_extraction = "getChildOrderInfo"
        call(common_act.getChildOrderStatus, child_fields_request(child_info_extraction, ["order.status", "Sts"], direct_params))
        call(common_act.verifyEntities, verification(child_info_extraction, "checking child order",
                                                     [verify_ent("Order Status", "order.status", "Open")]))
