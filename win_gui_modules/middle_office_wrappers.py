from enum import Enum

from th2_grpc_act_gui_quod import middle_office_pb2, common_pb2
from th2_grpc_act_gui_quod.common_pb2 import EmptyRequest
from th2_grpc_act_gui_quod.trades_pb2 import ExtractTradesBookSubLvlDataDetails

from win_gui_modules.common_wrappers import CommissionsDetails, ContainedRow, TableCheckDetails
from win_gui_modules.order_book_wrappers import ExtractionDetail


class TicketDetails:
    def __init__(self, request: middle_office_pb2.TicketDetails()):
        self.request = request

    def set_client(self, client: str):
        self.request.client = client

    def set_trade_date(self, trade_date: str):
        self.request.tradeDate = trade_date

    def set_net_gross_ind(self, net_gross: str):
        self.request.netGrossInd = net_gross

    def set_give_up_broker(self, give_up_broker: str):
        self.request.giveUpBroker = give_up_broker

    def set_agreed_price(self, agreed_price: str):
        self.request.agreedPrice = agreed_price

    def set_net_price(self, net_price):
        self.request.net_price = net_price

    def build(self):
        return self.request

    def set_split_quantity(self, split_quantity: str):
        self.request.splitQuantity = split_quantity


class ExtractionField(Enum):
    AGREED_PRICE = middle_office_pb2.ExtractionDetails.ExtractionField.AGREED_PRICE
    GROSS_AMOUNT = middle_office_pb2.ExtractionDetails.ExtractionField.GROSS_AMOUNT
    TOTAL_COMM = middle_office_pb2.ExtractionDetails.ExtractionField.TOTAL_COMM
    TOTAL_FEES = middle_office_pb2.ExtractionDetails.ExtractionField.TOTAL_FEES
    NET_AMOUNT = middle_office_pb2.ExtractionDetails.ExtractionField.NET_AMOUNT
    NET_PRICE = middle_office_pb2.ExtractionDetails.ExtractionField.NET_PRICE
    PSET_BIC = middle_office_pb2.ExtractionDetails.ExtractionField.PSET_BIC
    EXCHANGE_RATE = middle_office_pb2.ExtractionDetails.ExtractionField.EXCHANGE_RATE
    SETTLEMENT_TYPE = middle_office_pb2.ExtractionDetails.ExtractionField.SETTLEMENT_TYPE
    BLOCK_SETTLEMENT_TYPE = middle_office_pb2.ExtractionDetails.ExtractionField.BLOCK_SETTLEMENT_TYPE
    IS_MANUAL_TOGGLED = middle_office_pb2.ExtractionDetails.ExtractionField.IS_MANUAL_TOGGLED
    FEES_TAB = middle_office_pb2.ExtractionDetails.ExtractionField.FEES_TAB
    COMMISSIONS_TAB = middle_office_pb2.ExtractionDetails.ExtractionField.COMMISSIONS_TAB


class ExtractionDetails:
    def __init__(self, request: middle_office_pb2.ExtractionDetails()):
        self.request = request

    def set_extraction_id(self, extraction_id: str):
        self.request.extractionId = extraction_id

    def extract_agreed_price(self, name: str):
        self.extract_value(ExtractionField.AGREED_PRICE, name)

    def extract_gross_amount(self, name: str):
        self.extract_value(ExtractionField.GROSS_AMOUNT, name)

    def extract_total_comm(self, name: str):
        self.extract_value(ExtractionField.TOTAL_COMM, name)

    def extract_total_fees(self, name: str):
        self.extract_value(ExtractionField.TOTAL_FEES, name)

    def extract_net_amount(self, name: str):
        self.extract_value(ExtractionField.NET_AMOUNT, name)

    def extract_net_price(self, name: str):
        self.extract_value(ExtractionField.NET_PRICE, name)

    def extract_pset_bic(self, name: str):
        self.extract_value(ExtractionField.PSET_BIC, name)

    def extract_exchange_rate(self, name: str):
        self.extract_value(ExtractionField.EXCHANGE_RATE, name)

    def extract_manual_checkbox_state(self, name: str):
        self.extract_value(ExtractionField.IS_MANUAL_TOGGLED, name)

    def extract_settlement_type(self, name: str):
        self.extract_value(ExtractionField.SETTLEMENT_TYPE, name)

    def extract_block_settlement_type(self, name: str):
        self.extract_value(ExtractionField.BLOCK_SETTLEMENT_TYPE, name)

    def extract_fees_row(self, name):
        self.extract_value(ExtractionField.FEES_TAB, name)

    def extract_commission_row(self, name):
        self.extract_value(ExtractionField.COMMISSIONS_TAB, name)

    def extract_value(self, field: ExtractionField, name: str):
        extracted_value = middle_office_pb2.ExtractionDetails.ExtractionParam()
        extracted_value.type = field.value
        extracted_value.name = name
        self.request.extractionParams.append(extracted_value)


