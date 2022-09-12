from dataclasses import dataclass

from th2_grpc_act_gui_quod import basket_book_pb2, middle_office_pb2, common_pb2
from th2_grpc_act_gui_quod import care_orders_pb2
from th2_grpc_act_gui_quod import order_book_pb2, order_book_fx_pb2
from th2_grpc_act_gui_quod.care_orders_pb2 import TransferPoolDetails
from th2_grpc_act_gui_quod.common_pb2 import EmptyRequest

from win_gui_modules.basket_ticket_wrappers import RowDetails
from win_gui_modules.common_wrappers import CommissionsDetails
from win_gui_modules.order_ticket import OrderTicketDetails, FXOrderDetails


class ModifyOrderDetails:
    def __init__(self, base_request=None):
        self.modify_order_details = order_book_pb2.ModifyOrderDetails()
        if base_request is not None:
            self.modify_order_details.base.CopyFrom(base_request)

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


class CancelOrderDetails:
    def __init__(self, base_request):
        self.cancel_order_details = order_book_pb2.CancelOrderDetails()
        if base_request is not None:
            self.cancel_order_details.base.CopyFrom(base_request)

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


class ForceCancelOrderDetails:
    def __init__(self, base_request):
        self.cancel_order_details = order_book_pb2.ForceCancelOrderDetails()
        if base_request is not None:
            self.cancel_order_details.base.CopyFrom(base_request)

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

    def set_transfer_order_user(self, desk: str, partial_desk: bool = False):
        self.transfer_order_details.desk = desk
        self.transfer_order_details.partialDesk = partial_desk

    def build(self):
        return self.transfer_order_details


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
        self.clear_filter = False

    @staticmethod
    def create(order_info_list: list = None, info=None):
        order_details = OrdersDetails()

        if order_info_list is not None:
            for i in order_info_list:
                order_details.add_single_order_info(i)

        if info is not None:
            order_details.add_single_order_info(info)

        return order_details

    def clear_filter(self):
        self.clear_filter = True

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
        request.clearOrderBookFilter = self.clear_filter
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

    def __init__(self, base_request: EmptyRequest = None):
        if base_request is not None:
            self._request = order_book_pb2.SuspendOrderDetails(base=base_request)
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
    def create(action=None, actions: list = None, sub_order_details: OrdersDetails = None, row_number=None):
        order_info = OrderInfo()
        if action is not None:
            order_info.add_single_order_action(action)

        if actions is not None:
            order_info.add_order_actions(actions)

        if sub_order_details is not None:
            order_info.set_sub_orders_details(sub_order_details)
        if row_number is not None:
            order_info.set_number(row_number)
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
    def __init__(self, base_request: EmptyRequest = None):
        if base_request is not None:
            self._request = order_book_pb2.MassExecSummaryAveragePriceDetails(base=base_request)
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

    def set_source_account(self, source_account: str):
        self.request.sourceAccount = source_account


class OtherTabDetails:
    def __init__(self, request: order_book_pb2.ManualExecutionDetails.OtherTabDetails):
        self._request = request

    def set_trade_type(self, trade_type: str):
        self._request.tradeType = trade_type

    def set_net_gross_ind(self, net_gross_ind: str):
        self._request.netGrossInd = net_gross_ind

    def set_sec_last_mkt(self, sec_last_mkt: str):
        self._request.secLastMkt = sec_last_mkt

    def set_settlement_type(self, set_settlement_type: str):
        self._request.settlementType = set_settlement_type

    def set_settl_currency(self, settl_currency: str):
        self._request.settlCurrency = settl_currency

    def set_exchange_rate(self, exchange_rate: str):
        self._request.exchangeRate = exchange_rate

    def set_exchange_rate_cacl(self, exchange_rate_cacl):
        self._request.exchangeRateCacl = exchange_rate_cacl

    def set_agent_fees(self, agent_fees: str):
        self._request.agentFees = agent_fees

    def set_market_fees(self, market_fees: str):
        self._request.marketFees = market_fees

    def set_route_fees(self, route_fees: str):
        self._request.routeFees = route_fees


