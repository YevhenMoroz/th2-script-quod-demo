from dataclasses import dataclass
from datetime import date, datetime
from enum import Enum

from th2_grpc_act_gui_quod import ar_operations_pb2
from th2_grpc_act_gui_quod.ar_operations_pb2 import CellExtractionDetails, ActionsRatesTile
from th2_grpc_act_gui_quod.common_pb2 import EmptyRequest

from win_gui_modules.common_wrappers import BaseTileDetails, MoveWindowDetails
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


class ContextActionType(Enum):
    CHECK_EMPTY_TOP_OF_BOOK_MARGINS = ar_operations_pb2.ContextActionRatesTile.ClickContextActionType.ContextActionType.CHECK_EMPTY_TOP_OF_BOOK_MARGINS
    CHECK_CUMULATIVE_TOP_OF_BOOK_MARGINS = ar_operations_pb2.ContextActionRatesTile.ClickContextActionType.ContextActionType.CHECK_CUMULATIVE_TOP_OF_BOOK_MARGINS
    CHECK_VWAP = ar_operations_pb2.ContextActionRatesTile.ClickContextActionType.ContextActionType.CHECK_VWAP
    CHECK_STRATEGIES = ar_operations_pb2.ContextActionRatesTile.ClickContextActionType.ContextActionType.CHECK_STRATEGIES
    CHECK_FULL_AMOUNT = ar_operations_pb2.ContextActionRatesTile.ClickContextActionType.ContextActionType.CHECK_FULL_AMOUNT
    CHECK_AGGREGATED_RATES = ar_operations_pb2.ContextActionRatesTile.ClickContextActionType.ContextActionType.CHECK_AGGREGATED_RATES
    CHECK_AGGREGATED_TOP_OF_BOOK = ar_operations_pb2.ContextActionRatesTile.ClickContextActionType.ContextActionType.CHECK_AGGREGATED_TOP_OF_BOOK
    CHECK_EXCLUDE_UNHEALTHY_VENUES = ar_operations_pb2.ContextActionRatesTile.ClickContextActionType.ContextActionType.CHECK_EXCLUDE_UNHEALTHY_VENUES


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
    def open_direct_venue_panel():
        action = ar_operations_pb2.ContextActionRatesTile.OpenDirectVenuePanel()
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

    @staticmethod
    def filter_full_amount_venues(venues: list):
        action = ar_operations_pb2.ContextActionRatesTile.FilterFullAmountVenues()
        for venue in venues:
            action.venues.append(venue)
        context_action = ContextActionRatesTile()
        context_action.add_action(action)
        return context_action

    @staticmethod
    def add_full_amount_qty(qty: str):
        action = ar_operations_pb2.ContextActionRatesTile.AddFullAmountQty()
        action.quantity = qty
        context_action = ContextActionRatesTile()
        context_action.add_action(action)
        return context_action

    @staticmethod
    def filter_top_of_book_venue(venue: str):
        action = ar_operations_pb2.ContextActionRatesTile.FilterTopOfBooksVenue()
        action.venue = venue
        context_action = ContextActionRatesTile()
        context_action.add_action(action)
        return context_action

    @staticmethod
    def add_context_action_type(context_action_types: list, details: BaseTileDetails = None):
        action = ar_operations_pb2.ContextActionRatesTile.ClickContextActionType()
        action.data.CopyFrom(details.build())
        for act in context_action_types:
            action.actionType.append(act)
        context_action = ContextActionRatesTile()
        context_action.add_action(action)
        return context_action

    @staticmethod
    def add_aggregated_rates(context_action_types=[ContextActionType.CHECK_AGGREGATED_RATES.value],
                             details: BaseTileDetails = None):
        action = ar_operations_pb2.ContextActionRatesTile.ClickContextActionType()
        action.data.CopyFrom(details.build())
        for act in context_action_types:
            action.actionType.append(act)
        context_action = ContextActionRatesTile()
        context_action.add_action(action)
        return context_action


    @staticmethod
    def open_full_amount(context_action_types=[ContextActionType.CHECK_FULL_AMOUNT.value]
                             ):
        action = ar_operations_pb2.ContextActionRatesTile.ClickContextActionType()
        for act in context_action_types:
            action.actionType.append(act)
        context_action = ContextActionRatesTile()
        context_action.add_action(action)
        return context_action


    def add_action(self, action):
        if isinstance(action, ar_operations_pb2.ContextActionRatesTile.FilterVenues):
            self.request.filterVenues.CopyFrom(action)
        elif isinstance(action, ar_operations_pb2.ContextActionRatesTile.ClickToButton):
            self.request.buttonClick.CopyFrom(action)
        elif isinstance(action, ar_operations_pb2.ContextActionRatesTile.OpenDirectVenuePanel):
            self.request.openDirectVenuePanel.CopyFrom(action)
        elif isinstance(action, ar_operations_pb2.ContextActionRatesTile.FilterFullAmountVenues):
            self.request.filterFullAmountVenues.CopyFrom(action)
        elif isinstance(action, ar_operations_pb2.ContextActionRatesTile.AddFullAmountQty):
            self.request.addFullAmountQty.CopyFrom(action)
        elif isinstance(action, ar_operations_pb2.ContextActionRatesTile.FilterTopOfBooksVenue):
            self.request.filterTopOfBooksVenue.CopyFrom(action)
        elif isinstance(action, ar_operations_pb2.ContextActionRatesTile.ClickContextActionType):
            self.request.clickContextActionType.CopyFrom(action)
        elif isinstance(action, ar_operations_pb2.ContextActionRatesTile.FilterSyntheticCombinations):
            self.request.filterSyntheticCombinations.CopyFrom(action)


    @staticmethod
    def filter_synthetic_combination(currenc_pair: str):
        action = ar_operations_pb2.ContextActionRatesTile.FilterSyntheticCombinations()
        action.currencyPair.append(currenc_pair)
        context_action = ContextActionRatesTile()
        context_action.add_action(action)
        return context_action

    @staticmethod
    def filter_synthetic_combinations(currency_pair_list: list):
        action = ar_operations_pb2.ContextActionRatesTile.FilterSyntheticCombinations()
        for currenc_pair in currency_pair_list:
            action.currencyPair.append(currenc_pair)
        context_action = ContextActionRatesTile()
        context_action.add_action(action)
        return context_action


    def build(self):
        return self.request