class SettlementDetails:
    def __init__(self, request: middle_office_pb2.SettlementDetails()):
        self.request = request

    def set_settlement_type(self, settlement_type: str):
        self.request.settlementType = settlement_type

    def set_settlement_currency(self, settlement_currency: str):
        self.request.settlementCurrency = settlement_currency

    def set_exchange_rate(self, exchange_rate: str):
        self.request.exchangeRate = exchange_rate

    def set_exchange_rate_calc(self, exchange_rate_calc: str):
        self.request.exchangeRateCalc = exchange_rate_calc

    def set_settlement_amount(self, settlement_amount: str):
        self.request.settlementAmount = settlement_amount

    def toggle_settlement_date(self):
        self.request.toggleSettlementDate = True

    def set_settlement_date(self, settlement_date: str):
        self.request.settlementDate = settlement_date

    def set_pset(self, pset: str):
        self.request.pset = pset

    def set_pset_bic(self, pset_bic: str):
        pass

    def toggle_recompute(self):
        self.request.toggleRecompute = True

    def build(self):
        return self.request


class AllocationsDetails:
    def __init__(self, request: middle_office_pb2.AllocationsDetails):
        self.request = request

    def add_allocation_param(self, param: dict):
        params = self.request.AllocationsParams()
        params.fields.update(param)
        self.request.allocationsParams.append(params)

    def clear_greed(self):
        self.request.clearGreed = True

    def add_allocation_param_list(self, params_list: list):
        params = self.request.AllocationsParams()
        length = len(params_list)
        i = 0
        while i < length:
            params.fileds[params_list[i]] = params_list[i + 1]
            i += 2
        self.request.allocationsParams.append(params)


class OrderDetails:
    def __init__(self, request):
        self.request = request

    def set_order_number(self, number: int):
        self.request.orderNumber = number

    def clear_filter(self):
        self.request.clearAllocationFilter = True

    def add_extraction_detail(self, detail: ExtractionDetail):
        var = self.request.extractionDetails.add()
        var.name = detail.name
        var.colName = detail.column_name

    def add_extraction_details(self, details: list):
        for detail in details:
            self.add_extraction_detail(detail)

    def clear_filter_from_book(self):
        self.request.clearBlockFilter = True


class ViewOrderExtractionDetails:
    def __init__(self, base_request: EmptyRequest = None):
        if base_request is not None:
            self._request = middle_office_pb2.ViewOrderExtractionDetails(base=base_request)
        else:
            self._request = middle_office_pb2.ViewOrderExtractionDetails()

    def set_default_params(self, base_request):
        self._request.base.CopyFrom(base_request)

    def set_block_filter(self, block_filter: dict):
        self._request.blockFilter.update(block_filter)

    def set_view_orders_filter(self, view_orders_filter: dict):
        self._request.viewOrdersFilter.update(view_orders_filter)

    def add_order_details(self) -> OrderDetails:
        var = self._request.ordersDetails.add()
        return OrderDetails(var)

    def extract_length(self, count_id: str):
        self._request.extractCount = True
        self._request.countId = count_id

    def build(self):
        return self._request


