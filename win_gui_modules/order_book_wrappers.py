from .order_ticket import OrderTicketDetails
from th2_grpc_act_gui_quod import order_book_pb2
from dataclasses import dataclass


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
    def create(order_info_list: list = None, info=None):
        order_details = OrdersDetails()

        if order_info_list is not None:
            for i in order_info_list:
                order_details.add_single_order_info(i)

        if info is not None:
            order_details.add_single_order_info(info)

        return order_details

    def set_extraction_id(self, extraction_id: str):
        self.extraction_id = extraction_id

    def set_filter(self, filter_list: list):
        length = len(filter_list)
        i = 0
        while i < length:
            self.orders_details.filter[filter_list[i]] = filter_list[i + 1]
            i += 2

    def set_order_info(self, order_info_list: list):
        for order_info in order_info_list:
            self.orders_details.orderInfo.append(order_info.build())

    def add_single_order_info(self, order_info):
        self.orders_details.orderInfo.append(order_info.build())

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


class Criterion:
    def __init__(self):
        self.criterion = order_book_pb2.VerifyGeneratedOrderEvent.Criterion()

    def set_column_name(self, column_name: str):
        self.criterion.columnName = column_name

    def minimize(self):
        self.criterion.compareType = order_book_pb2.VerifyGeneratedOrderEvent.CompareType.MINIMIZE

    def maximize(self):
        self.criterion.compareType = order_book_pb2.VerifyGeneratedOrderEvent.CompareType.MAXIMIZE

    def build(self):
        return self.criterion


class VerifyGeneratedOrderEvent:
    def __init__(self):
        self.verify_action = order_book_pb2.VerifyGeneratedOrderEvent()

    def set_venue(self, venue: str):
        self.verify_action.venue = venue

    def set_criterion(self, criterion: Criterion):
        self.verify_action.criterion.CopyFrom(criterion.build())

    def build(self):
        return self.verify_action


class OrderAnalysisAction:
    def __init__(self):
        self.order_analysis_action = order_book_pb2.OrderAnalysisAction()

    @staticmethod
    def create_verify_generate_order_event(venue: str = None, criterion: Criterion = None):
        verify_action = VerifyGeneratedOrderEvent()
        if venue is not None:
            verify_action.set_venue(venue)
        if criterion is not None:
            verify_action.set_criterion(criterion)

        result = OrderAnalysisAction()
        result.add_action(verify_action)

        return result

    def add_action(self, action):
        if isinstance(action, VerifyGeneratedOrderEvent):
            self.order_analysis_action.verifyGeneratedOrderEvent.CopyFrom(action.build())

    def build(self):
        return self.order_analysis_action


class ExtractionAction:
    def __init__(self):
        self.extraction_action = order_book_pb2.ExtractionAction()

    @staticmethod
    def create_extraction_action(extraction_detail: ExtractionDetail = None, extraction_details: list = None):
        action = ExtractionAction()
        if extraction_detail is not None:
            action.add_detail(extraction_detail)

        if extraction_details is not None:
            action.add_details(extraction_details)

        return action

    def add_detail(self, detail: ExtractionDetail):
        var = self.extraction_action.orderDetails.add()
        var.name = detail.name
        var.colName = detail.column_name

    def add_details(self, details: list):
        for detail in details:
            self.add_detail(detail)

    def build(self):
        return self.extraction_action


class OrderInfo:
    def __init__(self):
        self.order_info = order_book_pb2.OrderInfo()

    @staticmethod
    def create(action=None, actions: list = None, sub_order_details: OrdersDetails = None):
        order_info = OrderInfo()
        if action is not None:
            order_info.add_single_order_action(action)

        if actions is not None:
            order_info.add_order_actions(actions)

        if sub_order_details is not None:
            order_info.set_sub_orders_details(sub_order_details)

        return order_info

    def set_sub_orders_details(self, sub_order_details: OrdersDetails):
        self.order_info.subOrders.CopyFrom(sub_order_details.details())

    def set_number(self, number: int):
        self.order_info.number = number

    def add_order_actions(self, actions: list):
        for action in actions:
            self.add_single_order_action(action)

    def add_single_order_action(self, action):
        order_action = order_book_pb2.OrderAction()
        if isinstance(action, OrderAnalysisAction):
            order_analysis = order_book_pb2.OrderAnalysis()
            order_analysis.orderAnalysis.append(action.build())
            order_action.orderAnalysis.CopyFrom(order_analysis)
        elif isinstance(action, ExtractionAction):
            order_action.extractionAction.CopyFrom(action.build())
        else:
            raise Exception("Unsupported action type")
        self.order_info.orderActions.append(order_action)

    def build(self):
        return self.order_info
