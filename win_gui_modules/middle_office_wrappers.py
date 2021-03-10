from enum import Enum

from th2_grpc_act_gui_quod import middle_office_pb2, common_pb2
from th2_grpc_act_gui_quod.common_pb2 import EmptyRequest

from win_gui_modules.common_wrappers import CommissionsDetails
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


class ExtractionField(Enum):
    AGREED_PRICE = middle_office_pb2.ExtractionDetails.ExtractionField.AGREED_PRICE
    GROSS_AMOUNT = middle_office_pb2.ExtractionDetails.ExtractionField.GROSS_AMOUNT
    TOTAL_COMM = middle_office_pb2.ExtractionDetails.ExtractionField.TOTAL_COMM
    TOTAL_FEES = middle_office_pb2.ExtractionDetails.ExtractionField.TOTAL_FEES
    NET_AMOUNT = middle_office_pb2.ExtractionDetails.ExtractionField.NET_AMOUNT
    NET_PRICE = middle_office_pb2.ExtractionDetails.ExtractionField.NET_PRICE
    PSET_BIC = middle_office_pb2.ExtractionDetails.ExtractionField.PSET_BIC
    EXCHANGE_RATE = middle_office_pb2.ExtractionDetails.ExtractionField.EXCHANGE_RATE


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


class AllocationsDetails:
    def __init__(self, request: middle_office_pb2.AllocationsDetails):
        self.request = request

    def add_allocation_param(self, param: dict):
        params = self.request.AllocationsParams()
        params.fields.update(param)
        self.request.allocationsParams.append(params)

    def add_allocation_param_list(self, params_list: list):
        params = self.request.AllocationsParams()
        length = len(params_list)
        i = 0
        while i < length:
            params.fileds[params_list[i]] = params_list[i + 1]
            i += 2
        self.request.allocationsParams.append(params)


class OrderInfo:
    def __init__(self, request: middle_office_pb2.OrderBookAllocationsExtractionDetails.OrderInfo()):
        self.request = request

    def set_order_number(self, number: int):
        self.request.orderNumber = number

    def add_extraction_detail(self, detail: ExtractionDetail):
        var = self.request.extractionDetails.add()
        var.name = detail.name
        var.colName = detail.column_name

    def add_extraction_details(self, details: list):
        for detail in details:
            self.add_extraction_detail(detail)


class OrderBookAllocationsExtractionDetails:
    def __init__(self, request: middle_office_pb2.OrderBookAllocationsExtractionDetails()):
        self.request = request

    def set_extraction_id(self, extraction_id: str):
        self.request.extractionId = extraction_id

    def set_filter(self, filter_list: list):
        length = len(filter_list)
        i = 0
        while i < length:
            self.request.filter[filter_list[i]] = filter_list[i + 1]
            i += 2

    def extract_length(self, count_id: str):
        self.request.extractCount = True
        self.request.countId = count_id

    def add_order_info(self) -> OrderInfo:
        order_info = middle_office_pb2.OrderBookAllocationsExtractionDetails.OrderInfo()
        self.request.orders.append(order_info)
        return OrderInfo(order_info)


class ModifyTicketDetails:
    def __init__(self, base: EmptyRequest = None):
        if base is not None:
            self._request = middle_office_pb2.ModifyTicketDetails(base=base)
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

    def add_commissions_details(self) -> CommissionsDetails:
        self._request.commissionsDetails.CopyFrom(common_pb2.CommissionsDetails())
        return CommissionsDetails(self._request.commissionsDetails)

    def add_extraction_details(self):
        self._request.extractionDetails.CopyFrom(middle_office_pb2.ExtractionDetails())
        return ExtractionDetails(self._request.extractionDetails)

    def add_order_book_allocations_extraction_details(self) -> OrderBookAllocationsExtractionDetails:
        self._request.orderBookAllocationsExtractionDetails.CopyFrom(
            middle_office_pb2.OrderBookAllocationsExtractionDetails())
        return OrderBookAllocationsExtractionDetails(self._request.orderBookAllocationsExtractionDetails)

    def add_ticket_details(self) -> TicketDetails:
        self._request.ticketDetails.CopyFrom(middle_office_pb2.TicketDetails())
        return TicketDetails(self._request.ticketDetails)

    def add_settlement_details(self) -> SettlementDetails:
        self._request.settlementDetails.CopyFrom(middle_office_pb2.SettlementDetails())
        return SettlementDetails(self._request.settlementDetails)

    def add_allocations_details(self) -> AllocationsDetails:
        self._request.allocationsDetails.CopyFrom(middle_office_pb2.AllocationsDetails())
        return AllocationsDetails(self._request.allocationsDetails)

    def build(self):
        return self._request


class ExtractMiddleOfficeBlotterValuesRequest:
    def __init__(self, base: EmptyRequest = None):
        if base is not None:
            self._request = middle_office_pb2.ExtractMiddleOfficeBlotterValuesRequest(base=base)
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

    def add_extraction_detail(self, detail: ExtractionDetail):
        var = self._request.extractionDetails.add()
        var.name = detail.name
        var.colName = detail.column_name

    def add_extraction_details(self, details: list):
        for detail in details:
            self.add_extraction_detail(detail)

    def build(self):
        return self._request
