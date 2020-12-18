from grpc_modules import order_ticket_pb2
from .order_ticket import OrderTicketDetails


class NewOrderDetails:

    def __init__(self):
        self.new_order_details = order_ticket_pb2.NewOrderDetails()

    def set_order_details(self, order_details: OrderTicketDetails):
        self.new_order_details.orderDetails.CopyFrom(order_details.build())

    def set_lookup_instr(self, lookup_symbol: str):
        self.new_order_details.instrLookupSymbol = lookup_symbol

    def set_default_params(self, base_request):
        self.new_order_details.base.CopyFrom(base_request)

    def build(self):
        return self.new_order_details