class MenuItemDetails:
    def __init__(self, base_request: EmptyRequest = None):
        if base_request is not None:
            self._request = order_book_pb2.MenuItemDetails(base=base_request)
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
    def __init__(self, base_request: EmptyRequest = None):
        if base_request is not None:
            self._request = order_book_pb2.ManualExecutionDetails(base=base_request)
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

    def add_other_details(self) -> OtherTabDetails:
        var = self._request.othertabDetails.add()
        return OtherTabDetails(var)

    def set_error_expected(self, error_expected: bool):
        self._request.errorExpected = error_expected

    def build(self):
        return self._request


class CompleteOrdersDetails:
    def __init__(self, base_request: EmptyRequest = None):
        if base_request is not None:
            self._request = order_book_pb2.CompleteOrdersDetails(base=base_request)
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
    def __init__(self, base_request: EmptyRequest = None):
        if base_request is not None:
            self._request = order_book_pb2.BaseOrdersDetails(base=base_request)
        else:
            self._request = order_book_pb2.BaseOrdersDetails()

    def set_default_params(self, base_request):
        self._request.base.CopyFrom(base_request)

    def set_filter(self, filter_list: list):
        length = len(filter_list)
        i = 0
        while i < length:
            self._request.filter[filter_list[i]] = filter_list[i + 1]
            i += 2

    def build(self):
        return self._request


class ManualCrossDetails:
    def __init__(self, base_request: EmptyRequest = None):
        if base_request is not None:
            self._request = order_book_pb2.ManualCrossDetails(base=base_request)
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

    def set_extract_footer(self):
        self._request.manualCrossValues.CopyFrom(ExtractManualCrossValuesRequest("ErrorMessage").build())

    def build(self):
        return self._request


class ExtractManualCrossValuesRequest:
    def __init__(self, extraction_id: str = None, manual_cross_extracted_value: list = None):
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

    def set_error_expected(self, error_expected: bool):
        self._request.errorExpected = error_expected

    def set_basket_name(self, basket_name: str):
        self._request.basketName = basket_name

    def build(self):
        return self._request


class CreateBasketDetails:
    def __init__(self, base_request=None, row_numbers: list = None, name: str = None, row_details: list = None):
        self._request = order_book_pb2.CreateBasketDetails()
        if base_request is not None:
            self._request.base.CopyFrom(base_request)
        if name is not None:
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

    def set_rows_for_delete(self, delete_rows: int):
        i = 0
        while i < delete_rows:
            self._request.rowsDetails.append(RowDetails(delete_row=True).build())
            i += 1

    def build(self):
        return self._request


class CancelChildOrdersDetails:
    def __init__(self, base: EmptyRequest = None):
        if base is not None:
            self._request = order_book_pb2.CancelChildOrdersDetails(base=base)
        else:
            self._request = order_book_pb2.CancelOrderDetails()

    def set_default_params(self, base_request):
        self._request.base.CopyFrom(base_request)

    def set_filter(self, filter: dict):
        self._request.filter.update(filter)

    def build(self):
        return self._request


class SecondLevelExtractionDetails:
    def __init__(self, base_request=None, filter: dict = None, tabs_details: list = None):
        if base_request is not None:
            self.request = order_book_pb2.SecondLevelExtractionDetails(base=base_request)
        else:
            self.request = order_book_pb2.SecondLevelExtractionDetails()

        if filter is not None:
            self.request.filter.update(filter)

        if tabs_details is not None:
            for details in tabs_details:
                self.request.tabsDetails.append(details)

    def set_default_params(self, base_request):
        self.request.base.CopyFrom(base_request)

    def set_filter(self, filter: dict):
        self.request.filter.update(filter)

    def set_tabs_details(self, tabs_details: list):
        for detail in tabs_details:
            self.request.tabsDetails.append(detail)

    def build(self):
        return self.request


class SecondLevelTabDetails:
    def __init__(self, tab_name: str = None, columns_names: list = None, rows_numbers: list = None):
        self.request = order_book_pb2.SecondLevelTabDetails()

        if tab_name is not None:
            self.request.tabName = tab_name

        if columns_names is not None:
            for name in columns_names:
                self.request.columnsNames.append(name)

        if rows_numbers is not None:
            for number in rows_numbers:
                self.request.rowsNumbers.append(number)

    def set_tab_name(self, tab_name: str):
        self.request.tabName = tab_name

    def set_columns_names(self, columns_names: list):
        for name in columns_names:
            self.request.columnsNames.append(name)

    def set_rows_numbers(self, rows_numbers: list):
        for number in rows_numbers:
            self.request.rowsNumbers.append(number)

    def build(self):
        return self.request


