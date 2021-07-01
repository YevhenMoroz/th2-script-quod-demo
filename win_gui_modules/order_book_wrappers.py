from th2_grpc_act_gui_quod.common_pb2 import EmptyRequest

from .order_ticket import OrderTicketDetails, FXOrderDetails
from th2_grpc_act_gui_quod import order_book_pb2, order_book_fx_pb2
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

    def set_selected_row_count(self, selected_row_count: int):
        self.modify_order_details.multipleRowSelection = True
        self.modify_order_details.selectedRowCount = selected_row_count

    def build(self):
        return self.modify_order_details


class ModifyFXOrderDetails:
    def __init__(self, base_request):
        self.modify_order_details = order_book_fx_pb2.ModifyFXOrderDetails()

        self.modify_order_details.base.CopyFrom(base_request)

    def set_order_details(self, order_details: FXOrderDetails):
        self.modify_order_details.orderDetails.CopyFrom(order_details.build())

    def set_filter(self, filter_list: list):
        length = len(filter_list)
        i = 0
        while i < length:
            self.modify_order_details.filter[filter_list[i]] = filter_list[i + 1]
            i += 2

    def set_selected_row_count(self, selected_row_count: int):
        self.modify_order_details.multipleRowSelection = True
        self.modify_order_details.selectedRowCount = selected_row_count

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

    def set_selected_row_count(self, selected_row_count: int):
        self.cancel_order_details.multipleRowSelection = True
        self.cancel_order_details.selectedRowCount = selected_row_count

    def build(self):
        return self.cancel_order_details


class CancelFXOrderDetails:
    def __init__(self, base_request):
        self.cancel_order_details = order_book_fx_pb2.CancelFXOrderDetails()
        self.cancel_order_details.base.CopyFrom(base_request)

    def set_filter(self, filter_list: list):
        length = len(filter_list)
        i = 0
        while i < length:
            self.cancel_order_details.filter[filter_list[i]] = filter_list[i + 1]
            i += 2

    def set_comment(self, comment: str):
        self.cancel_order_details.comment = comment

    def set_cancel_children(self, cancel_children: bool = False):
        self.cancel_order_details.cancelChildren.value = cancel_children

    def set_selected_row_count(self, selected_row_count: int):
        self.cancel_order_details.multipleRowSelection = True
        self.cancel_order_details.selectedRowCount = selected_row_count

    def build(self):
        return self.cancel_order_details


class ReleaseFXOrderDetails:
    def __init__(self, base_request):
        self.release_order_details = order_book_fx_pb2.ModifyFXOrderDetails()
        self.release_order_details.base.CopyFrom(base_request)

    def set_filter(self, filter_list: list):
        length = len(filter_list)
        i = 0
        while i < length:
            self.release_order_details.filter[filter_list[i]] = filter_list[i + 1]
            i += 2

    def set_selected_row_count(self, selected_row_count: int):
        self.release_order_details.multipleRowSelection = True
        self.release_order_details.selectedRowCount = selected_row_count

    def set_order_details(self, order_details: FXOrderDetails):
        self.release_order_details.orderDetails.CopyFrom(order_details.build())

    def build(self):
        return self.release_order_details


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


class CalcDataContentsRowSelector:
    def __init__(self):
        self.row_selector = order_book_pb2.CalcDataContentsRowSelector()

    def set_column_name(self, column_name: str):
        self.row_selector.columnName = column_name

    def minimize(self):
        self.row_selector.compareType = order_book_pb2.CalcDataContentsRowSelector.CompareType.MINIMIZE

    def maximize(self):
        self.row_selector.compareType = order_book_pb2.CalcDataContentsRowSelector.CompareType.MAXIMIZE

    def build(self):
        return self.row_selector


class VerifyGeneratedOrderEvent:
    def __init__(self):
        self.verify_action = order_book_pb2.VerifyGeneratedOrderEvent()

    def set_venue(self, venue: str):
        self.verify_action.venue = venue

    def set_row_selector(self, row_selector: CalcDataContentsRowSelector):
        self.verify_action.rowSelector.CopyFrom(row_selector.build())

    def set_event_number(self, event_number: int):
        self.verify_action.eventRowNumber.value = event_number

    def build(self):
        return self.verify_action


class ExtractCalcDataContents:
    def __init__(self):
        self.extract_action = order_book_pb2.ExtractCalcDataContents()

    def set_row_selector(self, row_selector: CalcDataContentsRowSelector):
        self.extract_action.rowSelector.CopyFrom(row_selector.build())

    def set_event_number(self, event_number: int):
        self.extract_action.eventRowNumber.value = event_number

    def add_detail(self, detail: ExtractionDetail):
        var = self.extract_action.details.add()
        var.name = detail.name
        var.colName = detail.column_name

    def add_details(self, details: list):
        for detail in details:
            self.add_detail(detail)

    def build(self):
        return self.extract_action


class ExtractEventRows:
    def __init__(self):
        self.extract_action = order_book_pb2.ExtractEventRows()

    def set_event_number(self, event_number: int):
        self.extract_action.eventRowNumber.value = event_number

    def build(self):
        return self.extract_action


