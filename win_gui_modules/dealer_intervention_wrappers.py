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
        self.request = dealer_intervention_operations_pb2.ModificationRequest(base=base)
        self.request.action = dealer_intervention_operations_pb2.ModificationRequest.Action.NONE
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

    def set_bid_large(self, bidLarge: str):
        self.request.bidLarge = bidLarge

    def set_bid_small(self, bidSmall: str):
        self.request.bidSmall = bidSmall

    def set_ask_large(self, askLarge: str):
        self.request.askLarge = askLarge

    def set_ask_small(self, askSmall: str):
        self.request.askSmall = askSmall

    def set_spread_step(self, spreadStep: str):
        self.request.spreadStep = spreadStep

    def click_is_hedged_chec_box(self, flag: bool = True):
        self.request.isHedged = flag

    def send(self):
        self.request.action = dealer_intervention_operations_pb2.ModificationRequest.Action.SEND

    def reject(self):
        self.request.action = dealer_intervention_operations_pb2.ModificationRequest.Action.REJECT

    def build(self):
        return self.request


class RFQPanelValues(Enum):
    short_path = dealer_intervention_operations_pb2.RFQExtractionDetails.ExtractedType
    QUOTE_TTL                            = short_path.QUOTE_TTL
    BID_PRICE_PIPS                       = short_path.BID_PRICE_PIPS
    ASK_PRICE_PIPS                       = short_path.ASK_PRICE_PIPS
    NEAR_LEG_QUANTITY                    = short_path.NEAR_LEG_QUANTITY
    FAR_LEG_QUANTITY                     = short_path.FAR_LEG_QUANTITY
    PRICE_SPREAD                         = short_path.PRICE_SPREAD
    BID_PRICE_LARGE                      = short_path.BID_PRICE_LARGE
    ASK_PRICE_LARGE                      = short_path.ASK_PRICE_LARGE
    REQUEST_STATE                        = short_path.REQUEST_STATE
    REQUEST_SIDE                         = short_path.REQUEST_SIDE
    BUTTON_TEXT                          = short_path.BUTTON_TEXT
    INSTRUMENT_LABEL_CONTROL             = short_path.INSTRUMENT_LABEL_CONTROL
    CURRENCY_VALUE_LABEL_CONTROL         = short_path.CURRENCY_VALUE_LABEL_CONTROL
    NEAR_TENOR_LABEL                     = short_path.NEAR_TENOR_LABEL
    FAR_TENOR_LABEL                      = short_path.FAR_TENOR_LABEL
    NEAR_SETTL_DATE_LABEL                = short_path.NEAR_SETTL_DATE_LABEL
    FAR_SETTL_DATE_LABEL                 = short_path.FAR_SETTL_DATE_LABEL
    PARTY_VALUE_LABEL_CONTROL            = short_path.PARTY_VALUE_LABEL_CONTROL
    REQUEST_SIDE_VALUE_LABEL_CONTROL     = short_path.REQUEST_SIDE_VALUE_LABEL_CONTROL
    FILL_SIDE_VALUE_LABEL_CONTROL        = short_path.FILL_SIDE_VALUE_LABEL_CONTROL
    CREATION_VALUE_LABEL_CONTROL         = short_path.CREATION_VALUE_LABEL_CONTROL
    BID_NEAR_POINTS_VALUE_LABEL          = short_path.BID_NEAR_POINTS_VALUE_LABEL
    BID_FAR_POINTS_VALUE_LABEL           = short_path.BID_FAR_POINTS_VALUE_LABEL
    BID_NEAR_PRICE_VALUE_LABEL           = short_path.BID_NEAR_PRICE_VALUE_LABEL
    BID_FAR_PRICE_VALUE_LABEL            = short_path.BID_FAR_PRICE_VALUE_LABEL
    BID_VALUE_LABEL                      = short_path.BID_VALUE_LABEL
    ASK_VALUE_LABEL                      = short_path.ASK_VALUE_LABEL
    ASK_NEAR_POINTS_VALUE_LABEL          = short_path.ASK_NEAR_POINTS_VALUE_LABEL
    ASK_FAR_POINTS_VALUE_LABEL           = short_path.ASK_FAR_POINTS_VALUE_LABEL
    ASK_NEAR_PRICE_VALUE_LABEL           = short_path.ASK_NEAR_PRICE_VALUE_LABEL
    ASK_FAR_PRICE_VALUE_LABEL            = short_path.ASK_FAR_PRICE_VALUE_LABEL
    OPPOSITE_NEAR_BID_QTY_VALUE_LABEL    = short_path.OPPOSITE_NEAR_BID_QTY_VALUE_LABEL
    OPPOSITE_NEAR_ASK_QTY_VALUE_LABEL    = short_path.OPPOSITE_NEAR_ASK_QTY_VALUE_LABEL
    OPPOSITE_FAR_BID_QTY_VALUE_LABEL     = short_path.OPPOSITE_FAR_BID_QTY_VALUE_LABEL
    OPPOSITE_FAR_ASK_QTY_VALUE_LABEL     = short_path.OPPOSITE_FAR_ASK_QTY_VALUE_LABEL
    IS_BID_PRICE_PIPS_ENABLED            = short_path.IS_BID_PRICE_PIPS_ENABLED
    IS_ASK_PRICE_PIPS_ENABLED            = short_path.IS_ASK_PRICE_PIPS_ENABLED
    IS_NEAR_LEG_QUANTITY_ENABLED         = short_path.IS_NEAR_LEG_QUANTITY_ENABLED
    IS_FAR_LEG_QUANTITY_ENABLED          = short_path.IS_FAR_LEG_QUANTITY_ENABLED
    IS_PRICE_SPREAD_ENABLED              = short_path.IS_PRICE_SPREAD_ENABLED
    IS_BID_PRICE_LARGE_ENABLED           = short_path.IS_BID_PRICE_LARGE_ENABLED
    IS_ASK_PRICE_LARGE_ENABLED           = short_path.IS_ASK_PRICE_LARGE_ENABLED

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

    def extract_button_text(self, name: str):
        self.extract_value(RFQPanelValues.BUTTON_TEXT, name)
    def extract_instrument_label_control(self, name: str):    self.extract_value(RFQPanelValues.INSTRUMENT_LABEL_CONTROL, name)
    def extract_currency_value_label_control(self, name: str):    self.extract_value(RFQPanelValues.CURRENCY_VALUE_LABEL_CONTROL, name)
    def extract_near_tenor_label(self, name: str):    self.extract_value(RFQPanelValues.NEAR_TENOR_LABEL, name)
    def extract_far_tenor_label(self, name: str):    self.extract_value(RFQPanelValues.FAR_TENOR_LABEL, name)
    def extract_near_settl_date_label(self, name: str):    self.extract_value(RFQPanelValues.NEAR_SETTL_DATE_LABEL, name)
    def extract_far_settl_date_label(self, name: str):    self.extract_value(RFQPanelValues.FAR_SETTL_DATE_LABEL, name)
    def extract_party_value_label_control(self, name: str):    self.extract_value(RFQPanelValues.PARTY_VALUE_LABEL_CONTROL, name)
    def extract_request_side_value_label_control(self, name: str):    self.extract_value(RFQPanelValues.REQUEST_SIDE_VALUE_LABEL_CONTROL, name)
    def extract_fill_side_value_label_control(self, name: str):    self.extract_value(RFQPanelValues.FILL_SIDE_VALUE_LABEL_CONTROL, name)
    def extract_creation_value_label_control(self, name: str):    self.extract_value(RFQPanelValues.CREATION_VALUE_LABEL_CONTROL, name)
    def extract_bid_near_points_value_label(self, name: str):    self.extract_value(RFQPanelValues.BID_NEAR_POINTS_VALUE_LABEL, name)
    def extract_bid_far_points_value_label(self, name: str):    self.extract_value(RFQPanelValues.BID_FAR_POINTS_VALUE_LABEL, name)
    def extract_bid_near_price_value_label(self, name: str):    self.extract_value(RFQPanelValues.BID_NEAR_PRICE_VALUE_LABEL, name)
    def extract_bid_far_price_value_label(self, name: str):    self.extract_value(RFQPanelValues.BID_FAR_PRICE_VALUE_LABEL, name)
    def extract_bid_value_label(self, name: str):    self.extract_value(RFQPanelValues.BID_VALUE_LABEL, name)
    def extract_ask_value_label(self, name: str):    self.extract_value(RFQPanelValues.ASK_VALUE_LABEL, name)
    def extract_ask_near_points_value_label(self, name: str):    self.extract_value(RFQPanelValues.ASK_NEAR_POINTS_VALUE_LABEL, name)
    def extract_ask_far_points_value_label(self, name: str):    self.extract_value(RFQPanelValues.ASK_FAR_POINTS_VALUE_LABEL, name)
    def extract_ask_near_price_value_label(self, name: str):    self.extract_value(RFQPanelValues.ASK_NEAR_PRICE_VALUE_LABEL, name)
    def extract_ask_far_price_value_label(self, name: str):    self.extract_value(RFQPanelValues.ASK_FAR_PRICE_VALUE_LABEL, name)
    def extract_opposite_near_bid_qty_value_label(self, name: str):    self.extract_value(RFQPanelValues.OPPOSITE_NEAR_BID_QTY_VALUE_LABEL, name)
    def extract_opposite_near_ask_qty_value_label(self, name: str):    self.extract_value(RFQPanelValues.OPPOSITE_NEAR_ASK_QTY_VALUE_LABEL, name)
    def extract_opposite_far_bid_qty_value_label(self, name: str):    self.extract_value(RFQPanelValues.OPPOSITE_FAR_BID_QTY_VALUE_LABEL, name)
    def extract_opposite_far_ask_qty_value_label(self, name: str):    self.extract_value(RFQPanelValues.OPPOSITE_FAR_ASK_QTY_VALUE_LABEL, name)
    def extract_is_bid_price_pips_enabled(self, name: str):    self.extract_value(RFQPanelValues.IS_BID_PRICE_PIPS_ENABLED, name)
    def extract_is_ask_price_pips_enabled(self, name: str):    self.extract_value(RFQPanelValues.IS_ASK_PRICE_PIPS_ENABLED, name)
    def extract_is_near_leg_quantity_enabled(self, name: str):    self.extract_value(RFQPanelValues.IS_NEAR_LEG_QUANTITY_ENABLED, name)
    def extract_is_far_leg_quantity_enabled(self, name: str):    self.extract_value(RFQPanelValues.IS_FAR_LEG_QUANTITY_ENABLED, name)
    def extract_is_price_spread_enabled(self, name: str):    self.extract_value(RFQPanelValues.IS_PRICE_SPREAD_ENABLED, name)
    def extract_is_bid_price_large_enabled(self, name: str):    self.extract_value(RFQPanelValues.IS_BID_PRICE_LARGE_ENABLED, name)
    def extract_is_ask_price_large_enabled(self, name: str):    self.extract_value(RFQPanelValues.IS_ASK_PRICE_LARGE_ENABLED, name)

    def extract_value(self, field: RFQPanelValues, name: str):
        extracted_value = dealer_intervention_operations_pb2.RFQExtractionDetails.ExtractedValue()
        extracted_value.type = field.value
        extracted_value.name = name
        self.request.extractedValues.append(extracted_value)

    def build(self):
        return self.request