class AmendAllocationsDetails:
    def __init__(self, request: middle_office_pb2.AmendAllocationsDetails()):
        self.request = request

    def set_filter(self, filter_dict: dict):
        self.request.filter.update(filter_dict)

    def set_row_number(self, row_number: int):
        self.request.rowNumber = row_number


class FeesDetails:
    def __init__(self, request: middle_office_pb2.FeesDetails()):
        self.request = request

    def remove_fees(self):
        self.request.removeFees = True

    def add_fees(self, feeType: str = None, basis: str = None, rate: str = None, amount: str = None,
                 currency: str = None, category: str = None):
        var = self.request.feesTabTableParams.add()
        if feeType is not None:
            var.feeType = feeType
        if basis is not None:
            var.basis = basis
        if rate is not None:
            var.rate = rate
        if amount is not None:
            var.amount = amount
        if currency is not None:
            var.currency = currency
        if category is not None:
            var.category = category

    def build(self):
        return self.request


class MiscDetails:
    def __init__(self, request: middle_office_pb2.MiscDetails()):
        self.request = request

    def set_trade_type(self, value: str):
        self.request.tradeType = value

    def set_bo_field_1(self, value: str):
        self.request.boField1 = value

    def set_bo_field_2(self, value: str):
        self.request.boField2 = value

    def set_bo_field_3(self, value: str):
        self.request.boField3 = value

    def set_bo_field_4(self, value: str):
        self.request.boField4 = value

    def set_bo_field_5(self, value: str):
        self.request.boField5 = value

    def set_bo_notes_value(self, value: str):
        self.request.backOfficeNotesValue = value

    def build(self):
        return self.request


class CheckContextAction:
    def __init__(self, request: common_pb2.CheckContextActionDetails()):
        self.request = request

    def set_extraction_key(self, extraction_key: str):
        self.request.extractionKey = extraction_key

    def set_action_name(self, action_name: str):
        self.request.actionName = action_name


class ModifyTicketDetails:
    def __init__(self, base_request: EmptyRequest = None):
        if base_request is not None:
            self._request = middle_office_pb2.ModifyTicketDetails(base=base_request)
        else:
            self._request = middle_office_pb2.ModifyTicketDetails()

    def set_default_params(self, base_request):
        self._request.base.CopyFrom(base_request)

    def set_filter(self, filter_list: list):
        length = len(filter_list)
        i = 0
        while i < length:
            self._request.filter[filter_list[i]] = filter_list[i + 1]
            i += 2

    def set_selected_row_count(self, selected_row_count: int):
        self._request.multipleRowSelection = True
        self._request.selectedRowCount = selected_row_count

    def set_partial_error_message(self, error_message: str):
        self._request.partialErrorMessage = error_message

    def add_commissions_details(self) -> CommissionsDetails:
        self._request.commissionsDetails.CopyFrom(common_pb2.CommissionsDetails())
        return CommissionsDetails(self._request.commissionsDetails)

    def add_extraction_details(self):
        self._request.extractionDetails.CopyFrom(middle_office_pb2.ExtractionDetails())
        return ExtractionDetails(self._request.extractionDetails)

    def add_ticket_details(self) -> TicketDetails:
        self._request.ticketDetails.CopyFrom(middle_office_pb2.TicketDetails())
        return TicketDetails(self._request.ticketDetails)

    def add_settlement_details(self) -> SettlementDetails:
        self._request.settlementDetails.CopyFrom(middle_office_pb2.SettlementDetails())
        return SettlementDetails(self._request.settlementDetails)

    def add_allocations_details(self) -> AllocationsDetails:
        self._request.allocationsDetails.CopyFrom(middle_office_pb2.AllocationsDetails())
        return AllocationsDetails(self._request.allocationsDetails)

    def add_amend_allocations_details(self) -> AmendAllocationsDetails:
        self._request.amendAllocationsDetails.CopyFrom(middle_office_pb2.AmendAllocationsDetails())
        return AmendAllocationsDetails(self._request.amendAllocationsDetails)

    def add_fees_details(self) -> FeesDetails:
        self._request.feesDetails.CopyFrom(middle_office_pb2.FeesDetails())
        return FeesDetails(self._request.feesDetails)

    def add_misc_details(self) -> MiscDetails:
        self._request.miscDetails.CopyFrom(middle_office_pb2.MiscDetails())
        return MiscDetails(self._request.miscDetails)

    def add_check_context_action(self) -> CheckContextAction:
        self._request.checkContextAction.CopyFrom(common_pb2.CheckContextActionDetails())
        return CheckContextAction(self._request.checkContextAction)

    def clear_filter(self):
        self._request.clearMiddleOfficeFilter = True

    def build(self):
        return self._request


