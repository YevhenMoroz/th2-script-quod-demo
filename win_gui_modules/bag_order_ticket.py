from dataclasses import dataclass
from typing import List

from th2_grpc_act_gui_quod import bag_mgt_pb2
from th2_grpc_act_gui_quod.bag_mgt_pb2 import OrderBagTicketDetails, OrderBagBookDetails
from th2_grpc_act_gui_quod.common_pb2 import EmptyRequest


class PegsOrdDetails:
    def __init__(self):
        self.order = OrderBagTicketDetails.PegsOrdDetails()

    def set_price_type(self, price_type: str):
        self.order.priceType = price_type

    def set_price_offset(self, price_offset: str):
        self.order.priceOffset = price_offset

    def set_scope(self, scope: str):
        self.order.scope = scope

    def set_offset_type(self, offset_type: str):
        self.order.offsetType = offset_type

    def build(self):
        return self.order


class SubLevelDetails:
    def __init__(self):
        self.order = OrderBagTicketDetails.SubLevelDetails()

    def set_number(self, number: str):
        self.order.number = number

    def set_filter(self, filter_list: list):
        length = len(filter_list)
        i = 0
        while i < length:
            self.order.filter[filter_list[i]] = filter_list[i + 1]
            i += 2

    def build(self):
        return self.order


class BagOrderTicketDetails:

    def __init__(self):
        self.order = bag_mgt_pb2.OrderBagTicketDetails()

    def set_qty(self, qty: str):
        self.order.qty = qty

    def set_display_qty(self, display_qty: str):
        self.order.displayQty = display_qty

    def set_price(self, price: str):
        self.order.price = price

    def confirm_ticket_creation(self):
        self.order.confirm = OrderBagTicketDetails.Confirmation.OK

    def cancel_ticket_creation(self):
        self.order.confirm = OrderBagTicketDetails.Confirmation.CANCEL

    def add_pegs_details(self, pegs_details: PegsOrdDetails):
        self.order.pegsOrdDetails.CopyFrom(pegs_details)

    def modify_wave_bag_details(self, wave_bag_details: List[SubLevelDetails]):
        for details in wave_bag_details:
            self.order.subLevelDetails.append(details)

    def build(self):
        return self.order


class OrderBagWaveCreationDetails:

    def __init__(self, base_request, order_details: OrderBagTicketDetails):
        self.oder_bag_creation_details = bag_mgt_pb2.OrderBagWaveCreationDetails()
        self.oder_bag_creation_details.base.CopyFrom(base_request)
        self.oder_bag_creation_details.orderBagTicketDetails.CopyFrom(order_details)

    def set_default_params(self, base_request):
        self.oder_bag_creation_details.base.CopyFrom(base_request)

    def set_filter(self, filter_list: list):
        length = len(filter_list)
        i = 0
        while i < length:
            self.oder_bag_creation_details.filter[filter_list[i]] = filter_list[i + 1]
            i += 2

    def add_bag_ticket_details(self, order_details: BagOrderTicketDetails):
        return self.oder_bag_creation_details.orderBagTicketDetails.CopyFrom(order_details.build())

    def build(self):
        return self.oder_bag_creation_details


@dataclass
class ExtractionBagFieldsDetails:
    value: str
    column_name: str


class GetOrderBagBookDetailsRequest:
    def __init__(self):
        self.base_params = None
        self.extraction_id = None
        self.orderbag_details = bag_mgt_pb2.OrderBagBookDetails()

    @staticmethod
    def create(order_info_list: list = None, info=None):
        orderbag_details = GetOrderBagBookDetailsRequest()

        if order_info_list is not None:
            for i in order_info_list:
                orderbag_details.add_single_bag_order_info(i)

        if info is not None:
            orderbag_details.add_single_bag_order_info(info)

        return orderbag_details

    def set_extraction_id(self, extraction_id: str):
        self.extraction_id = extraction_id

    def set_filter(self, filter_list: list):
        length = len(filter_list)
        i = 0
        while i < length:
            self.orderbag_details.filter[filter_list[i]] = filter_list[i + 1]
            i += 2

    def add_bag_order_info(self, bag_order_info_list: list):
        for bag_order_info in bag_order_info_list:
            self.orderbag_details.orderInfo.append(bag_order_info.build())

    def add_single_bag_order_info(self, bag_order_info):
        self.orderbag_details.orderInfo.append(bag_order_info.build())

    def set_default_params(self, base_request):
        self.base_params = base_request

    def build(self):
        request = bag_mgt_pb2.GetOrderBagBookDetailsRequest()
        request.base.CopyFrom(self.base_params)
        request.extractionId = self.extraction_id
        request.orderBagDetails.CopyFrom(self.orderbag_details)
        return request

    def details(self):
        return self.orderbag_details


class ExtractionBagOrderAction:
    def __init__(self):
        self.extraction_action = bag_mgt_pb2.ExtractionBagAction()

    @staticmethod
    def create_extraction_action(extraction_detail: ExtractionBagFieldsDetails = None, extraction_details: list = None):
        action = ExtractionBagOrderAction()
        if extraction_detail is not None:
            action.add_detail(extraction_detail)

        if extraction_details is not None:
            action.add_details(extraction_details)

        return action

    def add_detail(self, detail: ExtractionBagFieldsDetails):
        var = self.extraction_action.bagOrderDetails.add()
        var.value = detail.value
        var.colName = detail.column_name

    def add_details(self, details: list):
        for detail in details:
            self.add_detail(detail)

    def build(self):
        return self.extraction_action


class BagOrderInfo:
    def __init__(self):
        self.bagorder_info = bag_mgt_pb2.BagOrderInfo()

    @staticmethod
    def create(action=None, actions: list = None, sub_orders: GetOrderBagBookDetailsRequest = None):
        bagorder_info = BagOrderInfo()
        if action is not None:
            bagorder_info.add_single_extraction_action(action)

        if actions is not None:
            bagorder_info.add_extraction_actions(actions)

        if sub_orders is not None:
            bagorder_info.set_sub_orders_details(sub_orders)

        return bagorder_info

    def set_sub_orders_details(self, sub_orders: GetOrderBagBookDetailsRequest):
        self.bagorder_info.subOrders.CopyFrom(sub_orders.details())

    def set_number(self, number: int):
        self.bagorder_info.number = number

    def add_extraction_actions(self, bagorder_info_list: list):
        for bagorder_info in bagorder_info_list:
            self.add_single_extraction_action(bagorder_info)

    def add_single_extraction_action(self, bagorder_info):
        orderbag_details = bag_mgt_pb2.BagAction()
        if isinstance(bagorder_info, ExtractionBagOrderAction):
            orderbag_details.extractionAction.CopyFrom(bagorder_info.build())
        else:
            raise Exception("Unsupported action type")
        self.bagorder_info.orderAction.append(orderbag_details)

    def build(self):
        return self.bagorder_info