class ActionsRatesTile:
    def __init__(self):
        self.request = ar_operations_pb2.ActionsRatesTile()

    @staticmethod
    def click_to_ask_esp_order(venue: str):
        action = ar_operations_pb2.ActionsRatesTile.ClickToAskESPOrder()
        action.venue = venue
        action_rates = ActionsRatesTile()
        action_rates.add_action(action)
        return action_rates

    @staticmethod
    def click_to_bid_esp_order(venue: str):
        action = ar_operations_pb2.ActionsRatesTile.ClickToBidESPOrder()
        action.venue = venue
        action_rates = ActionsRatesTile()
        action_rates.add_action(action)
        return action_rates


    @staticmethod
    def click_on_full_amounts_sell_button(qty: str):
        action = ar_operations_pb2.ActionsRatesTile.ClickOnFullAmountsSellButton()
        action.quantity = qty
        action_rates = ActionsRatesTile()
        action_rates.add_action(action)
        return action_rates


    @staticmethod
    def click_on_full_amounts_buy_button(qty: str):
        action = ar_operations_pb2.ActionsRatesTile.ClickOnFullAmountsBuyButton()
        action.quantity = qty
        action_rates = ActionsRatesTile()
        action_rates.add_action(action)
        return action_rates

    @staticmethod
    def click_to_ask_esp_order_by_quantity(venue: str, quantity: str):
        action = ar_operations_pb2.ActionsRatesTile.ClickToAskESPOrderByQuantity()
        action.venue = venue
        action.quantity = quantity
        action_rates = ActionsRatesTile()
        action_rates.add_action(action)
        return action_rates

    @staticmethod
    def click_to_bid_esp_order_by_quantity(venue: str, quantity: str):
        action = ar_operations_pb2.ActionsRatesTile.ClickToBidESPOrderByQuantity()
        action.venue = venue
        action.quantity = quantity
        action_rates = ActionsRatesTile()
        action_rates.add_action(action)
        return action_rates

    @staticmethod
    def click_to_direct_venue_add_raw(venue: str):
        action = ar_operations_pb2.ActionsRatesTile.ClickToDirectVenueAddRaw()
        action.venue = venue
        action_rates = ActionsRatesTile()
        action_rates.add_action(action)
        return action_rates

    @staticmethod
    def click_to_direct_venue_remove_raw(venue: str):
        action = ar_operations_pb2.ActionsRatesTile.ClickToDirectVenueRemoveRawCorrect()
        action.venue = venue
        action_rates = ActionsRatesTile()
        action_rates.add_action(action)
        return action_rates

    @staticmethod
    def click_to_resting_orders_checkbox():
        action = ar_operations_pb2.ActionsRatesTile.ClickToRestingOrdersCheckBox()
        action_rates = ActionsRatesTile()
        action_rates.add_action(action)
        return action_rates

    def add_action(self, action):
        if isinstance(action, ar_operations_pb2.ActionsRatesTile.ClickToAskESPOrder):
            self.request.clickToAskESPOrder.CopyFrom(action)
        elif isinstance(action, ar_operations_pb2.ActionsRatesTile.ClickToBidESPOrder):
            self.request.clickToBidESPOrder.CopyFrom(action)
        elif isinstance(action, ar_operations_pb2.ActionsRatesTile.ClickToAskESPOrderByQuantity):
            self.request.clickToAskESPOrderByQuantity.CopyFrom(action)
        elif isinstance(action, ar_operations_pb2.ActionsRatesTile.ClickToBidESPOrderByQuantity):
            self.request.clickToBidESPOrderByQuantity.CopyFrom(action)
        elif isinstance(action, ar_operations_pb2.ActionsRatesTile.ClickToDirectVenueAddRaw):
            self.request.clickToDirectVenueAddRaw.CopyFrom(action)
        elif isinstance(action, ar_operations_pb2.ActionsRatesTile.ClickToDirectVenueRemoveRawCorrect):
            self.request.clickToDirectVenueRemoveRawCorrect2.CopyFrom(action)
        elif isinstance(action, ar_operations_pb2.ActionsRatesTile.ClickToRestingOrdersCheckBox):
            self.request.clickToRestingOrdersCheckBox.CopyFrom(action)
        elif isinstance(action, ar_operations_pb2.ActionsRatesTile.ClickOnFullAmountsSellButton):
            self.request.clickOnFullAmountsSellButton.CopyFrom(action)
        elif isinstance(action, ar_operations_pb2.ActionsRatesTile.ClickOnFullAmountsBuyButton):
            self.request.clickOnFullAmountsBuyButton.CopyFrom(action)

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

    def clear_near_date(self, clear_near_date: bool):
        self.modify_request.clearNearDate = clear_near_date

    def clear_far_leg_date(self, clear_far_leg_date: bool):
        self.modify_request.clearFarLegDate = clear_far_leg_date

    def clear_quantity(self, clear_quantity: bool):
        self.modify_request.clearQuantity = clear_quantity

    def clear_far_leg_quantity(self, clear_far_leg_quantity: bool):
        self.modify_request.clearFarLegQuantity = clear_far_leg_quantity

    def clear_far_leg_tenor(self, clear_far_leg_tenor: bool):
        self.modify_request.clearFarTenor = clear_far_leg_tenor

    def set_settlement_date(self, settlement_date: date):
        self.modify_request.settlementDate.FromDatetime(datetime.fromordinal(settlement_date.toordinal()))

    def set_maturity_date(self, settlement_date: date):
        self.modify_request.maturityDate.FromDatetime(datetime.fromordinal(settlement_date.toordinal()))

    def set_far_leg_settlement_date(self, settlement_date: date):
        self.modify_request.farLegSettlementDate.FromDatetime(datetime.fromordinal(settlement_date.toordinal()))

    def set_far_maturity_date(self, settlement_date: date):
        self.modify_request.farMaturityDate.FromDatetime(datetime.fromordinal(settlement_date.toordinal()))

    def set_client(self, client: str):
        self.modify_request.client = client

    def set_quantity(self, quantity: int):
        self.modify_request.quantity.value = quantity

    def set_quantity2(self, quantity: int):
        self.modify_request.farLegQuantity.value = quantity

    def set_quantity_as_string(self, quantity: str):
        self.modify_request.quantityAsString = quantity

    def set_far_leg_quantity_as_string(self, quantity: str):
        self.modify_request.farLegQuantityAsString = quantity

    def set_far_leg_qty(self, quantity: int):
        self.modify_request.farLegQuantity.value = quantity

    def click_checkbox_left(self):
        self.modify_request.clickLeftBox = True

    def click_checkbox_right(self):
        self.modify_request.clickRightBox = True

    def add_context_action(self, context_action: ContextAction):
        self.modify_request.contextActions.append(context_action.build())

    def add_context_actions(self, context_actions: list):
        for action in context_actions:
            self.add_context_action(action)

    def add_actions(self, actions_rates: list):
        for action in actions_rates:
            self.add_actions(action)

    def build(self):
        return self.modify_request


