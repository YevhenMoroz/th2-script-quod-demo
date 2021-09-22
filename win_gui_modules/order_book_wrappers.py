from th2_grpc_act_gui_quod.care_orders_pb2 import TransferPoolDetails
from th2_grpc_act_gui_quod.common_pb2 import EmptyRequest
from th2_grpc_act_gui_quod.order_book_pb2 import ExtractManualCrossValuesRequest

from .order_ticket import OrderTicketDetails, FXOrderDetails
from th2_grpc_act_gui_quod import order_book_pb2, order_book_fx_pb2, ar_operations_pb2, care_orders_pb2
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

    def amend_by_icon(self):
        self.modify_order_details.amendByIcon = True

    def build(self):
        return self.modify_order_details


class MassExecSummaryDetails:
    def __init__(self, base: EmptyRequest = None, count_of_selected_rows: int = None, reported_price_value: str = None):
        if base is not None:
            self._request = order_book_pb2.MassExecSummaryDetails(base=base)
        else:
            self._request = order_book_pb2.MassExecSummaryDetails()

        if count_of_selected_rows is not None:
            self._request.countOfSelectedRows = count_of_selected_rows

        if reported_price_value is not None:
            self._request.reportedPrice = reported_price_value

    def set_default_params(self, base_request):
        self._request.base.CopyFrom(base_request)

    def set_count_of_selected_rows(self, count: int):
        self._request.countOfSelectedRows = count

    def set_reported_price_value(self, reported_price: str):
        self._request.reportedPrice = reported_price

    def build(self):
        return self._request


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

    def amend_by_icon(self):
        self.modify_order_details.amendByIcon = True

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

    def cancel_by_icon(self):
        self.cancel_order_details.cancelByIcon = True

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


class TransferOrderDetails:
    def __init__(self):
        self.transfer_order_details = order_book_pb2.TransferOrderDetails()

    def set_filter(self, filter_list: list):
        length = len(filter_list)
        i = 0
        while i < length:
            self.transfer_order_details.filter[filter_list[i]] = filter_list[i + 1]
            i += 2

    def set_default_params(self, base_request):
        self.transfer_order_details.base.CopyFrom(base_request)

    def set_selected_row_count(self, selected_row_count: int):
        self.transfer_order_details.multipleRowSelection = True
        self.transfer_order_details.selectedRowCount = selected_row_count

    def build(self):
        return self.transfer_order_details

    def set_transfer_order_user(self, desk: str, partial_desk: bool = False):
        self.transfer_order_details.desk = desk
        self.transfer_order_details.partialDesk = partial_desk


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


class SuspendOrderDetails:

    def __init__(self, base: EmptyRequest = None):
        if base is not None:
            self._request = order_book_pb2.SuspendOrderDetails(base=base)
        else:
            self._request = order_book_pb2.SuspendOrderDetails()

    def set_filter(self, table_filter: dict):
        self._request.filter.update(table_filter)

    def set_cancel_children(self, cancel_children: bool):
        self._request.cancelChildren = cancel_children

    def build(self):
        return self._request


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


class MassExecSummaryAveragePriceDetails:
    def __init__(self, base: EmptyRequest = None):
        if base is not None:
            self._request = order_book_pb2.MassExecSummaryAveragePriceDetails(base=base)
        else:
            self._request = order_book_pb2.MassExecSummaryAveragePriceDetails()

    def set_default_params(self, base_request):
        self._request.base.CopyFrom(base_request)

    def set_count_of_selected_rows(self, count: int):
        self._request.countOfSelectedRows = count

    def build(self):
        return self._request


class DiscloseFlagDetails:
    def __init__(self, base_request=None, row_numbers: list = None):
        self._request = order_book_pb2.DiscloseFlagDetails()
        self._request.base.CopyFrom(base_request)

        if row_numbers is not None:
            for number in row_numbers:
                self._request.rowNumbers.append(number)

    def set_default_params(self, base_request):
        self._request.base.CopyFrom(base_request)

    def set_row_numbers(self, row_numbers: list):
        for number in row_numbers:
            self._request.rowNumbers.append(number)

    def manual(self):
        self._request.flagOption = order_book_pb2.DiscloseFlagDetails.FlagOption.MANUAL

    def real_time(self):
        self._request.flagOption = order_book_pb2.DiscloseFlagDetails.FlagOption.REAL_TIME

    def disable(self):
        self._request.flagOption = order_book_pb2.DiscloseFlagDetails.FlagOption.DISABLE

    def build(self):
        return self._request


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