class ExtractOrderDataDetails:
    def __init__(self):
        self._request = basket_book_pb2.ExtractOrderDataDetails()

    def set_default_params(self, base_request):
        self._request.base.CopyFrom(base_request)

    def set_filter(self, filter: dict):
        self._request.filter.update(filter)

    def set_column_names(self, column_names: list):
        for name in column_names:
            self._request.columnNames.append(name)

    def build(self):
        return self._request


class ExtractChildOrderDataDetails:
    def __init__(self, extract_order_data: ExtractOrderDataDetails = None, rows_number: int = None):
        self._request = basket_book_pb2.ExtractChildOrderDataDetails()
        self._request.extractDetails.CopyFrom(extract_order_data)
        self._request.rowsNumber = rows_number

    def set_extract_order_data(self, extract_order_data: ExtractOrderDataDetails):
        self._request.extractDetails.CopyFrom(extract_order_data)

    def set_rows_number(self, rows_number: int):
        self._request.rowsNumber = rows_number

    def build(self):
        return self._request


class SplitBookingParameter:
    def __init__(self, ticket_details: middle_office_pb2.TicketDetails = None,
                 settlement_details: middle_office_pb2.SettlementDetails = None,
                 commissions_details: common_pb2.CommissionsDetails = None,
                 fees_details: middle_office_pb2.FeesDetails = None,
                 misc_details: middle_office_pb2.MiscDetails = None):
        self._request = order_book_pb2.SplitBookingParameter()

        if ticket_details is not None:
            self._request.ticketDetails.CopyFrom(ticket_details)

        if settlement_details is not None:
            self._request.settlementDetails.CopyFrom(settlement_details)

        if commissions_details is not None:
            self._request.commissionsDetails.CopyFrom(commissions_details)

        if fees_details is not None:
            self._request.feesDetails.CopyFrom(fees_details)

        if misc_details is not None:
            self._request.miscDetails.CopyFrom(misc_details)

    def set_ticket_details(self, ticket_details):
        self._request.ticketDetails.CopyFrom(ticket_details)

    def set_settlement_details(self, settlement_details):
        self._request.settlementDetails.CopyFrom(settlement_details)

    def set_commissions_details(self, commissions_details: CommissionsDetails):
        self._request.commissionsDetails.CopyFrom(commissions_details)

    def set_fees_details(self, fees_details):
        self._request.feesDetails.CopyFrom(fees_details)

    def set_misc_details(self, misc_details):
        self._request.miscDetails.CopyFrom(misc_details)

    def build(self):
        return self._request


class SplitBookingDetails:
    def __init__(self, base: EmptyRequest = None, rows_numbers: list = None, split_booking_params: list = None):
        if base is not None:
            self._request = order_book_pb2.SplitBookingDetails(base=base)
        else:
            self._request = order_book_pb2.SplitBookingDetails()

        if rows_numbers is not None:
            for number in rows_numbers:
                self._request.rowsNumbers.append(number)

        if split_booking_params is not None:
            for param in split_booking_params:
                self._request.splitBookingParams.append(param)

    def set_default_params(self, base_request):
        self._request.base.CopyFrom(base_request)

    def set_rows_numbers(self, rows_numbers: list):
        for number in rows_numbers:
            self._request.rowsNumbers.append(number)

    def set_split_booking_parameter(self, split_booking_params: list):
        for param in split_booking_params:
            self._request.splitBookingParams.append(param)

    def set_error_expected(self, error_expected: bool):
        self._request.errorExpected = error_expected

    def build(self):
        return self._request


class MassManualExecutionDetails:
    def __init__(self, base_request: EmptyRequest = None, count_of_selected_rows: int = None, price: str = None):
        if base_request is not None:
            self._request = order_book_pb2.MassManualExecutionDetails(base=base_request)
        else:
            self._request = order_book_pb2.MassManualExecutionDetails()

        if price is not None:
            self._request.price = price

        if count_of_selected_rows is not None:
            self._request.countOfSelectedRows = count_of_selected_rows

    def set_default_params(self, base_request):
        self._request.base.CopyFrom(base_request)

    def set_price(self, price: str):
        self._request.price = price

    def set_count_of_selected_rows(self, rows: int):
        self._request.countOfSelectedRows = rows

    def build(self):
        return self._request


