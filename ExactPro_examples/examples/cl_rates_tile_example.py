from win_gui_modules.base_test import BaseTest
from win_gui_modules.client_pricing_wrappers import BaseTileDetails, ModifyRatesTileRequest, PlaceRatesTileOrderRequest, \
    ExtractRatesTileTableValuesRequest, ExtractRatesTileValues
from win_gui_modules.order_book_wrappers import ExtractionDetail
from win_gui_modules.services import Services
from win_gui_modules.wrappers import set_base


class ClientPricingRatesTileExample(BaseTest):

    def __init__(self, services: Services, parent_event):
        super().__init__(services)
        self.create_test_event(parent_event, "TEST", "Client Pricing window, Rates Tile example")

    def execute(self):
        call = self.call
        set_base(self._session_id, self._event_id)

        cp_service = self._services.cp_operations_service

        # create rates tile order
        base_details = BaseTileDetails(base=self.get_base_request())
        call(cp_service.createRatesTile, base_details.build())

        # modify rates tile order
        modify_request = ModifyRatesTileRequest(details=base_details)
        modify_request.set_instrument("Instrument")
        modify_request.set_pips("123")
        modify_request.set_client_tier("Bronze")
        modify_request.toggle_live()
        modify_request.toggle_automated()
        modify_request.press_pricing()
        modify_request.press_executable()
        modify_request.press_use_defaults()
        modify_request.increase_ask()
        modify_request.decrease_ask()
        modify_request.increase_bid()
        modify_request.decrease_bid()
        modify_request.narrow_spread()
        modify_request.widen_spread()
        modify_request.skew_towards_ask()
        modify_request.skew_towards_bid()
        call(cp_service.modifyRatesTile, modify_request.build())

        # extract rates tile values
        extract_request = ExtractRatesTileValues(details=base_details)
        extract_request.extract_spread("ratesTile.spread")
        extract_request.extract_pips("ratesTile.pips")
        extract_request.extract_value_date("ratesTile.valueDate")
        extract_request.extract_bid_quantity("ratesTile.bidQuantity")
        extract_request.extract_ask_quantity("ratesTile.askQuantity")
        extract_request.extract_ask_large_value("ratesTile.askLargeValue")
        extract_request.extract_bid_large_value("ratesTile.bidLargeValue")
        extract_request.set_extraction_id("extrId0")
        call(cp_service.extractRateTileValues, extract_request.build())

        # extract rates tile table values
        extract_table_request = ExtractRatesTileTableValuesRequest(details=base_details)
        extract_table_request.set_extraction_id("ExtractionId1")
        extract_table_request.set_row_number(1)
        extract_table_request.set_ask_extraction_field(ExtractionDetail("rateTile.Px", "Px"))
        # extract_table_request.set_ask_extraction_fields([ExtractionDetail("rateTile.Px", "Px")])
        extract_table_request.set_bid_extraction_field(ExtractionDetail("rateTile.Px", "Px"))
        # extract_table_request.set_bid_extraction_fields([ExtractionDetail("rateTile.Px", "Px")])
        call(cp_service.extractRatesTileTableValues, extract_table_request.build())

        # place rates tile order
        place_request = PlaceRatesTileOrderRequest(details=base_details)
        place_request.set_quantity("12345")
        place_request.set_slippage("12345")
        place_request.set_stop_price("12345")
        place_request.set_order_type("OrderType")
        place_request.set_order_price_large_value("12345")
        place_request.set_order_price_pips("12345")
        place_request.set_time_in_force("TimeInForce")
        place_request.set_client("Client1")
        place_request.buy() # or sell
        # place_request.sell()
        call(cp_service.placeRatesTileOrder, place_request.build())

        # close client pricing window
        call(cp_service.closeWindow, self.get_base_request())