class MenuItemDetails:
    def __init__(self, base: EmptyRequest = None):
        if base is not None:
            self._request = order_book_pb2.MenuItemDetails(base=base)
        else:
            self._request = order_book_pb2.MenuItemDetails()

    def set_filter(self, table_filter: dict):
        self._request.filter.update(table_filter)

    def set_menu_item(self, menu_item: str):
        self._request.menuItem = menu_item

    def set_selected_rows(self, selected_rows):
        self._request.selectedRows.extend(selected_rows)

    def set_extraction_Id(self, extraction_Id: str):
        self._request.extractionId = extraction_Id

    def build(self):
        return self._request


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

    def set_row_number(self, row_number: (int)):
        self._request.rowNumber = row_number

    def add_executions_details(self) -> ExecutionsDetails:
        var = self._request.executionDetails.add()
        return ExecutionsDetails(var)

    def set_error_expected(self, error_expected: bool):
        self._request.errorExpected = error_expected

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
        # self.manualCrossValues = order_book_pb2.ExtractManualCrossValuesRequest()

    def set_default_params(self, base_request):
        self._request.base.CopyFrom(base_request)

    def set_extract_manual_cross_value(self, manual_cross_value):
        self._request.manualCrossValues.CopyFrom(manual_cross_value)

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


class ExtractManualCrossValuesRequest:
    def __init__(self, extraction_id: int = None, manual_cross_extracted_value: list = None):
        self._request = order_book_pb2.ExtractManualCrossValuesRequest()
        if extraction_id is not None:
            self._request.extractionId = extraction_id
        if manual_cross_extracted_value is not None:
            for value in manual_cross_extracted_value:
                self._request.extractedValues.append(value)

    def set_extraction_id(self, extraction_id: int):
        self._request.extractionId = extraction_id

    def set_manual_cross_extracted_value(self, manual_cross_extracted_value: list):
        for value in manual_cross_extracted_value:
            self._request.extractedValues.append(value)

    def build(self):
        return self._request


class ManualCrossExtractedValue:
    def __init__(self, type=None, name: str = None):
        self._request = order_book_pb2.ExtractManualCrossValuesRequest.ManualCrossExtractedValue()
        self._request.type = type
        self._request.name = name

    def set_type(self, type):
        self._request.type = type

    def set_name(self, name: str):
        self._request.name = name

    def build(self):
        return self._request


class FXOrdersDetails:
    def __init__(self):
        self.base_params = None
        self.extraction_id = None
        self.orders_details = order_book_fx_pb2.FXOrdersDetailsInfo()

    @staticmethod
    def create(order_info_list: list = None, info=None):
        order_details = FXOrdersDetails()

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
        request = order_book_fx_pb2.GetFXOrdersDetailsRequest()
        request.base.CopyFrom(self.base_params)
        request.extractionId = self.extraction_id
        request.orderDetails.CopyFrom(self.orders_details)
        return request

    def details(self):
        return self.orders_details


class FXOrderInfo:
    def __init__(self):
        self.order_info = order_book_fx_pb2.FXOrderInfo()

    @staticmethod
    def create(action=None, actions: list = None, sub_order_details: FXOrdersDetails = None):
        order_info = FXOrderInfo()
        if action is not None:
            order_info.add_single_order_action(action)

        if actions is not None:
            order_info.add_order_actions(actions)

        if sub_order_details is not None:
            order_info.set_sub_orders_details(sub_order_details)

        return order_info

    def set_sub_orders_details(self, sub_order_details: FXOrdersDetails):
        self.order_info.subOrders.CopyFrom(sub_order_details.details())

    def set_number(self, number: int):
        self.order_info.number = number

    def add_order_actions(self, actions: list):
        for action in actions:
            self.add_single_order_action(action)

    def add_single_order_action(self, action):
        order_action = order_book_fx_pb2.FXOrderAction()
        if isinstance(action, ExtractionAction):
            order_action.extractionAction.CopyFrom(action.build())
        else:
            raise Exception("Unsupported action type")
        self.order_info.orderActions.append(order_action)

    def build(self):
        return self.order_info


class SuspendOrderDetails:

    def __init__(self, base: EmptyRequest = None):
        if base is not None:
            self._request = order_book_pb2.SuspendOrderDetails(base=base)
        else:
            self._request = order_book_pb2.SuspendOrderDetails()

    def set_filter(self, table_filter: dict):
        self._request.filter.update(table_filter)

    def set_cancel_children(self, cancel_children: bool):
        self._request.cancelChildren = cancel_children

    def build(self):
        return self._request


