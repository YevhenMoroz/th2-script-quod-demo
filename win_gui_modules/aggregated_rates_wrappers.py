from dataclasses import dataclass
from datetime import date, datetime
from enum import Enum

from th2_grpc_act_gui_quod import ar_operations_pb2
from th2_grpc_act_gui_quod.ar_operations_pb2 import CellExtractionDetails

from win_gui_modules.common_wrappers import BaseTileDetails
from win_gui_modules.order_book_wrappers import ExtractionDetail


class ContextAction:
    def __init__(self):
        self.request = ar_operations_pb2.ContextAction()

    @staticmethod
    def create_venue_filter(venue: str):
        action = ar_operations_pb2.ContextAction.FilterVenues()
        action.venues.append(venue)
        context_action = ContextAction()
        context_action.add_action(action)
        return context_action

    @staticmethod
    def create_venue_filters(venues: list):
        action = ar_operations_pb2.ContextAction.FilterVenues()
        for venue in venues:
            action.venues.append(venue)
        context_action = ContextAction()
        context_action.add_action(action)
        return context_action

    @staticmethod
    def create_button_click(button_name: str):
        action = ar_operations_pb2.ContextAction.ClickToButton()
        action.buttonName = button_name
        context_action = ContextAction()
        context_action.add_action(action)
        return context_action

    def add_action(self, action):
        if isinstance(action, ar_operations_pb2.ContextAction.FilterVenues):
            self.request.filterVenues.CopyFrom(action)
        elif isinstance(action, ar_operations_pb2.ContextAction.ClickToButton):
            self.request.buttonClick.CopyFrom(action)

    def build(self):
        return self.request


class ContextActionRatesTile:
    def __init__(self):
        self.request = ar_operations_pb2.ContextActionRatesTile()

    @staticmethod
    def create_venue_filter(venue: str):
        action = ar_operations_pb2.ContextActionRatesTile.FilterVenues()
        action.venues.append(venue)
        context_action = ContextActionRatesTile()
        context_action.add_action(action)
        return context_action

    @staticmethod
    def create_venue_filters(venues: list):
        action = ar_operations_pb2.ContextActionRatesTile.FilterVenues()
        for venue in venues:
            action.venues.append(venue)
        context_action = ContextActionRatesTile()
        context_action.add_action(action)
        return context_action

    @staticmethod
    def create_button_click(button_name: str):
        action = ar_operations_pb2.ContextActionRatesTile.ClickToButton()
        action.buttonName = button_name
        context_action = ContextActionRatesTile()
        context_action.add_action(action)
        return context_action

    def add_action(self, action):
        if isinstance(action, ar_operations_pb2.ContextActionRatesTile.FilterVenues):
            self.request.filterVenues.CopyFrom(action)
        elif isinstance(action, ar_operations_pb2.ContextActionRatesTile.ClickToButton):
            self.request.buttonClick.CopyFrom(action)

    def build(self):
        return self.request


class ModifyRFQTileRequest:
    def __init__(self, details: BaseTileDetails = None):
        if details is not None:
            self.modify_request = ar_operations_pb2.ModifyRFQTileRequest(data=details.build())
        else:
            self.modify_request = ar_operations_pb2.ModifyRFQTileRequest()

    def set_details(self, details: BaseTileDetails):
        self.modify_request.data.CopyFrom(details.build())

    def set_from_currency(self, currency: str):
        self.modify_request.fromCurrency = currency

    def set_to_currency(self, currency: str):
        self.modify_request.toCurrency = currency

    def set_near_tenor(self, tenor: str):
        self.modify_request.nearTenor = tenor

    def set_far_leg_tenor(self, tenor: str):
        self.modify_request.farLegTenor = tenor

    def set_change_currency(self, change_currency: bool):
        self.modify_request.changeCurrency = change_currency

    def set_settlement_date(self, settlement_date: date):
        self.modify_request.settlementDate.FromDatetime(datetime.fromordinal(settlement_date.toordinal()))

    def set_far_leg_settlement_date(self, settlement_date: date):
        self.modify_request.farLegSettlementDate.FromDatetime(datetime.fromordinal(settlement_date.toordinal()))

    def set_client(self, client: str):
        self.modify_request.client = client

    def set_quantity(self, quantity: int):
        self.modify_request.quantity.value = quantity

    def set_far_leg_qty(self, quantity: int):
        self.modify_request.farLegQuantity.value = quantity

    def add_context_action(self, context_action: ContextAction):
        self.modify_request.contextActions.append(context_action.build())

    def add_context_actions(self, context_actions: list):
        for action in context_actions:
            self.add_context_action(action)

    def build(self):
        return self.modify_request


