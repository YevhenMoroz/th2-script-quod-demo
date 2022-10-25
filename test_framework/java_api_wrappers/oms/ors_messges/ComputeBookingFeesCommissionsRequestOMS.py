from dataclasses import dataclass
from typing import List

from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.java_api_wrappers.ors_messages.ComputeBookingFeesCommissionsRequest import \
    ComputeBookingFeesCommissionsRequest


@dataclass
class OrderAllocBlockInstance:
    cl_ord_id: str
    order_id: str
    post_trade_status: str


@dataclass
class ExecAllocBlockInstance:
    exec_qty: str
    exec_id: str
    exec_price: str
    post_trade_exec_status: str


class ComputeBookingFeesCommissionsRequestOMS(ComputeBookingFeesCommissionsRequest):
    def __init__(self, data_set: BaseDataSet, parameters: dict = None):
        super().__init__(data_set, parameters)
        self.__data_set = data_set
        self.__list_exec_alloc_block = []
        self.__list_order_alloc_block = []

    def set_list_of_exec_alloc_block(self, exec_qty, exec_id, exec_price, post_trade_exec_status):
        self.__list_exec_alloc_block.append(
            ExecAllocBlockInstance(exec_qty, exec_id, exec_price, post_trade_exec_status))

    def set_list_of_order_alloc_block(self, cl_ord_id, order_id, post_trade_status):
        self.__list_order_alloc_block.append(OrderAllocBlockInstance(cl_ord_id, order_id, post_trade_status))

    def set_default_compute_booking_request(self, qty) -> None:
        instance_order_alloc_block = []
        for instance in self.__list_order_alloc_block:
            instance_order_alloc_block.append({'ClOrdID': instance.cl_ord_id, 'OrdID': instance.order_id,
                                               'PostTradeStatus': instance.post_trade_status})
        instance_exec_alloc_block = []
        for instance in self.__list_exec_alloc_block:
            instance_exec_alloc_block.append({'ExecQty': instance.exec_qty, 'ExecID': instance.exec_id,
                                              'ExecPrice': instance.exec_price,
                                              'PostTradeExecStatus': instance.post_trade_exec_status})
        base_parameters = {
            'SEND_SUBJECT': 'QUOD.ORS.ALLOC.FE',
            'REPLY_SUBJECT': 'QUOD.FE.ORS',
            'ComputeBookingFeesCommissionsRequestBlock': {
                'OrdAllocList': {
                    'OrdAllocBlock': instance_order_alloc_block},
                'ExecAllocList': {
                    'ExecAllocBlock': instance_exec_alloc_block},
                'Qty': qty,
                'AccountGroupID': self.__data_set.get_client_by_name('client_1'),
                'AvgPx': '20',
                'RecomputeInSettlCurrency': 'N'
            }
        }
        super().change_parameters(base_parameters)
