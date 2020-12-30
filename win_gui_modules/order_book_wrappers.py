from dataclasses import dataclass

from .order_ticket import OrderTicketDetails
from grpc_modules import order_book_pb2


class ModifyOrderDetails:
    def __init__(self):
        self.modify_order_details = order_book_pb2.ModifyOrderDetails()

    def set_order_details(self, order_details: OrderTicketDetails):
        self.modify_order_details.orderDetails.CopyFrom(order_details.build())

    def set_filter(self, filter_list: list):
        length = len(filter_list)
        i = 0
        while i < length:
            self.modify_order_details.filter[filter_list[i]] = filter_list[i + 1]
            i += 2

    def set_default_params(self, base_request):
        self.modify_order_details.base.CopyFrom(base_request)

    def build(self):
        return self.modify_order_details


class CancelOrderDetails:
    def __init__(self):
        self.cancel_order_details = order_book_pb2.CancelOrderDetails()

    def set_filter(self, filter_list: list):
        length = len(filter_list)
        i = 0
        while i < length:
            self.cancel_order_details.filter[filter_list[i]] = filter_list[i + 1]
            i += 2

    def set_default_params(self, base_request):
        self.cancel_order_details.base.CopyFrom(base_request)

    def set_comment(self, comment: str):
        self.cancel_order_details.comment = comment

    def set_cancel_children(self, cancel_children: bool):
        self.cancel_order_details.cancelChildren.value = cancel_children

    def build(self):
        return self.cancel_order_details


@dataclass
class ExtractionDetail:
    name: str
    column_name: str


class OrdersDetails:
    def __init__(self):
        self.base_params = None
        self.extraction_id = None
        self.orders_details = order_book_pb2.OrdersDetailsInfo()

    @staticmethod
    def create(info_list: list = None, info=None):
        order_details = OrdersDetails()

        if info_list is not None:
            for i in info_list:
                order_details.add_single_extraction_info(i)

        if info is not None:
            order_details.add_single_extraction_info(info)

        return order_details

    @staticmethod
    def from_info(sub_orders: list):
        order_details = OrdersDetails()
        order_details.set_extraction_info(sub_orders)
        return order_details

    def set_extraction_id(self, extraction_id: str):
        self.extraction_id = extraction_id

    def set_filter(self, filter_list: list):
        length = len(filter_list)
        i = 0
        while i < length:
            self.orders_details.filter[filter_list[i]] = filter_list[i + 1]
            i += 2

    def set_extraction_info(self, sub_orders: list):
        for sub_order in sub_orders:
            self.orders_details.extractionInfo.append(sub_order.build())

    def set_one_extraction_info(self, sub_order):
        self.orders_details.extractionInfo.append(sub_order.build())

    def add_single_extraction_info(self, sub_order):
        self.orders_details.extractionInfo.append(sub_order.build())

    def set_default_params(self, base_request):
        self.base_params = base_request

    def extract_length(self, count_id: str):
        self.orders_details.extractCount = True
        self.orders_details.countId = count_id

    def request(self):
        request = order_book_pb2.GetOrdersDetailsRequest()
        request.base.CopyFrom(self.base_params)
        request.extractionId = self.extraction_id
        request.orderDetails.CopyFrom(self.orders_details)
        return request

    def details(self):
        return self.orders_details


class ExtractionInfo:
    def __init__(self):
        self.extraction_info = order_book_pb2.ExtractionInfo()

    @staticmethod
    def create(detail: ExtractionDetail = None, data: list = None, sub_order_details: OrdersDetails = None):
        info = ExtractionInfo()
        if detail is not None:
            info.add_order_details(detail)

        if data is not None:
            for i in data:
                info.add_order_details(i)

        if sub_order_details is not None:
            info.set_sub_orders_details(sub_order_details)

        return info

    @staticmethod
    def from_data(data: list):
        info = ExtractionInfo()
        info.set_order_details(data)
        return info

    @staticmethod
    def from_sub_order_details(sub_order_details: OrdersDetails):
        info = ExtractionInfo()
        info.set_sub_orders_details(sub_order_details)
        return info

    def set_sub_orders_details(self, sub_order_details: OrdersDetails):
        self.extraction_info.subOrders.CopyFrom(sub_order_details.details())

    def set_number(self, number: int):
        self.extraction_info.number = number

    def set_order_details(self, data: list):
        length = len(data)
        i = 0
        while i < length:
            var = self.extraction_info.orderDetails.add()
            var.name = data[i]
            var.colName = data[i + 1]
            i += 2

    def add_order_details(self, data: ExtractionDetail):
        var = self.extraction_info.orderDetails.add()
        var.name = data.name
        var.colName = data.column_name

    def build(self):
        return self.extraction_info