class ExtractMiddleOfficeBlotterValuesRequest:
    def __init__(self, base_request: EmptyRequest = None):
        if base_request is not None:
            self._request = middle_office_pb2.ExtractMiddleOfficeBlotterValuesRequest(base=base_request)
        else:
            self._request = middle_office_pb2.ExtractMiddleOfficeBlotterValuesRequest()

    def set_default_params(self, base_request):
        self._request.base.CopyFrom(base_request)

    def set_filter(self, filter_list: list):
        length = len(filter_list)
        i = 0
        while i < length:
            self._request.filter[filter_list[i]] = filter_list[i + 1]
            i += 2

    def set_extraction_id(self, extraction_id: str):
        self._request.extractionId = extraction_id

    def set_row_number(self, row_number: int):
        self._request.rowNumber = row_number

    def add_extraction_detail(self, detail: ExtractionDetail):
        var = self._request.extractionDetails.add()
        var.name = detail.name
        var.colName = detail.column_name

    def add_extraction_details(self, details: list):
        for detail in details:
            self.add_extraction_detail(detail)

    def build(self):
        return self._request

    def clear_filter(self):
        self._request.clearMiddleOfficeFilter = True


class AllocationsExtractionDetails:
    def __init__(self, base_request: EmptyRequest = None):
        if base_request is not None:
            self._request = middle_office_pb2.AllocationsExtractionDetails(base=base_request)
        else:
            self._request = middle_office_pb2.AllocationsExtractionDetails()

    def set_default_params(self, base_request):
        self._request.base.CopyFrom(base_request)

    def set_block_filter(self, block_filter: dict):
        self._request.blockFilter.update(block_filter)

    def set_allocations_filter(self, allocations_filter: dict):
        self._request.allocationsFilter.update(allocations_filter)

    def add_order_details(self) -> OrderDetails:
        var = self._request.ordersDetails.add()
        return OrderDetails(var)

    def build(self):
        return self._request


class AllocationsTableCheckDetails:
    def __init__(self, base: EmptyRequest = None):
        self._request = middle_office_pb2.AllocationsTableCheckDetails()
        if base is not None:
            self.table_check_details = TableCheckDetails(base=base)
        else:
            self.table_check_details = TableCheckDetails()

    def set_default_params(self, base_request):
        self.table_check_details.set_default_params(base_request)

    def set_block_filter(self, filters: dict):
        self._request.blockFilter.update(filters)

    def set_allocations_filter(self, filters: dict):
        self.table_check_details.set_filter(filters)

    def add_contained_rows(self) -> ContainedRow:
        return self.table_check_details.add_contained_rows()

    def build(self):
        self._request.tableCheckDetails.CopyFrom(self.table_check_details.build())
        return self._request


class ExtractionPanelDetails:
    def __init__(self, base: EmptyRequest = None, filter: dict = None, panels: list = None, count_of_rows: int = None):
        if base is not None:
            self._request = middle_office_pb2.ExtractionPanelDetails(base=base)
        else:
            self._request = middle_office_pb2.ExtractionPanelDetails()

        if filter is not None:
            self._request.filter.update(filter)

        if panels is not None:
            for panel in panels:
                self._request.panels.append(panel)

        if count_of_rows:
            self._request.count_of_rows = count_of_rows

    def set_default_params(self, base_request):
        self._request.base.CopyFrom(base_request)

    def set_filter(self, filter: dict):
        self._request.filter.update(filter)

    def set_panels(self, panels: list):
        for panel in panels:
            self._request.panels.append(panel)

    def set_count_of_rows(self, count: int):
        self._request.count_of_rows = count

    def build(self):
        return self._request


