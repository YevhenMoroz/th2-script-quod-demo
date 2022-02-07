from test_framework.win_gui_wrappers.fe_trading_constant import ClientPrisingTileAction, PriceNaming, Side, TimeInForce, \
    OrderType
from test_framework.win_gui_wrappers.fe_trading_constant import RatesColumnNames as col_n
from test_framework.win_gui_wrappers.forex.client_pricing_tile import ClientPricingTile
from win_gui_modules.client_pricing_wrappers import ModifyRatesTileRequest, PlaceRatesTileOrderRequest, \
    ExtractRatesTileValues, ExtractRatesTileTableValuesRequest, SelectRowsRequest, DeselectRowsRequest, \
    GetCPRTPColors, PlaceRateTileTableOrderRequest, RatesTileTableOrdSide
from win_gui_modules.order_book_wrappers import ExtractionDetail
from win_gui_modules.utils import call


class ClientRatesTile(ClientPricingTile):
    def __init__(self, case_id, session_id, index: int = 0):
        super().__init__(case_id, session_id, index)
        self.modify_request = ModifyRatesTileRequest(details=self.base_details)
        self.place_order_request = PlaceRatesTileOrderRequest(details=self.base_details)
        self.extract_values_request = ExtractRatesTileValues(details=self.base_details)
        self.extract_table_value_request = ExtractRatesTileTableValuesRequest(details=self.base_details)
        self.select_rows_request = SelectRowsRequest(details=self.base_details)
        self.deselect_rows_request = DeselectRowsRequest(details=self.base_details)
        self.extract_color_request = GetCPRTPColors(base_tile_data=self.base_data)
        self.place_order_by_row = None
        self.create_tile_call = self.cp_service.createRatesTile
        self.close_tile_call = self.cp_service.closeRatesTile

    # region Action
    def modify_client_tile(self, instrument: str = None, client_tier: str = None, pips: str = None):
        if instrument is not None:
            self.modify_request.set_instrument(instrument)
        if client_tier is not None:
            self.modify_request.set_client_tier(client_tier)
        if pips is not None:
            self.modify_request.set_pips(pips)
        call(self.cp_service.modifyRatesTile, self.modify_request.build())
        self.clear_details([self.modify_request])

    def press_pricing(self):
        self.modify_request.press_pricing()
        call(self.cp_service.modifyRatesTile, self.modify_request.build())
        self.clear_details([self.modify_request])

    def press_executable(self):
        self.modify_request.press_executable()
        call(self.cp_service.modifyRatesTile, self.modify_request.build())
        self.clear_details([self.modify_request])

    def press_use_default(self):
        self.modify_request.press_use_defaults()
        call(self.cp_service.modifyRatesTile, self.modify_request.build())
        self.clear_details([self.modify_request])

    def switch_to_tired(self):
        self.modify_request.toggle_tiered()
        call(self.cp_service.modifyRatesTile, self.modify_request.build())
        self.clear_details([self.modify_request])

    def switch_to_sweepable(self):
        self.modify_request.toggle_sweepable()
        call(self.cp_service.modifyRatesTile, self.modify_request.build())
        self.clear_details([self.modify_request])

    def press_live(self):
        self.modify_request.toggle_live()
        call(self.cp_service.modifyRatesTile, self.modify_request.build())
        self.clear_details([self.modify_request])

    def press_auto_on(self):
        self.modify_request.toggle_automated()
        call(self.cp_service.modifyRatesTile, self.modify_request.build())
        self.clear_details([self.modify_request])

    def modify_spread(self, *args: ClientPrisingTileAction):
        if ClientPrisingTileAction.increase_ask in args:
            self.modify_request.increase_ask()
        if ClientPrisingTileAction.decrease_ask in args:
            self.modify_request.decrease_ask()
        if ClientPrisingTileAction.increase_bid in args:
            self.modify_request.increase_bid()
        if ClientPrisingTileAction.decrease_bid in args:
            self.modify_request.decrease_bid()
        if ClientPrisingTileAction.narrow_spread in args:
            self.modify_request.narrow_spread()
        if ClientPrisingTileAction.widen_spread in args:
            self.modify_request.widen_spread()
        if ClientPrisingTileAction.skew_towards_ask in args:
            self.modify_request.skew_towards_ask()
        if ClientPrisingTileAction.skew_towards_bid in args:
            self.modify_request.skew_towards_bid()
        call(self.cp_service.modifyRatesTile, self.modify_request.build())
        self.clear_details([self.modify_request])

    def select_rows(self, rows: list):
        self.select_rows_request.set_row_numbers(rows)
        call(self.cp_service.selectRows, self.select_rows_request.build())

    def deselect_rows(self):
        call(self.cp_service.deselectRows, self.deselect_rows_request.build())

    def place_order(self, client: str = None, qty: str = None, side: Side = Side.buy, price_large: str = None,
                    price_pips: str = None, slippage: str = None, stop_price: str = None,
                    order_type: OrderType = OrderType.limit, tif: TimeInForce = TimeInForce.FOK):
        if client is not None:
            self.place_order_request.set_client(client)
        if qty is not None:
            self.place_order_request.set_quantity(qty)
        if price_large is not None:
            self.place_order_request.set_order_price_large_value(price_large)
        if price_pips is not None:
            self.place_order_request.set_order_price_pips(price_pips)
        if stop_price is not None:
            self.place_order_request.set_stop_price(stop_price)
        if slippage is not None:
            self.place_order_request.set_slippage(slippage)
        if order_type is OrderType.market:
            self.place_order_request.set_order_type(OrderType.market.value)
        if order_type is OrderType.previously_quoted:
            self.place_order_request.set_order_type(OrderType.previously_quoted.value)
        if tif is TimeInForce.IOC:
            self.place_order_request.set_time_in_force(TimeInForce.IOC.value)
        if side is Side.buy:
            self.place_order_request.buy()
        if side is Side.sell:
            self.place_order_request.sell()
        call(self.cp_service.placeRatesTileOrder, self.place_order_request.build())
        self.clear_details([self.place_order_request])

    def open_order_ticket_by_row(self, row, side: RatesTileTableOrdSide = RatesTileTableOrdSide.BUY):
        self.place_order_by_row = PlaceRateTileTableOrderRequest(self.base_data, row, side)
        call(self.cp_service.placeRateTileTableOrder, self.place_order_by_row.build())
        self.clear_details([self.place_order_by_row])

    # endregion

    # region Extraction
    def extract_prices_from_tile(self, *args: PriceNaming):
        if PriceNaming.ask_large in args:
            self.extract_values_request.extract_ask_large_value(PriceNaming.ask_large.value)
        if PriceNaming.ask_pips in args:
            self.extract_values_request.extract_ask_pips(PriceNaming.ask_pips.value)
        if PriceNaming.bid_large in args:
            self.extract_values_request.extract_bid_large_value(PriceNaming.bid_large.value)
        if PriceNaming.bid_pips in args:
            self.extract_values_request.extract_bid_pips(PriceNaming.bid_pips.value)
        if PriceNaming.spread in args:
            self.extract_values_request.extract_spread(PriceNaming.spread.value)
        response = call(self.cp_service.extractRateTileValues, self.extract_values_request.build())
        self.clear_details([self.extract_values_request])
        return response

    def extract_values_from_rates(self, *args: col_n, row_number: int = 1):
        """
        -----Example of usage-----
        ask_base = RatesColumnNames.ask_base
        bid_base = RatesColumnNames.bid_base
        base_before = self.rates_tile.extract_values_from_rates(bid_base, ask_base)
        -----Get extracted value-----
        value = base_before[str(bid_base)]
        """
        self.extract_table_value_request.set_row_number(row_number)
        if col_n.bid_effective in args:
            self.extract_table_value_request.set_bid_extraction_field(
                ExtractionDetail(str(col_n.bid_effective), col_n.bid_effective.value))
        if col_n.ask_effective in args:
            self.extract_table_value_request.set_bid_extraction_field(
                ExtractionDetail(str(col_n.ask_effective), col_n.ask_effective.value))
        if col_n.ask_base in args:
            self.extract_table_value_request.set_ask_extraction_field(
                ExtractionDetail(str(col_n.ask_base), col_n.ask_base.value))
        if col_n.ask_band in args:
            self.extract_table_value_request.set_ask_extraction_field(
                ExtractionDetail(str(col_n.ask_band), col_n.ask_band.value))
        if col_n.ask_pub in args:
            self.extract_table_value_request.set_ask_extraction_field(
                ExtractionDetail(str(col_n.ask_pub), col_n.ask_pub.value))
        if col_n.ask_pts in args:
            self.extract_table_value_request.set_ask_extraction_field(
                ExtractionDetail(str(col_n.ask_pts), col_n.ask_pts.value))
        if col_n.ask_spot in args:
            self.extract_table_value_request.set_ask_extraction_field(
                ExtractionDetail(str(col_n.ask_spot), col_n.ask_spot.value))
        if col_n.ask_px in args:
            self.extract_table_value_request.set_ask_extraction_field(
                ExtractionDetail(str(col_n.ask_px), col_n.ask_px.value))
        if col_n.ask_effective in args:
            self.extract_table_value_request.set_bid_extraction_field(
                ExtractionDetail(str(col_n.ask_effective), col_n.ask_effective.value))
        if col_n.bid_base in args:
            self.extract_table_value_request.set_bid_extraction_field(
                ExtractionDetail(str(col_n.bid_base), col_n.bid_base.value))
        if col_n.bid_band in args:
            self.extract_table_value_request.set_bid_extraction_field(
                ExtractionDetail(str(col_n.bid_band), col_n.bid_band.value))
        if col_n.bid_pub in args:
            self.extract_table_value_request.set_bid_extraction_field(
                ExtractionDetail(str(col_n.bid_pub), col_n.bid_pub.value))
        if col_n.bid_pts in args:
            self.extract_table_value_request.set_bid_extraction_field(
                ExtractionDetail(str(col_n.bid_pts), col_n.bid_pts.value))
        if col_n.bid_spot in args:
            self.extract_table_value_request.set_bid_extraction_field(
                ExtractionDetail(str(col_n.bid_spot), col_n.bid_spot.value))
        if col_n.bid_px in args:
            self.extract_table_value_request.set_bid_extraction_field(
                ExtractionDetail(str(col_n.bid_px), col_n.bid_px.value))
        response = call(self.cp_service.extractRatesTileTableValues, self.extract_table_value_request.build())
        self.clear_details([self.extract_table_value_request])
        return response

    def extract_header(self, instrument: str = None, client_tier: str = None, date: str = None):
        if instrument is not None:
            self.extract_values_request.extract_instrument(instrument)
        if client_tier is not None:
            self.extract_values_request.extract_client_tier(client_tier)
        if date is not None:
            self.extract_values_request.extract_value_date(date)
        response = call(self.cp_service.extractRateTileValues, self.extract_values_request.build())
        self.clear_details([self.extract_values_request])
        return response

    # endregion
    # region Check
    def check_color_of_pricing_button(self, x: int = 0, y: int = 90, expected_color: str = None):
        self.extract_color_request.get_pricing_btn_pixel_color(x, y)
        color = call(self.cp_service.getCPRatesTileColors, self.extract_color_request.build())
        self.compare_values(expected_value=expected_color, actual_value=str(color["PRICING_BUTTON"]),
                            event_name="Check color of button", value_name="Color")
        self.clear_details([self.extract_color_request])
    # endregion
