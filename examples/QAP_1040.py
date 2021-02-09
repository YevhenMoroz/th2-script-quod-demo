from utils.services import Services
from utils.base_test import BaseTest
from utils.wrappers import *
from utils.order_ticket_wrappers import OrderTicketDetails, NewOrderDetails


class QAP_1040(BaseTest):

    def __init__(self, services: Services, parent_event):
        super().__init__(services)
        self.create_test_event(parent_event, "QAP_1040", "Verify that user can send CO, fill it from manual execution.")



    def execute(self):

        qty = "10"
        limit = "10"
        lookup = "IMP"

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

        call = self.call

        set_base(self._session_id, self._event_id)

        act = self._services.order_ticket_service
        common_act = self._services.main_win_service

        call(act.placeOrder, new_order_details.build())
        order_info_extraction = "getOrderInfo"
        call(common_act.getOrderFields, fields_request(order_info_extraction, ["order.status", "Sts"]))
        call(common_act.verifyEntities, verification(order_info_extraction, "checking order",
                                                     [verify_ent("Order Status", "order.status", "Sent")]))
        call(common_act.acceptOrder, accept_order_request(lookup, qty, limit))
        call(common_act.getOrderFields, fields_request(order_info_extraction, ["order.status", "Sts"]))
        call(common_act.verifyEntities, verification(order_info_extraction, "checking order",
                                                     [verify_ent("Order Status", "order.status", "Open")]))