class AllocationBlockExtractionDetails:
    def __init__(self, base: EmptyRequest = None, filter_middle_office_grid: dict = None,
                 filter_allocations_grid: dict = None,
                 panels: list = None, block_panels: list = None):
        if base is not None:
            self._request = middle_office_pb2.AllocationBlockExtractionDetails(base=base)
        else:
            self._request = middle_office_pb2.AllocationBlockExtractionDetails()

        if filter_middle_office_grid is not None:
            self._request.filterMiddleOfficeGrid.update(filter_middle_office_grid)

        if filter_allocations_grid is not None:
            self._request.filterAllocationsGrid.update(filter_allocations_grid)

        if panels is not None:
            for panel in panels:
                self._request.panels.append(panel)
        if block_panels is not None:
            self._request.panels.extend(block_panels)

    def set_default_params(self, base_request):
        self._request.base.CopyFrom(base_request)

    def set_filter_middle_office_grid(self, filter_middle_office: dict):
        if filter_middle_office is not None:
            self._request.filterMiddleOfficeGrid.update(filter_middle_office)

    def set_filter_allocations_grid(self, filter_allocations_grid: dict):
        if filter_allocations_grid is not None:
            self._request.filterAllocationsGrid.update(filter_allocations_grid)

    def set_panels(self, panels: list):
        if panels is not None:
            for panel in panels:
                self._request.panels.append(panel)

    def set_block_panels(self, panels: list):
        if panels is not None:
            for panel in panels:
                self._request.blockPanels.append(panel)

    def build(self):
        return self._request


class MassApproveDetails:
    def __init__(self, base_request: EmptyRequest = None, rows_numbers: list = None):
        if base_request is not None:
            self._request = middle_office_pb2.MassApproveDetails(base=base_request)
        else:
            self._request = middle_office_pb2.MassApproveDetails()

        if rows_numbers is not None:
            for number in rows_numbers:
                self._request.rowsNumbers.append(number)

    def set_default_params(self, base_request):
        self._request.base.CopyFrom(base_request)

    def set_rows_number(self, rows_numbers: list):
        for number in rows_numbers:
            self._request.rowsNumbers.append(number)

    def set_filter(self, filter_dict: dict):
        self._request.filter.update(filter_dict)

    def build(self):
        return self._request


class OpeningBookingTicket:
    def __init__(self, base_request: EmptyRequest):
        if base_request is not None:
            self.__opening_window = middle_office_pb2.OpenBookingTicket(base=base_request)
        else:
            self.__opening_window = middle_office_pb2.OpenBookingTicket()

    def set_filter(self, filter: dict):
        self.__opening_window.filter.update(filter)

    def set_selected_row(self, selected_rows: int):
        self.__opening_window.selected_rows = selected_rows

    def build(self):
        return self.__opening_window


class ExtractAllocationSubLvlDataDetails:
    def __init__(self, base_request: EmptyRequest):
        if base_request is not None:
            self.__extractAllocationSubLvlDataDetails = middle_office_pb2.ExtractAllocationSubLvlDataDetails(
                base=base_request)
        else:
            self.__extractAllocationSubLvlDataDetails = middle_office_pb2.ExtractAllocationSubLvlDataDetails()

    def set_default_params(self, base_request):
        self.__extractAllocationSubLvlDataDetails.base.CopyFrom(base_request)

    def set_block_filter(self, filter_block):
        self.__extractAllocationSubLvlDataDetails.blockFilter.update(filter_block)

    def set_allocation_filter(self, allocation_filter):
        self.__extractAllocationSubLvlDataDetails.allocationFilter.update(allocation_filter)

    def set_internal_extraction_details(self, extraction_details: ExtractTradesBookSubLvlDataDetails):
        self.__extractAllocationSubLvlDataDetails.extractionDetails.CopyFrom(extraction_details)

    def build(self):
        return self.__extractAllocationSubLvlDataDetails