class ModifyRatesTileRequest:
    def __init__(self, details: BaseTileDetails = None):
        self.modify_request = ar_operations_pb2.ModifyRatesTileRequest(data=details.build())

    def set_details(self, details: BaseTileDetails):
        self.modify_request.data.CopyFrom(details.build())

    def set_from_currency(self, currency: str):
        self.modify_request.fromCurrency = currency

    def set_to_currency(self, currency: str):
        self.modify_request.toCurrency = currency

    def set_tenor(self, tenor: str):
        self.modify_request.tenor = tenor

    def set_settlement_date(self, settlement_date: date):
        self.modify_request.settlementDate.FromDatetime(datetime.fromordinal(settlement_date.toordinal()))

    def clear_settlement_date(self, clear_settlement_date: bool):
        self.modify_request.clearSettlementDate = clear_settlement_date

    def set_instrument(self, from_currency: str, to_currency: str, set_tenor: str):
        self.modify_request.changeInstrument = True
        self.modify_request.fromCurrency = from_currency
        self.modify_request.toCurrency = to_currency
        self.modify_request.tenor = set_tenor

    def set_quantity(self, quantity: str):
        self.modify_request.changeQty = True
        self.modify_request.quantityAsString = quantity

    def set_click_on_one_click_button(self):
        self.modify_request.clickOnOneClick = True

    def add_context_action(self, context_action: ContextActionRatesTile):
        self.modify_request.contextActions.append(context_action.build())

    def add_context_actions(self, context_actions: list):
        for context_action in context_actions:
            self.add_context_action(context_action)

    def clear_quantity(self, clear_quantity: bool):
        self.modify_request.clearQuantity = clear_quantity

    # def set_instrument(self, need_to_set_instrument: bool, from_currency: str, to_currency: str, set_tenor: str):
    #     self.modify_request.changeInstrument = need_to_set_instrument
    #     self.modify_request.fromCurrency = from_currency
    #     self.modify_request.toCurrency = to_currency
    #     self.modify_request.tenor = set_tenor

    def set_quantity_(self, need_to_set_quantity: bool, quantity: str):
        self.modify_request.changeQty = need_to_set_quantity
        self.modify_request.quantityAsString = quantity

    def add_action(self, actions_rates: ActionsRatesTile):
        self.modify_request.actions.append(actions_rates.build())

    def add_actions(self, actions_rates: list):
        for action in actions_rates:
            self.add_action(action)

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
    IS_BUY_BUTTON_ENABLED = ar_operations_pb2.ExtractRFQTileValuesRequest.ExtractedType.BUY_BUTTON_ENABLED
    IS_SELL_BUTTON_ENABLED = ar_operations_pb2.ExtractRFQTileValuesRequest.ExtractedType.SELL_BUTTON_ENABLED

    BEST_BID_LARGE = ar_operations_pb2.ExtractRFQTileValuesRequest.ExtractedType.BEST_BID_LARGE
    BEST_BID_SMALL = ar_operations_pb2.ExtractRFQTileValuesRequest.ExtractedType.BEST_BID_SMALL
    BEST_ASK_LARGE = ar_operations_pb2.ExtractRFQTileValuesRequest.ExtractedType.BEST_ASK_LARGE
    BEST_ASK_SMALL = ar_operations_pb2.ExtractRFQTileValuesRequest.ExtractedType.BEST_ASK_SMALL
    SPREAD = ar_operations_pb2.ExtractRFQTileValuesRequest.ExtractedType.SPREAD
    SWAP_DIFF_DAYS = ar_operations_pb2.ExtractRFQTileValuesRequest.ExtractedType.SWAP_DIFF_DAYS
    BENEFICIARY = ar_operations_pb2.ExtractRFQTileValuesRequest.ExtractedType.BENEFICIARY
    BEST_BID = ar_operations_pb2.ExtractRFQTileValuesRequest.ExtractedType.BEST_BID
    BEST_ASK = ar_operations_pb2.ExtractRFQTileValuesRequest.ExtractedType.BEST_ASK
    CLIENT = ar_operations_pb2.ExtractRFQTileValuesRequest.ExtractedType.CLIENT
    LABEL_BUY = ar_operations_pb2.ExtractRFQTileValuesRequest.ExtractedType.LABEL_BUY
    LABEL_SELL = ar_operations_pb2.ExtractRFQTileValuesRequest.ExtractedType.LABEL_SELL
    NEAR_MATURITY_DATE = ar_operations_pb2.ExtractRFQTileValuesRequest.ExtractedType.NEAR_MATURITY_DATE
    FAR_MATURITY_DATE = ar_operations_pb2.ExtractRFQTileValuesRequest.ExtractedType.FAR_MATURITY_DATE
    LEFT_CHECKBOX = ar_operations_pb2.ExtractRFQTileValuesRequest.ExtractedType.LEFT_CHECKBOX
    RIGHT_CHECKBOX = ar_operations_pb2.ExtractRFQTileValuesRequest.ExtractedType.RIGHT_CHECKBOX
    SEND_BUTTON_TEXT = ar_operations_pb2.ExtractRFQTileValuesRequest.ExtractedType.SEND_BUTTON_TEXT