class AddToBasketDetails:
    def __init__(self, base: EmptyRequest = None, row_numbers: list = None, basket_name: str = None):
        if base is not None:
            self._request = order_book_pb2.AddToBasketDetails(base=base)
        else:
            self._request = order_book_pb2.CancelOrderDetails()

        if row_numbers is not None:
            for numbers in row_numbers:
                self._request.rowNumbers.append(numbers)

        if basket_name is not None:
            self._request.basketName = basket_name

    def set_default_params(self, base_request):
        self._request.base.CopyFrom(base_request)

    def set_row_numbers(self, row_numbers: list):
        for number in row_numbers:
            self._request.rowNumbers.append(number)

    def set_basket_name(self, basket_name: str):
        self._request.basketName = basket_name

    def build(self):
        return self._request


class CreateBasketDetails:
    def __init__(self, base_request=None, row_numbers: list = None, name: str = None, row_details: list = None):
        self._request = order_book_pb2.CreateBasketDetails()
        self._request.base.CopyFrom(base_request)
        self._request.name = name

        if row_numbers is not None:
            for number in row_numbers:
                self._request.rowNumbers.append(number)

        if row_details is not None:
            for detail in row_details:
                self._request.rowsDetails.append(detail)

    def set_default_params(self, base_request):
        self._request.base.CopyFrom(base_request)

    def set_row_numbers(self, row_numbers: list):
        for number in row_numbers:
            self._request.rowNumbers.append(number)

    def set_name(self, name: str):
        self._request.name = name

    def set_row_details(self, row_details: list):
        for detail in row_details:
            self._request.rowsDetails.append(detail)

    def build(self):
        return self._request

# class QuoteRequestDetails:
#     def __init__(self):
#         self.base = None
#         self.extractionId = None
#         self.quote_request_details = ar_operations_pb2.QuoteRequestDetailsInfo()
#
#     @staticmethod
#     def create(order_info_list: list = None, info=None):
#         order_details = QuoteRequestDetails()
#
#         if order_info_list is not None:
#             for i in order_info_list:
#                 order_details.add_single_order_info(i)
#
#         if info is not None:
#             order_details.add_single_order_info(info)
#
#         return order_details
#
#     def set_extraction_id(self, extraction_id: str):
#         self.extractionId = extraction_id
#
#     def set_filter(self, filter_list: list):
#         length = len(filter_list)
#         i = 0
#         while i < length:
#             self.quote_request_details.filter[filter_list[i]] = filter_list[i + 1]
#             i += 2
#
#     def set_order_info(self, order_info_list: list):
#         for quoteRequestInfo in order_info_list:
#             self.quote_request_details.quoteRequestInfo.append(quoteRequestInfo.build())
#
#     def add_single_order_info(self, quoteRequestInfo):
#         self.quote_request_details.quoteRequestInfo.append(quoteRequestInfo.build())
#
#     def set_default_params(self, base_request):
#         self.base = base_request
#
#     def extract_length(self, count_id: str):
#         self.quote_request_details.extractCount = True
#         self.quote_request_details.countId = count_id
#
#     def request(self):
#         request = ar_operations_pb2.QuoteRequestDetailsRequest()
#         request.base.CopyFrom(self.base)
#         request.extractionId = self.extractionId
#         request.orderDetails.CopyFrom(self.quote_request_details)
#         return request
#
#     def details(self):
#         return self.quote_request_details


# class QuoteRequestInfo:
#     def __init__(self):
#         self.order_info = ar_operations_pb2.QuoteRequestInfo()
#
#     @staticmethod
#     def create(action=None, actions: list = None, sub_order_details: QuoteRequestDetails = None):
#         quote_request_info = QuoteRequestInfo()
#         if action is not None:
#             quote_request_info.add_single_order_action(action)
#
#         if actions is not None:
#             quote_request_info.add_order_actions(actions)
#
#         if sub_order_details is not None:
#             quote_request_info.set_sub_orders_details(sub_order_details)
#
#         return quote_request_info
#
#     def set_sub_orders_details(self, sub_order_details: QuoteRequestDetails):
#         self.order_info.subOrders.CopyFrom(sub_order_details.details())
#
#     def set_number(self, number: int):
#         self.order_info.number = number
#
#     def add_order_actions(self, actions: list):
#         for action in actions:
#             self.add_single_order_action(action)
#
#     def add_single_order_action(self, action):
#         quote_request_action = ar_operations_pb2.QuoteRequestAction()
#         if isinstance(action, ContextActionsQuoteBook):
#             quote_request_action.contextActionsQuoteBook = action.value
#         else:
#             raise Exception("Unsupported action type")
#         self.order_info.quoteRequestActions.append(quote_request_action)
#
#     def build(self):
#         return self.order_info
# #
#
# class ContextActionsQuoteBook(Enum):
#     reject = ar_operations_pb2.QuoteRequestAction.ContextActionsQuoteBook.REJECT
#     unassign = ar_operations_pb2.QuoteRequestAction.ContextActionsQuoteBook.UNASSIGN
