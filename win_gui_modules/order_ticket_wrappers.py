from th2_grpc_act_gui_quod.order_ticket_pb2 import NewOrderDetails as _NewOrderDetails
from win_gui_modules.order_ticket import OrderTicketDetails


class NewOrderDetails:

    def __init__(self):
        self.new_order_details = _NewOrderDetails()

    def set_order_details(self, order_details: OrderTicketDetails):
        self.new_order_details.orderDetails.CopyFrom(order_details.build())

    def set_lookup_instr(self, lookup_symbol: str):
        self.new_order_details.instrLookupSymbol = lookup_symbol

    def set_default_params(self, base_request):
        self.new_order_details.base.CopyFrom(base_request)

    def build(self):
        return self.new_order_details