class UnmatchAndTransferDetails:
    def __init__(self, base_request):
        self.transfer_details = order_book_pb2.UnmatchAndTransferDetails()
        self.transfer_details.base.CopyFrom(base_request)

    def set_filter_and_sub_filter(self, filter_dict: dict, sub_filter_dict: dict = None):
        self.transfer_details.filter.update(filter_dict)
        if sub_filter_dict:
            self.transfer_details.subFilter.update(sub_filter_dict)

    def set_account_destination(self, account_destination: str):
        self.transfer_details.account = account_destination

    def build(self):
        return self.transfer_details


class SubLvlInfo:
    def __init__(self):
        self._request = order_book_pb2.SubLvlInfo()

    def set_filter(self, filter_dict: dict = None):
        if filter_dict is not None:
            self._request.filter.update(filter_dict)

    def set_tab_name(self, tab_name):
        self._request.tabName = tab_name

    def build(self):
        return self._request


class GetSubLvlDetails:
    def __init__(self, base_request: EmptyRequest = None):
        if base_request is not None:
            self._request = order_book_pb2.GetSubLvlDetails(base=base_request)
        else:
            self._request = order_book_pb2.GetSubLvlDetails()

    def set_base_request(self, base_request=None):
        if base_request is not None:
            self._request.base.CopyFrom(base_request)

    def set_filter(self, filter_dict: dict = None):
        if filter_dict is not None:
            self._request.filter.update(filter_dict)

    def set_column_names(self, column_names: list):
        self._request.columnNames.extend(column_names)

    def set_sub_lvl_info(self, sub_lvl_info: list):
        self._request.subLvlInfo.append(sub_lvl_info)

    def build(self):
        return self._request


class QuickButtonCreationDetails:
    def __init__(self, base_request: EmptyRequest = None):
        if base_request is not None:
            self._request = order_book_pb2.SplitShortcutCreationButtonDetails(base=base_request)
        else:
            self._request = order_book_pb2.SplitShortcutCreationButtonDetails()

    def set_btn_name(self, btn_name: str):
        self._request.btnName = btn_name

    def set_custom_name(self, custom_name: str):
        self._request.customName = custom_name

    def set_qty(self, qty: str):
        self._request.qty = qty

    def set_qty_type(self, qty_type: str):
        self._request.qtyType = qty_type

    def set_action_type(self, action_type: str):
        self._request.actionType = action_type

    def set_tif(self, tif: str):
        self._request.tif = tif

    def set_routes(self, routes: str):
        self._request.routes = routes

    def set_strategy(self, strategy: str):
        self._request.strategy = strategy

    def set_strategy_type(self, strategy_type: str):
        self._request.strategyType = strategy_type

    def set_child_strategy(self, child_strategy: str):
        self._request.childStrategy = child_strategy

    def set_order_type(self, order_type: str):
        self._request.orderType = order_type

    def set_recipient(self, recipient: str):
        self._request.recipient = recipient

    def set_order_id(self, order_id: str):
        self._request.ordBookFilter["Order ID"] = order_id

    def build(self):
        return self._request


class ActionsHotKeysDetails:
    def __init__(self, base_request: EmptyRequest = None):
        if base_request is not None:
            self.request = order_book_pb2.ActionWithOrdersViaHotKeysDetails(base=base_request)
        else:
            self.request = order_book_pb2.ActionWithOrdersViaHotKeysDetails()

    def set_default_params(self, base_request):
        self.request.base.CopyFrom(base_request)

    def set_row_number(self, rows_numbers: list):
        for row in rows_numbers:
            self.request.rowNumbers.append(row)

    def set_filter(self, filter_dict: dict):
        self.request.filter.update(filter_dict)

    def set_cancel_hotkey(self):
        self.request.hotkeys.append(order_book_pb2.ActionWithOrdersViaHotKeysDetails.HotKeys.DEL)

    def set_enter_hotkey(self):
        self.request.hotkeys.append(order_book_pb2.ActionWithOrdersViaHotKeysDetails.HotKeys.ENTER)

    def build(self):
        return self.request