class ModifyRatesTileRequest:
    def __init__(self, details: BaseTileDetails = None):
        self.modify_request = ar_operations_pb2.ModifyRatesTileRequest()

    def set_details(self, details: BaseTileDetails):
        self.modify_request.data.CopyFrom(details.build())

    def set_from_currency(self, currency: str):
        self.modify_request.fromCurrency = currency

    def set_to_currency(self, currency: str):
        self.modify_request.toCurrency = currency
    def set_tenor(self, tenor: str):
        self.modify_request.tenor = tenor

    def set_change_instrument(self, change_instrument: bool):
        self.modify_request.changeInstrument = change_instrument

    def set_quantity(self, quantity: int):
        self.modify_request.quantity.value = quantity

    def set_change_qty(self, qty: bool):
        self.modify_request.changeQty = qty

    def add_context_action(self, context_action: ContextActionRatesTile):
        self.modify_request.contextActions.append(context_action.build())

    def add_context_actions(self, context_actions: list):
        for action in context_actions:
            self.add_context_action(action)

    def set_click_on_one_click_button(self):
        self.modify_request.clickOnOneClick = True

    def build(self):
        return self.modify_request


class RFQTileValues(Enum):
    CURRENCY_PAIR = ar_operations_pb2.ExtractRFQTileValuesRequest.ExtractedType.CURRENCY_PAIR
    CURRENCY = ar_operations_pb2.ExtractRFQTileValuesRequest.ExtractedType.CURRENCY
    QUANTITY = ar_operations_pb2.ExtractRFQTileValuesRequest.ExtractedType.QUANTITY
    FAR_LEG_QTY = ar_operations_pb2.ExtractRFQTileValuesRequest.ExtractedType.FAR_LEG_QUANTITY
    TENOR = ar_operations_pb2.ExtractRFQTileValuesRequest.ExtractedType.TENOR
    FAR_LEG_TENOR = ar_operations_pb2.ExtractRFQTileValuesRequest.ExtractedType.FAR_LEG_TENOR
    NEAR_SETTLEMENT_DATE = ar_operations_pb2.ExtractRFQTileValuesRequest.ExtractedType.NEAR_SETTLEMENT_DATE
    FAR_LEG_SETTLEMENT_DATE = ar_operations_pb2.ExtractRFQTileValuesRequest.ExtractedType.FAR_LEG_SETTLEMENT_DATE


