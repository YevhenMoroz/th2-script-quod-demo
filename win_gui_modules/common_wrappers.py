from th2_grpc_act_gui_quod import order_ticket_pb2
from th2_grpc_act_gui_quod.common_pb2 import EmptyRequest, BaseTileData


class BaseTileDetails:
    def __init__(self, base: EmptyRequest = None, window_index: int = None):
        if base is not None and window_index is not None:
            self.base_details = BaseTileData(base=base, windowIndex=window_index)
        elif base is not None:
            self.base_details = BaseTileData(base=base)
        elif window_index is not None:
            self.base_details = BaseTileData(windowIndex=window_index)
        else:
            self.base_details = BaseTileData()

    def set_window_index(self, index: int):
        self.base_details.windowIndex = index

    def set_default_params(self, base_request):
        self.base_details.base.CopyFrom(base_request)

    def build(self):
        return self.base_details


class CommissionsDetails:
    def __init__(self, commission_details: order_ticket_pb2.CommissionsDetails()):
        self.request = commission_details

    def toggle_manual(self):
        self.request.toggleManual = True

    def add_commission(self, basis: str = None, rate: str = None, amount: str = None, currency: str = None):
        var = self.request.commissionsTableParams.add()
        if basis is not None:
            var.basis = basis
        if rate is not None:
            var.rate = rate
        if amount is not None:
            var.amount = amount
        if currency is not None:
            var.currency = currency
