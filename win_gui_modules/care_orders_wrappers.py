from th2_grpc_act_gui_quod import care_orders_pb2
from th2_grpc_act_gui_quod.care_orders_pb2 import TransferPoolDetails
from th2_grpc_act_gui_quod.common_pb2 import EmptyRequest


class TransferPoolDetailsCLass:

    def __init__(self):
        self.order = care_orders_pb2.TransferPoolDetails()

    def confirm_ticket_accept(self):
        self.order.confirm = TransferPoolDetails.Confirmation.ACCEPT

    def cancel_ticket_reject(self):
        self.order.confirm = TransferPoolDetails.Confirmation.REJECT

    def build(self):
        return self.order


class InternalTransferActionDetails:

    def __init__(self, base_request, order_details: TransferPoolDetails):
        self.internal_transfer_details = care_orders_pb2.InternalTransferActionDetails()
        self.internal_transfer_details.base.CopyFrom(base_request)
        self.internal_transfer_details.transferPoolDetails.CopyFrom(order_details)

    def set_default_params(self, base_request):
        self.internal_transfer_details.base.CopyFrom(base_request)

    def set_filter(self, filter_list: list):
        length = len(filter_list)
        i = 0
        while i < length:
            self.internal_transfer_details.filter[filter_list[i]] = filter_list[i + 1]
            i += 2

    def add_transfer_pool_details(self, order_details: TransferPoolDetails):
        return self.internal_transfer_details.transferPoolDetails.CopyFrom(order_details.build())

    def build(self):
        return self.internal_transfer_details