class RatesTileValues(Enum):
    INSTRUMENT = ar_operations_pb2.ExtractRatesTileValuesRequest.ExtractedType.INSTRUMENT
    TENOR_DATE = ar_operations_pb2.ExtractRatesTileValuesRequest.ExtractedType.TENOR_DATE
    QUANTITY = ar_operations_pb2.ExtractRatesTileValuesRequest.ExtractedType.QUANTITY
    BEST_BID_LARGE = ar_operations_pb2.ExtractRatesTileValuesRequest.ExtractedType.BEST_BID_LARGE
    BEST_BID_SMALL = ar_operations_pb2.ExtractRatesTileValuesRequest.ExtractedType.BEST_BID_SMALL
    BEST_ASK_LARGE = ar_operations_pb2.ExtractRatesTileValuesRequest.ExtractedType.BEST_ASK_LARGE
    BEST_ASK_SMALL = ar_operations_pb2.ExtractRatesTileValuesRequest.ExtractedType.BEST_ASK_SMALL
    SPREAD = ar_operations_pb2.ExtractRatesTileValuesRequest.ExtractedType.SPREAD
    BEST_BID = ar_operations_pb2.ExtractRatesTileValuesRequest.ExtractedType.BEST_BID
    BEST_ASK = ar_operations_pb2.ExtractRatesTileValuesRequest.ExtractedType.BEST_ASK


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

    def extract_near_maturity_date(self, name: str):
        self.extract_value(RFQTileValues.NEAR_MATURITY_DATE, name)

    def extract_far_maturity_date(self, name: str):
        self.extract_value(RFQTileValues.FAR_MATURITY_DATE, name)

    def extract_far_leg_settlement_date(self, name: str):
        self.extract_value(RFQTileValues.FAR_LEG_SETTLEMENT_DATE, name)

    def extract_best_bid(self, name: str):
        self.extract_value(RFQTileValues.BEST_BID, name)

    def extract_best_bid_large(self, name: str):
        self.extract_value(RFQTileValues.BEST_BID_LARGE, name)

    def extract_best_bid_small(self, name: str):
        self.extract_value(RFQTileValues.BEST_BID_SMALL, name)

    def extract_best_ask(self, name: str):
        self.extract_value(RFQTileValues.BEST_ASK, name)

    def extract_best_ask_large(self, name: str):
        self.extract_value(RFQTileValues.BEST_ASK_LARGE, name)

    def extract_best_ask_small(self, name: str):
        self.extract_value(RFQTileValues.BEST_ASK_SMALL, name)

    def extract_spread(self, name: str):
        self.extract_value(RFQTileValues.SPREAD, name)

    def extract_swap_diff_days(self, name: str):
        self.extract_value(RFQTileValues.SWAP_DIFF_DAYS, name)

    def extract_beneficiary(self, name: str):
        self.extract_value(RFQTileValues.BENEFICIARY, name)

    def extract_client(self, name: str):
        self.extract_value(RFQTileValues.CLIENT, name)

    def extract_cur_label_right(self, name: str):
        self.extract_value(RFQTileValues.LABEL_BUY, name)

    def extract_cur_label_left(self, name: str):
        self.extract_value(RFQTileValues.LABEL_SELL, name)

    def extract_left_checkbox(self, name: str):
        self.extract_value(RFQTileValues.LEFT_CHECKBOX, name)

    def extract_right_checkbox(self, name: str):
        self.extract_value(RFQTileValues.RIGHT_CHECKBOX, name)

    def extract_send_button_text(self, name: str):
        self.extract_value(RFQTileValues.SEND_BUTTON_TEXT, name)

    def extract_near_tenor_list(self, preFilter: str = None):
        if preFilter is not None:
            self.request.tenorFilter = preFilter
        else:
            self.request.tenorFilter = ''

    def extract_is_buy_button_enabled(self, name: str):
        self.extract_value(RFQTileValues.IS_BUY_BUTTON_ENABLED, name)

    def extract_is_sell_button_enabled(self, name: str):
        self.extract_value(RFQTileValues.IS_SELL_BUTTON_ENABLED, name)

    def extract_value(self, field: RFQTileValues, name: str):
        extracted_value = ar_operations_pb2.ExtractRFQTileValuesRequest.ExtractedValue()
        extracted_value.type = field.value
        extracted_value.name = name
        self.request.extractedValues.append(extracted_value)

    def build(self):
        return self.request


