from test_framework.win_gui_wrappers.forex.aggregates_rates_tile import AggregatesRatesTile
from win_gui_modules.aggregated_rates_wrappers import ModifyRatesTileRequest, PlaceESPOrder, ContextActionRatesTile
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

    # region Action
    def modify_rates_tile(self, from_cur: str, to_cur: str, tenor: str, qty: str = None, settle_date: int = None,
                          single_venue: str = None, venue_list: list = None, ):
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
        action = self.context_action.add_aggregated_rates(details=self.base_details)
        self.modify_request.add_context_action(action)
        call(self.ar_service.modifyRatesTile, self.modify_request.build())
        self.clear_details([self.modify_request])

    def open_direct_venue(self):
        action = self.context_action.open_direct_venue_panel()
        self.modify_request.add_context_action(action)
        call(self.ar_service.modifyRatesTile, self.modify_request.build())
        self.clear_details([self.modify_request])

    def add_full_amount(self, qty: list):
        open_full_amount = self.context_action.open_full_amount()
        self.modify_request.add_context_action(open_full_amount)
        for i in qty:
            add_full_qty = self.context_action.add_full_amount_qty(i)
            self.modify_request.add_context_actions([add_full_qty])
        call(self.ar_service.modifyRatesTile, self.modify_request.build())
        self.clear_details([self.modify_request])
