from th2_grpc_act_gui_quod import rfq_operations_pb2
from th2_grpc_act_gui_quod.common_pb2 import EmptyRequest
from datetime import date, datetime
from google.protobuf.timestamp_pb2 import Timestamp
from google.protobuf.wrappers_pb2 import Int64Value
from enum import Enum


class RFQTileDetails:

    def __init__(self, base: EmptyRequest = None):
        if base is not None:
            self.__request_details = rfq_operations_pb2.RFQTileDetails(base=base)
        else:
            self.__request_details = rfq_operations_pb2.RFQTileDetails()

    def set_from_currency(self, currency: str):
        self.__request_details.fromCurrency = currency

    def set_to_currency(self, currency: str):
        self.__request_details.toCurrency = currency

    def set_near_tenor(self, tenor: str):
        self.__request_details.nearTenor = tenor

    def set_window_index(self, index: int):
        self.__request_details.windowIndex = index

    def set_change_currency(self, change_currency: bool):
        self.__request_details.changeCurrency = change_currency

    def set_settlement_date(self, settlement_date: date):
        self.__request_details.settlementDate.FromDatetime(datetime.fromordinal(settlement_date.toordinal()))

    def set_client(self, client: str):
        self.__request_details.client = client

    def set_quantity(self, quantity: int):
        self.__request_details.quantity.value = quantity

    def request(self) -> rfq_operations_pb2.RFQTileDetails:
        return self.__request_details


class RFQTileOrderSide(Enum):
    BUY = rfq_operations_pb2.RFQTileOrderDetails.Action.BUY
    SELL = rfq_operations_pb2.RFQTileOrderDetails.Action.SELL


class RFQTileOrderDetails:

    def __init__(self, base: EmptyRequest = None):
        if base is not None:
            self.__request_details = rfq_operations_pb2.RFQTileOrderDetails(base=base)
        else:
            self.__request_details = rfq_operations_pb2.RFQTileOrderDetails()

    def set_window_index(self, index: int):
        self.__request_details.windowIndex = index

    def set_venue(self, venue: str):
        self.__request_details.venue = venue

    def set_action(self, action: RFQTileOrderSide):
        self.__request_details.action = action.value

    def request(self) -> rfq_operations_pb2.RFQTileOrderDetails:
        return self.__request_details


class RFQTilePanelDetails:

    def __init__(self, base: EmptyRequest = None):
        if base is not None:
            self.__request_details = rfq_operations_pb2.RFQTilePanelDetails(base=base)
        else:
            self.__request_details = rfq_operations_pb2.RFQTilePanelDetails()

    def set_window_index(self, index: int):
        self.__request_details.windowIndex = index

    def request(self) -> rfq_operations_pb2.RFQTilePanelDetails:
        return self.__request_details