class ExtractHeaders(object):
    rowNumber: int


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
        extract_cell.extractionField.colName = detail.col_name
        extract_cell.extractionField.venueName = detail.venue_name
        extract_cell.extractionField.intSide = detail.int_side
        action = TableAction()
        action.set_action(extract_cell)
        return action

    @staticmethod
    def extract_headers(colIndexes: list):
        extract_headers = ar_operations_pb2.TableAction.ExtractHeaders()
        for colIndex in colIndexes:
            extract_headers.cols.append(colIndex)

        action = TableAction()
        action.set_action(extract_headers)
        return action

    def set_action(self, action):
        if isinstance(action, ar_operations_pb2.TableAction.CheckTableVenuesRequest):
            self.request.checkTableVenues.CopyFrom(action)
        if isinstance(action, ar_operations_pb2.TableAction.ExtractCellValue):
            self.request.extractCellValue.CopyFrom(action)
        if isinstance(action, ar_operations_pb2.TableAction.ExtractHeaders):
            self.request.extractHeaders.CopyFrom(action)

    def build(self):
        return self.request


class ExtractRatesTileDataRequest:

    def __init__(self, details: BaseTileDetails):
        self.request = ar_operations_pb2.ExtractRatesTileValuesRequest(data=details.build())

    def set_extraction_id(self, extraction_id: str):
        self.request.extractionId = extraction_id

    def extract_instrument(self, name: str):
        self.extract_value(RatesTileValues.INSTRUMENT, name)

    def extract_tenor_date(self, name: str):
        self.extract_value(RatesTileValues.TENOR_DATE, name)

    def extract_quantity(self, name: str):
        self.extract_value(RatesTileValues.QUANTITY, name)

    def extract_best_bid_large(self, name: str):
        self.extract_value(RatesTileValues.BEST_BID_LARGE, name)

    def extract_best_bid_small(self, name: str):
        self.extract_value(RatesTileValues.BEST_BID_SMALL, name)

    def extract_best_ask_large(self, name: str):
        self.extract_value(RatesTileValues.BEST_ASK_LARGE, name)

    def extract_best_ask_small(self, name: str):
        self.extract_value(RatesTileValues.BEST_ASK_SMALL, name)

    def extract_spread(self, name: str):
        self.extract_value(RatesTileValues.SPREAD, name)

    def extract_best_bid(self, name: str):
        self.extract_value(RatesTileValues.BEST_BID, name)

    def extract_best_ask(self, name: str):
        self.extract_value(RatesTileValues.BEST_ASK, name)

    def extract_1click_btn_text(self, name: str):
        self.extract_value(RatesTileValues.ONE_CLICK_BTN_TEXT, name)

    def extract_value(self, field: RatesTileValues, name: str):
        extracted_value = ar_operations_pb2.ExtractRatesTileValuesRequest.ExtractedValue()
        extracted_value.type = field.value
        extracted_value.name = name
        self.request.extractedValues.append(extracted_value)

    def build(self):
        return self.request