class OrderAnalysisAction:
    def __init__(self):
        self.order_analysis_action = order_book_pb2.OrderAnalysisAction()

    @staticmethod
    def create_verify_generate_order_event(event_number: int = None, venue: str = None,
                                           row_selector: CalcDataContentsRowSelector = None):
        verify_action = VerifyGeneratedOrderEvent()
        if event_number is not None:
            verify_action.set_event_number(event_number)
        if venue is not None:
            verify_action.set_venue(venue)
        if row_selector is not None:
            verify_action.set_row_selector(row_selector)

        result = OrderAnalysisAction()
        result.add_action(verify_action)

        return result

    @staticmethod
    def create_extract_calc_data_contents(event_number: int, row_selector: CalcDataContentsRowSelector,
                                          detail: ExtractionDetail = None, details: list = None):
        extract_action = ExtractCalcDataContents()
        extract_action.set_event_number(event_number)
        extract_action.set_row_selector(row_selector)
        if detail is not None:
            extract_action.add_detail(detail)
        if details is not None:
            extract_action.add_details(details)

        result = OrderAnalysisAction()
        result.add_action(extract_action)

        return result

    @staticmethod
    def create_extract_event_rows(event_number: int = None):
        extract_action = ExtractEventRows()
        if event_number is not None:
            extract_action.set_event_number(event_number)

        result = OrderAnalysisAction()
        result.add_action(extract_action)

        return result

    def add_action(self, action):
        if isinstance(action, VerifyGeneratedOrderEvent):
            self.order_analysis_action.verifyGeneratedOrderEvent.CopyFrom(action.build())
        elif isinstance(action, ExtractCalcDataContents):
            self.order_analysis_action.extractCalcDataContents.CopyFrom(action.build())
        elif isinstance(action, ExtractEventRows):
            self.order_analysis_action.extractEventRows.CopyFrom(action.build())

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
            order_analysis.orderAnalysisAction.append(action.build())
            order_action.orderAnalysis.CopyFrom(order_analysis)
        elif isinstance(action, ExtractionAction):
            order_action.extractionAction.CopyFrom(action.build())
        else:
            raise Exception("Unsupported action type")
        self.order_info.orderActions.append(order_action)

    def build(self):
        return self.order_info


class ExecutionsDetails:
    def __init__(self, request: order_book_pb2.ManualExecutionDetails.ExecutionDetails):
        self.request = request

    def set_quantity(self, quantity: str):
        self.request.quantity = quantity

    def set_price(self, price: str):
        self.request.price = price

    def set_executing_firm(self, executing_firm: str):
        self.request.executingFirm = executing_firm

    def set_contra_firm(self, contra_firm: str):
        self.request.contraFirm = contra_firm

    def set_last_capacity(self, last_capacity: str):
        self.request.lastCapacity = last_capacity

    def set_settlement_date_offset(self, offset: int):
        self.request.settlementDateOffset = offset


class ManualExecutingDetails:
    def __init__(self, base: EmptyRequest = None):
        if base is not None:
            self._request = order_book_pb2.ManualExecutionDetails(base=base)
        else:
            self._request = order_book_pb2.ManualExecutionDetails()

    def set_default_params(self, base_request):
        self._request.base.CopyFrom(base_request)

    def set_filter(self, table_filter: dict):
        self._request.filter.update(table_filter)

    def set_row_number(self, row_number: int):
        self._request.rowNumber = row_number

    def add_executions_details(self) -> ExecutionsDetails:
        var = self._request.executionDetails.add()
        return ExecutionsDetails(var)

    def build(self):
        return self._request


class CompleteOrdersDetails:
    def __init__(self, base: EmptyRequest = None):
        if base is not None:
            self._request = order_book_pb2.CompleteOrdersDetails(base=base)
        else:
            self._request = order_book_pb2.CompleteOrdersDetails()

    def set_default_params(self, base_request):
        self._request.base.CopyFrom(base_request)

    def set_filter(self, table_filter: dict):
        self._request.filter.update(table_filter)

    def set_selected_row_count(self, selected_row_count: int):
        self._request.multipleRowSelection = True
        self._request.selectedRowCount = selected_row_count

    def build(self):
        return self._request

# Use for ReOrder Action and ReOrder Leaves Action
class BaseOrdersDetails:
    def __init__(self, base: EmptyRequest = None):
        if base is not None:
            self._request = order_book_pb2.BaseOrdersDetails(base=base)
        else:
            self._request = order_book_pb2.BaseOrdersDetails()

    def set_default_params(self, base_request):
        self._request.base.CopyFrom(base_request)

    def set_filter(self, table_filter: dict):
        self._request.filter.update(table_filter)

    def build(self):
        return self._request


class ManualCrossDetails:
    def __init__(self, base: EmptyRequest = None):
        if base is not None:
            self._request = order_book_pb2.ManualCrossDetails(base=base)
        else:
            self._request = order_book_pb2.ManualCrossDetails()

    def set_default_params(self, base_request):
        self._request.base.CopyFrom(base_request)

    def set_filter(self, table_filter: dict):
        self._request.filter.update(table_filter)

    def set_price(self, value: str):
        self._request.price = value

    def set_quantity(self, value: str):
        self._request.quantity = value

    def set_capacity(self, value: str):
        self._request.capacity = value

    def set_last_mkt(self, value: str):
        self._request.lastMkt = value

    def set_selected_rows(self, row_numbers: list):
        for row in row_numbers:
            self._request.selectedRows.append(row)

    def build(self):
        return self._request
