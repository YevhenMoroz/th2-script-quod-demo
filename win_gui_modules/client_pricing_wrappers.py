from enum import Enum

from th2_grpc_act_gui_quod import cp_operations_pb2

from win_gui_modules.common_wrappers import BaseTileDetails, SpreadAction
from win_gui_modules.order_book_wrappers import ExtractionDetail


class ModifyRatesTileRequest:
    def __init__(self, details: BaseTileDetails = None):
        if details is not None:
            self.modify_request = cp_operations_pb2.ModifyRatesTileRequest(data=details.build())
        else:
            self.modify_request = cp_operations_pb2.ModifyRatesTileRequest()

    def set_details(self, details: BaseTileDetails):
        self.modify_request.data.CopyFrom(details.build())

    def set_instrument(self, instrument: str):
        self.modify_request.instrument = instrument

    def set_client_tier(self, client_tier: str):
        self.modify_request.clientTier = client_tier

    def toggle_live(self):
        self.modify_request.toggleLive = True

    def toggle_automated(self):
        self.modify_request.toggleAutomated = True

    def press_use_defaults(self):
        self.modify_request.pressUseDefaults = True

    def press_executable(self):
        self.modify_request.pressExecutable = True

    def press_pricing(self):
        self.modify_request.pressPricing = True

    def set_pips(self, pips: str):
        self.modify_request.pips = pips

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
        self.modify_request.spreadActions.append(action.value)

    def build(self):
        return self.modify_request


class PlaceRatesTileOrderRequest:
    def __init__(self, details: BaseTileDetails = None):
        if details is not None:
            self.place_order_request = cp_operations_pb2.PlaceRatesTileOrderRequest(data=details.build())
        else:
            self.place_order_request = cp_operations_pb2.PlaceRatesTileOrderRequest()

    def set_details(self, details: BaseTileDetails):
        self.place_order_request.data.CopyFrom(details.build())

# SWAP buy and sell side
    def buy(self):
        self.place_order_request.side = cp_operations_pb2.PlaceRatesTileOrderRequest.Side.SELL

    def sell(self):
        self.place_order_request.side = cp_operations_pb2.PlaceRatesTileOrderRequest.Side.BUY

    def set_quantity(self, quantity: str):
        self.place_order_request.quantity = quantity

    def set_order_type(self, order_type: str):
        self.place_order_request.orderType = order_type

    def set_time_in_force(self, time_in_force: str):
        self.place_order_request.timeInForce = time_in_force

    def set_slippage(self, slippage: str):
        self.place_order_request.slippage = slippage

    def set_stop_price(self, stop_price: str):
        self.place_order_request.stopPrice = stop_price

    def set_order_price_large_value(self, order_price_large_value: str):
        self.place_order_request.orderPriceLargeValue = order_price_large_value

    def set_order_price_pips(self, order_price_pips: str):
        self.place_order_request.orderPricePips = order_price_pips

    def set_client(self, client: str):
        self.place_order_request.client = client

    def build(self):
        return self.place_order_request


class RatesTileValues(Enum):
    VALUE_DATE = cp_operations_pb2.ExtractRatesTileValuesRequest.ExtractedType.VALUE_DATE
    BID_LARGE_VALUE = cp_operations_pb2.ExtractRatesTileValuesRequest.ExtractedType.BID_LARGE_VALUE
    ASK_QUANTITY = cp_operations_pb2.ExtractRatesTileValuesRequest.ExtractedType.ASK_QUANTITY
    BID_QUANTITY = cp_operations_pb2.ExtractRatesTileValuesRequest.ExtractedType.BID_QUANTITY
    SPREAD = cp_operations_pb2.ExtractRatesTileValuesRequest.ExtractedType.SPREAD
    ASK_LARGE_VALUE = cp_operations_pb2.ExtractRatesTileValuesRequest.ExtractedType.ASK_LARGE_VALUE
    PIPS = cp_operations_pb2.ExtractRatesTileValuesRequest.ExtractedType.PIPS
    ASK_PIPS = cp_operations_pb2.ExtractRatesTileValuesRequest.ExtractedType.ASK_PIPS
    BID_PIPS = cp_operations_pb2.ExtractRatesTileValuesRequest.ExtractedType.BID_PIPS


class ExtractRatesTileValues:
    def __init__(self, details: BaseTileDetails = None):
        if details is not None:
            self.request = cp_operations_pb2.ExtractRatesTileValuesRequest(data=details.build())
        else:
            self.request = cp_operations_pb2.ExtractRatesTileValuesRequest()

    def set_details(self, details: BaseTileDetails):
        self.request.data.CopyFrom(details.build())

    def set_extraction_id(self, extraction_id: str):
        self.request.extractionId = extraction_id

    def extract_value_date(self, name: str):
        self.extract_value(RatesTileValues.VALUE_DATE, name)

    def extract_bid_large_value(self, name: str):
        self.extract_value(RatesTileValues.BID_LARGE_VALUE, name)

    def extract_ask_quantity(self, name: str):
        self.extract_value(RatesTileValues.ASK_QUANTITY, name)

    def extract_bid_quantity(self, name: str):
        self.extract_value(RatesTileValues.BID_QUANTITY, name)

    def extract_spread(self, name: str):
        self.extract_value(RatesTileValues.SPREAD, name)

    def extract_ask_large_value(self, name: str):
        self.extract_value(RatesTileValues.ASK_LARGE_VALUE, name)

    def extract_pips(self, name: str):
        self.extract_value(RatesTileValues.PIPS, name)

    def extract_ask_pips(self, name: str):
        self.extract_value(RatesTileValues.ASK_PIPS, name)

    def extract_bid_pips(self, name: str):
        self.extract_value(RatesTileValues.BID_PIPS, name)

    def extract_value(self, field: RatesTileValues, name: str):
        extracted_value = cp_operations_pb2.ExtractRatesTileValuesRequest.ExtractedValue()
        extracted_value.type = field.value
        extracted_value.name = name
        self.request.extractedValues.append(extracted_value)

    def build(self):
        return self.request


class ExtractRatesTileTableValuesRequest:
    def __init__(self, details: BaseTileDetails = None):
        if details is not None:
            self.request = cp_operations_pb2.ExtractRatesTileTableValuesRequest(data=details.build())
        else:
            self.request = cp_operations_pb2.ExtractRatesTileTableValuesRequest()

    def set_details(self, details: BaseTileDetails):
        self.request.data.CopyFrom(details.build())

    def set_extraction_id(self, extraction_id: str):
        self.request.extractionId = extraction_id

    def set_row_number(self, row_number: int):
        self.request.rowNumber = row_number

    def set_bid_extraction_fields(self, extractions_fields: list):
        for extraction_field in extractions_fields:
            self.set_bid_extraction_field(extraction_field)

    def set_ask_extraction_fields(self, extractions_fields: list):
        for extraction_field in extractions_fields:
            self.set_ask_extraction_field(extraction_field)

    def set_bid_extraction_field(self, detail: ExtractionDetail):
        var = self.request.bidExtractionFields.add()
        var.name = detail.name
        var.colName = detail.column_name

    def set_ask_extraction_field(self, detail: ExtractionDetail):
        var = self.request.askExtractionFields.add()
        var.name = detail.name
        var.colName = detail.column_name

    def build(self):
        return self.request