@dataclass
class CellExtractionDetails:
    name: str
    col_name: str
    venue_name: str
    int_side: int


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


# The buy and sell side have been reversed because act confused them
class ESPTileOrderSide(Enum):
    # buy and sell is top of book pips
    BUY = ar_operations_pb2.ESPTileOrderDetails.Action.SELL
    SELL = ar_operations_pb2.ESPTileOrderDetails.Action.BUY


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

# TODO: quod - refactor
@dataclass
class ESPExtractionDetails:
    name: str


class ExtractedType(Enum):
    price_pips = ar_operations_pb2.ESPTileOrderDetails.ExtractedType.PRICE_PIPS
    price_large = ar_operations_pb2.ESPTileOrderDetails.ExtractedType.PRICE_LARGE_VALUE
    qty = ar_operations_pb2.ESPTileOrderDetails.ExtractedType.QUANTITY
    instrument = ar_operations_pb2.ESPTileOrderDetails.ExtractedType.INSTRUMENT
    order_type = ar_operations_pb2.ESPTileOrderDetails.ExtractedType.ORDER_TYPE
    time_in_force = ar_operations_pb2.ESPTileOrderDetails.ExtractedType.TIME_IN_FORCE
    side_button = ar_operations_pb2.ESPTileOrderDetails.ExtractedType.SIDE_BUTTON