class ExtractRFQTileValues:
    def __init__(self, details: BaseTileDetails = None):
        if details is not None:
            self.request = ar_operations_pb2.ExtractRFQTileValuesRequest(data=details.build())
        else:
            self.request = ar_operations_pb2.ExtractRFQTileValuesRequest()

    def set_details(self, details: BaseTileDetails):
        self.request.data.CopyFrom(details.build())

    def set_extraction_id(self, extraction_id: str):
        self.request.extractionId = extraction_id

    def extract_currency_pair(self, name: str):
        self.extract_value(RFQTileValues.CURRENCY_PAIR, name)

    def extract_currency(self, name: str):
        self.extract_value(RFQTileValues.CURRENCY, name)

    def extract_quantity(self, name: str):
        self.extract_value(RFQTileValues.QUANTITY, name)

    def extract_far_leg_qty(self, name: str):
        self.extract_value(RFQTileValues.FAR_LEG_QTY, name)

    def extract_tenor(self, name: str):
        self.extract_value(RFQTileValues.TENOR, name)

    def extract_far_leg_tenor(self, name: str):
        self.extract_value(RFQTileValues.FAR_LEG_TENOR, name)

    def extract_near_settlement_date(self, name: str):
        self.extract_value(RFQTileValues.NEAR_SETTLEMENT_DATE, name)

    def extract_far_leg_settlement_date(self, name: str):
        self.extract_value(RFQTileValues.FAR_LEG_SETTLEMENT_DATE, name)

    def extract_value(self, field: RFQTileValues, name: str):
        extracted_value = ar_operations_pb2.ExtractRFQTileValuesRequest.ExtractedValue()
        extracted_value.type = field.value
        extracted_value.name = name
        self.request.extractedValues.append(extracted_value)

    def build(self):
        return self.request


class TableAction:
    def __init__(self):
        self.request = ar_operations_pb2.TableAction()

    @staticmethod
    def create_check_table_venue(detail: ExtractionDetail):
        check_venue = ar_operations_pb2.TableAction.CheckTableVenuesRequest()
        check_venue.extractionField.colName = detail.column_name
        check_venue.extractionField.name = detail.name
        action = TableAction()
        action.set_action(check_venue)
        return action

    @staticmethod
    def extract_cell_value(detail: CellExtractionDetails):
        extract_cell = ar_operations_pb2.TableAction.ExtractCellValue()
        extract_cell.extractionField.name = detail.name
        extract_cell.extractionField.colName = detail.colName
        extract_cell.extractionField.venueName = detail.venueName
        extract_cell.extractionField.intSide = detail.intSide
        action = TableAction()
        action.set_action(extract_cell)
        return action

    def set_action(self, action):
        if isinstance(action, ar_operations_pb2.TableAction.CheckTableVenuesRequest):
            self.request.checkTableVenues.CopyFrom(action)
        if isinstance(action,ar_operations_pb2.TableAction.ExtractCellValue):
            self.request.extractCellValue.CopyFrom(action)


    def build(self):
        return self.request


@dataclass
class CellExtractionDetails:
    name: str
    colName: str
    venueName: str
    intSide: int


class TableActionsRequest:
    def __init__(self, details: BaseTileDetails = None):
        if details is not None:
            self.request = ar_operations_pb2.TableActionsRequest(data=details.build())
        else:
            self.request = ar_operations_pb2.TableActionsRequest()

    def set_details(self, details: BaseTileDetails):
        self.request.data.CopyFrom(details.build())

    def set_extraction_id(self, extraction_id: str):
        self.request.extractionId = extraction_id

    def add_action(self, action: TableAction):
        self.request.tableActions.append(action.build())

    def add_actions(self, actions: list):
        for action in actions:
            self.add_action(action)

    def build(self):
        return self.request


class RFQTileOrderSide(Enum):
    BUY = ar_operations_pb2.RFQTileOrderDetails.Action.BUY
    SELL = ar_operations_pb2.RFQTileOrderDetails.Action.SELL

class PlaceRFQRequest:
    def __init__(self, details: BaseTileDetails = None):
        if details is not None:
            self.__request_details = ar_operations_pb2.RFQTileOrderDetails(data=details.build())
        else:
            self.__request_details = ar_operations_pb2.RFQTileOrderDetails()

    def set_details(self, details: BaseTileDetails):
        self.__request_details.data.CopyFrom(details.build())

    def set_venue(self, venue: str):
        self.__request_details.venue = venue

    def set_action(self, action: RFQTileOrderSide):
        self.__request_details.action = action.value

    def build(self) -> ar_operations_pb2.RFQTileOrderDetails:
        return self.__request_details
