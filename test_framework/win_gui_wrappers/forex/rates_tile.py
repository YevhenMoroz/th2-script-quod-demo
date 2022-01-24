from test_framework.win_gui_wrappers.forex.aggregates_rates_tile import AggregatesRatesTile
from win_gui_modules.aggregated_rates_wrappers import ModifyRatesTileRequest, PlaceESPOrder, ContextActionRatesTile, \
    ESPTileOrderSide, ActionsRatesTile
from custom import basic_custom_actions as bca
from win_gui_modules.utils import call


class RatesTile(AggregatesRatesTile):
    def __init__(self, case_id, session_id, index: int = 0):
        super().__init__(case_id, session_id, index)
        self.modify_request = ModifyRatesTileRequest(details=self.base_details)
        self.place_order_request = PlaceESPOrder(details=self.base_details)
        self.create_tile_call = self.ar_service.createRatesTile
        self.close_tile_call = self.ar_service.closeRatesTile
        self.context_action = ContextActionRatesTile()
        self.action_rates_tile = ActionsRatesTile()

    # region Actions
    def modify_rates_tile(self, from_cur: str, to_cur: str, tenor: str, qty: str = None, settle_date: int = None,
                          single_venue: str = None, venue_list: list = None, ):
        """
        Func for modifying rates tile, from_cur, to_cur, tenor is mandatory parameters, other not.
        Param settle_date  must be set to the number of days until which you want to go, for example -
        if you want to set tomorrow you need to set 1
        """
        self.modify_request.set_instrument(from_cur, to_cur, tenor)
        if qty is not None:
            self.modify_request.set_quantity(qty)
        if settle_date is not None:
            self.modify_request.set_settlement_date(bca.get_t_plus_date(settle_date))
        if single_venue is not None:
            action = self.context_action.create_venue_filter(single_venue)
            self.modify_request.add_context_action(action)
        if venue_list is not None:
            action = self.context_action.create_venue_filters(venue_list)
            self.modify_request.add_context_action(action)
        call(self.ar_service.modifyRatesTile, self.modify_request.build())
        self.clear_details([self.modify_request])

    def add_aggregated_rates(self):
        """
        RMC on ESP tile and select Aggregated rates from list
        """
        action = self.context_action.add_aggregated_rates(details=self.base_details)
        self.modify_request.add_context_action(action)
        call(self.ar_service.modifyRatesTile, self.modify_request.build())
        self.clear_details([self.modify_request])

    # region Direct Venue Execution
    def open_direct_venue(self, single_venue: str = None, venue_list: list = None):
        """
        RMC on ESP tile and select Direct Venue Execution from list and if venue_list
        or single_venue not None add filter by single venue or venue list
        """
        action = self.context_action.open_direct_venue_panel()
        if single_venue is not None:
            venue_filter = self.context_action.create_venue_filter(single_venue)
            self.modify_request.add_context_actions([action, venue_filter])
        elif venue_list is not None:
            venue_filter = self.context_action.create_venue_filters(venue_list)
            self.modify_request.add_context_actions([action, venue_filter])
        else:
            self.modify_request.add_context_action(action)
        call(self.ar_service.modifyRatesTile, self.modify_request.build())
        self.clear_details([self.modify_request])

    def click_on_venue_bid(self, venue: str):
        """
        Before using this func you need use open_direct_venue func and select venue from list
        This func click on venue from Direct Venue Execution list on bid button
        """
        click_to_venue = self.action_rates_tile.click_to_bid_esp_order(venue)
        self.modify_request.add_action(click_to_venue)
        call(self.ar_service.modifyRatesTile, self.modify_request.build())

    def click_on_venue_ask(self, venue: str):
        """
        Before using this func you need use open_direct_venue func and select venue from list
        This func click on venue from Direct Venue Execution list on ask button
        """
        click_to_venue = self.action_rates_tile.click_to_ask_esp_order(venue)
        self.modify_request.add_action(click_to_venue)
        call(self.ar_service.modifyRatesTile, self.modify_request.build())

    def add_row_to_direct_venue(self, venue: str, row_count: int):
        """
        Before using this func you need use open_direct_venue func and select venue from list
        """
        add_row = self.action_rates_tile.click_to_direct_venue_add_raw(venue)
        for _ in range(row_count):
            self.modify_request.add_action(add_row)
        call(self.ar_service.modifyRatesTile, self.modify_request.build())

    # endregion

    def add_full_amount(self, qty: list):
        """
        RMC on ESP tile and select Full Amount from list and after add Full Amount Qty
        """
        open_full_amount = self.context_action.open_full_amount()
        self.modify_request.add_context_action(open_full_amount)
        for i in qty:
            add_full_qty = self.context_action.add_full_amount_qty(i)
            self.modify_request.add_context_actions([add_full_qty])
        call(self.ar_service.modifyRatesTile, self.modify_request.build())
        self.clear_details([self.modify_request])

    def click_on_tob_buy(self):
        """
        Click on Top of Book Buy side on ESP tile
        """
        self.place_order_request.set_action(ESPTileOrderSide.BUY)
        self.place_order_request.top_of_book()
        call(self.ar_service.placeESPOrder, self.place_order_request.build())

    def click_on_tob_sell(self):
        """
        Click on Top of Book Sell side on ESP tile
        """
        self.place_order_request.set_action(ESPTileOrderSide.SELL)
        self.place_order_request.top_of_book()
        call(self.ar_service.placeESPOrder, self.place_order_request.build())

    def click_on_bid_btn(self):
        """
        Click on bid button on ESP tile
        """
        self.place_order_request.set_action(ESPTileOrderSide.BUY)
        call(self.ar_service.placeESPOrder, self.place_order_request.build())

    def click_on_ask_btn(self):
        """
        Click on ask button on ESP tile
        """
        self.place_order_request.set_action(ESPTileOrderSide.SELL)
        call(self.ar_service.placeESPOrder, self.place_order_request.build())
    # endregion
