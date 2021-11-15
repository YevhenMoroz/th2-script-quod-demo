from th2_grpc_act_gui_quod import order_ticket_fx_pb2
from th2_grpc_act_gui_quod.order_ticket_pb2 import NewOrderDetails as _NewOrderDetails
from th2_grpc_act_gui_quod.order_ticket_fx_pb2 import NewFxOrderDetails as _NewFXOrderDetails
from win_gui_modules.order_ticket import OrderTicketDetails, FXOrderDetails


class NewOrderDetails:

    def __init__(self, base_request=None):
        self.new_order_details = _NewOrderDetails()
        if base_request is not None:
            self.new_order_details.base.CopyFrom(base_request)

    def set_order_details(self, order_details: OrderTicketDetails):
        self.new_order_details.orderDetails.CopyFrom(order_details.build())

    def set_lookup_instr(self, lookup_symbol: str):
        self.new_order_details.instrLookupSymbol = lookup_symbol

    def set_default_params(self, base_request):
        self.new_order_details.base.CopyFrom(base_request)

    def build(self):
        return self.new_order_details


class NewFxOrderDetails:

    def __init__(self, base_request, order_details: FXOrderDetails, isMM: bool = False):
        self.new_fx_oder_details = order_ticket_fx_pb2.NewFxOrderDetails()
        self.new_fx_oder_details.base.CopyFrom(base_request)
        self.new_fx_oder_details.fxOrderDetails.CopyFrom(order_details.build())
        self.new_fx_oder_details.isMM = isMM

    def build(self):
        return self.new_fx_oder_details
