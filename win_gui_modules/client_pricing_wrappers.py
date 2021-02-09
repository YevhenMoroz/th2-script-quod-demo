from th2_grpc_act_gui_quod import cp_operations_pb2
from th2_grpc_act_gui_quod.common_pb2 import EmptyRequest

from win_gui_modules.order_book_wrappers import ExtractionDetail


class RatesTileDetails:
    def __init__(self, base: EmptyRequest = None, window_index: int = None):
        if base is not None and window_index is not None:
            self.base_details = cp_operations_pb2.RatesTileDetails(base=base, windowIndex=window_index)
        elif base is not None:
            self.base_details = cp_operations_pb2.RatesTileDetails(base=base)
        elif window_index is not None:
            self.base_details = cp_operations_pb2.RatesTileDetails(windowIndex=window_index)
        else:
            self.base_details = cp_operations_pb2.RatesTileDetails()

    def set_window_index(self, index: int):
        self.base_details.windowIndex = index

    def set_default_params(self, base_request):
        self.base_details.base.CopyFrom(base_request)

    def build(self):
        return self.base_details


class ModifyRatesTileRequest:
    def __init__(self, details: RatesTileDetails = None):
        if details is not None:
            self.modify_request = cp_operations_pb2.ModifyRatesTileRequest(details=details.build())
        else:
            self.modify_request = cp_operations_pb2.ModifyRatesTileRequest()

    def set_details(self, details: RatesTileDetails):
        self.modify_request.details.CopyFrom(details.build())

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
        self.modify_request.spreadActions.append(cp_operations_pb2.ModifyRatesTileRequest.SpreadAction.WIDEN_SPREAD)

    def narrow_spread(self):
        self.modify_request.spreadActions.append(cp_operations_pb2.ModifyRatesTileRequest.SpreadAction.NARROW_SPREAD)

    def increase_ask(self):
        self.modify_request.spreadActions.append(cp_operations_pb2.ModifyRatesTileRequest.SpreadAction.INCREASE_ASK)

    def decrease_ask(self):
        self.modify_request.spreadActions.append(cp_operations_pb2.ModifyRatesTileRequest.SpreadAction.DECREASE_ASK)

    def increase_bid(self):
        self.modify_request.spreadActions.append(cp_operations_pb2.ModifyRatesTileRequest.SpreadAction.INCREASE_BID)

    def decrease_bid(self):
        self.modify_request.spreadActions.append(cp_operations_pb2.ModifyRatesTileRequest.SpreadAction.DECREASE_BID)

    def skew_towards_bid(self):
        self.modify_request.spreadActions.append(cp_operations_pb2.ModifyRatesTileRequest.SpreadAction.SKEW_TOWARDS_BID)

    def skew_towards_ask(self):
        self.modify_request.spreadActions.append(cp_operations_pb2.ModifyRatesTileRequest.SpreadAction.SKEW_TOWARDS_ASK)

    def build(self):
        return self.modify_request


class PlaceRatesTileOrderRequest:
    def __init__(self, details: RatesTileDetails = None):
        if details is not None:
            self.place_order_request = cp_operations_pb2.PlaceRatesTileOrderRequest(details=details.build())
        else:
            self.place_order_request = cp_operations_pb2.PlaceRatesTileOrderRequest()

    def set_details(self, details: RatesTileDetails):
        self.place_order_request.details.CopyFrom(details.build())

    def buy(self):
        self.place_order_request.side = cp_operations_pb2.PlaceRatesTileOrderRequest.Side.BUY

    def sell(self):
        self.place_order_request.side = cp_operations_pb2.PlaceRatesTileOrderRequest.Side.SELL

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


class ExtractRatesTileValuesRequest:
    def __init__(self, details: RatesTileDetails = None):
        if details is not None:
            self.request = cp_operations_pb2.ExtractRatesTileValuesRequest(details=details.build())
        else:
            self.request = cp_operations_pb2.ExtractRatesTileValuesRequest()

    def set_details(self, details: RatesTileDetails):
        self.request.details.CopyFrom(details.build())

    def set_extraction_id(self, extraction_id: str):
        self.request.extractionId = extraction_id

    def extract_value_date(self):
        self.request.valueDate = True

    def extract_bid_large_value(self):
        self.request.bidLargeValue = True

    def extract_bid_quantity(self):
        self.request.topOfBookCumBidQuantity = True

    def extract_ask_quantity(self):
        self.request.topOfBookCumAskQuantity = True

    def extract_spread(self):
        self.request.topOfBookSpread = True

    def extract_ask_large_value(self):
        self.request.askLargeValue = True

    def extract_pips(self):
        self.request.pips = True

    def build(self):
        return self.request


class ExtractRatesTileTableValuesRequest:
    def __init__(self, details: RatesTileDetails = None):
        if details is not None:
            self.request = cp_operations_pb2.ExtractRatesTileTableValuesRequest(details=details.build())
        else:
            self.request = cp_operations_pb2.ExtractRatesTileTableValuesRequest()

    def set_details(self, details: RatesTileDetails):
        self.request.details.CopyFrom(details.build())

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