class PlaceESPOrder:
    def __init__(self, details: BaseTileDetails = None):
        if details is not None:
            self.__request_details = ar_operations_pb2.ESPTileOrderDetails(data=details.build())
        else:
            self.__request_details = ar_operations_pb2.ESPTileOrderDetails()

    def set_details(self, details: BaseTileDetails):
        self.__request_details.data.CopyFrom(details.build())

    def set_venue(self, venue: str):
        self.__request_details.venue = venue

    def set_action(self, action: ESPTileOrderSide):
        self.__request_details.action = action.value

    def top_of_book(self, check: bool = True):
        self.__request_details.topOfBook = check

    def build(self) -> ar_operations_pb2.ESPTileOrderDetails:
        return self.__request_details


class MoveESPOrderTicketRequest:
    def __init__(self, base: EmptyRequest = None):
        self.base = base
        self.request = ar_operations_pb2.MoveESPOrderTicketRequest()
        self.move_window_request = None

    def set_default_params(self, base_request):
        self.base = base_request

    def ask(self):
        self.request.side = ar_operations_pb2.MoveESPOrderTicketRequest.Side.ASK

    def bid(self):
        self.request.side = ar_operations_pb2.MoveESPOrderTicketRequest.Side.BID

    def top_of_book(self):
        self.request.topOfBook = True

    def panel_index(self, index):
        self.request.panelIndex = index

    def add_move_window_details(self) -> MoveWindowDetails():
        self.move_window_request = MoveWindowDetails()
        return self.move_window_request

    def build(self):
        self.move_window_request.set_default_params(self.base)
        self.request.moveWindowDetails.CopyFrom(self.move_window_request.build())
        return self.request

