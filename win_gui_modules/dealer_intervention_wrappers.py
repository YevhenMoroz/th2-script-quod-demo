from enum import Enum

from th2_grpc_act_gui_quod import dealer_intervention_operations_pb2
from th2_grpc_act_gui_quod import common_pb2

from win_gui_modules.common_wrappers import SpreadAction
from win_gui_modules.order_book_wrappers import ExtractionDetail


class BaseTableDataRequest:
    def __init__(self, base: common_pb2.EmptyRequest = None):
        if base is not None:
            self.request = dealer_intervention_operations_pb2.BaseTableData(base=base)
        else:
            self.request = dealer_intervention_operations_pb2.BaseTableData()

    def set_default_params(self, base_request: common_pb2.EmptyRequest):
        self.request.base.CopyFrom(base_request)

    def set_filter_dict(self, filter_dict: dict):
        self.request.filter.update(filter_dict)

    def set_filter_list(self, filter_list: list):
        length = len(filter_list)
        i = 0
        while i < length:
            self.request.filter[filter_list[i]] = filter_list[i + 1]
            i += 2

    def set_row_number(self, row_number: int):
        self.request.rowNumber = row_number

    def build(self):
        return self.request


class ExtractionDetailsRequest:
    def __init__(self, data: BaseTableDataRequest = None):
        if data is not None:
            self.request = dealer_intervention_operations_pb2.ExtractionDetails(data=data.build())
        else:
            self.request = dealer_intervention_operations_pb2.ExtractionDetails()
        self.request.clearFilterBefore = False

    def set_clear_flag(self, flag: bool = True):
        self.request.clearFilterBefore = flag

    def set_data(self, data: BaseTableDataRequest):
        self.request.data.CopyFrom(data.build())

    def set_extraction_id(self, extraction_id: str):
        self.request.extractionId = extraction_id

    def add_extraction_details(self, extraction_details: list):
        for detail in extraction_details:
            self.add_extraction_detail(detail)

    def add_extraction_detail(self, detail: ExtractionDetail):
        var = self.request.extractionDetails.add()
        var.name = detail.name
        var.colName = detail.column_name

    def build(self):
        return self.request


class ModificationRequest:
    def __init__(self, base: common_pb2.EmptyRequest = None):
        if base is not None:
            self.request = dealer_intervention_operations_pb2.ModificationRequest(base=base)
        else:
            self.request = dealer_intervention_operations_pb2.ModificationRequest()

    def set_default_params(self, base_request: common_pb2.EmptyRequest):
        self.request.base.CopyFrom(base_request)

    def widen_spread(self):
        self._append_spread_action(SpreadAction.WIDEN_SPREAD)

    def narrow_spread(self):
        self._append_spread_action(SpreadAction.NARROW_SPREAD)

    def increase_ask(self):
        self._append_spread_action(SpreadAction.INCREASE_ASK)

    def decrease_ask(self):
        self._append_spread_action(SpreadAction.DECREASE_ASK)

    def increase_bid(self):
        self._append_spread_action(SpreadAction.INCREASE_BID)

    def decrease_bid(self):
        self._append_spread_action(SpreadAction.DECREASE_BID)

    def skew_towards_bid(self):
        self._append_spread_action(SpreadAction.SKEW_TOWARDS_BID)

    def skew_towards_ask(self):
        self._append_spread_action(SpreadAction.SKEW_TOWARDS_ASK)

    def _append_spread_action(self, action: SpreadAction):
        self.request.spreadActions.append(action.value)

    def set_quote_ttl(self, quote_ttl: str):
        self.request.quoteTTL = quote_ttl

    def send(self):
        self.request.action = dealer_intervention_operations_pb2.ModificationRequest.Action.SEND

    def reject(self):
        self.request.action = dealer_intervention_operations_pb2.ModificationRequest.Action.REJECT

    def build(self):
        return self.request


class RFQPanelValues(Enum):
    QUOTE_TTL = dealer_intervention_operations_pb2.RFQExtractionDetails.ExtractedType.QUOTE_TTL
    BID_PRICE_PIPS = dealer_intervention_operations_pb2.RFQExtractionDetails.ExtractedType.BID_PRICE_PIPS
    ASK_PRICE_PIPS = dealer_intervention_operations_pb2.RFQExtractionDetails.ExtractedType.ASK_PRICE_PIPS
    NEAR_LEG_QUANTITY = dealer_intervention_operations_pb2.RFQExtractionDetails.ExtractedType.NEAR_LEG_QUANTITY
    FAR_LEG_QUANTITY = dealer_intervention_operations_pb2.RFQExtractionDetails.ExtractedType.FAR_LEG_QUANTITY
    PRICE_SPREAD = dealer_intervention_operations_pb2.RFQExtractionDetails.ExtractedType.PRICE_SPREAD
    BID_PRICE_LARGE = dealer_intervention_operations_pb2.RFQExtractionDetails.ExtractedType.BID_PRICE_LARGE
    ASK_PRICE_LARGE = dealer_intervention_operations_pb2.RFQExtractionDetails.ExtractedType.ASK_PRICE_LARGE
    REQUEST_STATE = dealer_intervention_operations_pb2.RFQExtractionDetails.ExtractedType.REQUEST_STATE
    REQUEST_SIDE = dealer_intervention_operations_pb2.RFQExtractionDetails.ExtractedType.REQUEST_SIDE


class RFQExtractionDetailsRequest:
    def __init__(self, base: common_pb2.EmptyRequest = None):
        if base is not None:
            self.request = dealer_intervention_operations_pb2.RFQExtractionDetails(base=base)
        else:
            self.request = dealer_intervention_operations_pb2.RFQExtractionDetails()

    def set_default_params(self, base_request: common_pb2.EmptyRequest):
        self.request.base.CopyFrom(base_request)

    def set_extraction_id(self, extraction_id: str):
        self.request.extractionId = extraction_id

    def extract_quote_ttl(self, name: str):
        self.extract_value(RFQPanelValues.QUOTE_TTL, name)

    def extract_bid_price_pips(self, name: str):
        self.extract_value(RFQPanelValues.BID_PRICE_PIPS, name)

    def extract_ask_price_pips(self, name: str):
        self.extract_value(RFQPanelValues.ASK_PRICE_PIPS, name)

    def extract_near_leg_quantity(self, name: str):
        self.extract_value(RFQPanelValues.NEAR_LEG_QUANTITY, name)

    def extract_far_leg_quantity(self, name: str):
        self.extract_value(RFQPanelValues.FAR_LEG_QUANTITY, name)

    def extract_price_spread(self, name: str):
        self.extract_value(RFQPanelValues.PRICE_SPREAD, name)

    def extract_bid_price_large(self, name: str):
        self.extract_value(RFQPanelValues.BID_PRICE_LARGE, name)

    def extract_ask_price_large(self, name: str):
        self.extract_value(RFQPanelValues.ASK_PRICE_LARGE, name)

    def extract_request_state(self, name: str):
        self.extract_value(RFQPanelValues.REQUEST_STATE, name)

    def extract_request_side(self, name: str):
        self.extract_value(RFQPanelValues.REQUEST_SIDE, name)

    def extract_value(self, field: RFQPanelValues, name: str):
        extracted_value = dealer_intervention_operations_pb2.RFQExtractionDetails.ExtractedValue()
        extracted_value.type = field.value
        extracted_value.name = name
        self.request.extractedValues.append(extracted_value)

    def build(self):
        return self.request
