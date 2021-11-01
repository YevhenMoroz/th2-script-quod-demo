from quod_qa.win_gui_wrappers.forex.aggregates_rates_tile import AggregatesRatesTile
from win_gui_modules.aggregated_rates_wrappers import ModifyRFQTileRequest, ContextAction, PlaceRFQRequest, \
    RFQTileOrderSide
from custom import basic_custom_actions as bca
from win_gui_modules.utils import call


class RFQTile(AggregatesRatesTile):
    def __init__(self, case_id, base_request, index: int = 0):
        super().__init__(case_id, base_request, index)
        self.modify_request = ModifyRFQTileRequest(details=self.base_details)
        self.place_order_request = PlaceRFQRequest(details=self.base_details)

    # region Actions
    def modify_rfq_tile(self, from_cur: str = None, to_cur: str = None, near_qty: str = None, far_qty: str = None,
                        near_tenor: str = None, far_tenor: str = None, client: str = None,
                        near_maturity_date: int = None, far_maturity_date: int = None, left_check: bool = False,
                        near_date: int = None, far_date: int = None, right_check: bool = False,
                        single_venue: str = None, venue_list: list = None):
        if from_cur is not None:
            self.modify_request.set_from_currency(from_cur)
        if to_cur is not None:
            self.modify_request.set_to_currency(to_cur)
        if near_qty is not None:
            self.modify_request.set_quantity_as_string(near_qty)
        if far_qty is not None:
            self.modify_request.set_far_leg_quantity_as_string(far_qty)
        if near_tenor is not None:
            self.modify_request.set_near_tenor(near_tenor)
        if far_tenor is not None:
            self.modify_request.set_far_leg_tenor(far_tenor)
        if client is not None:
            self.modify_request.set_client(client)
        if near_maturity_date is not None:
            self.modify_request.set_maturity_date(bca.get_t_plus_date(near_maturity_date))
        if far_maturity_date is not None:
            self.modify_request.set_maturity_date(bca.get_t_plus_date(far_maturity_date))
        if near_date is not None:
            self.modify_request.set_settlement_date(bca.get_t_plus_date(near_date))
        if far_date is not None:
            self.modify_request.set_far_leg_settlement_date(bca.get_t_plus_date(far_date))
        if single_venue is not None:
            action = ContextAction.create_venue_filter(single_venue)
            self.modify_request.add_context_action(action)
        if venue_list is not None:
            action = ContextAction.create_venue_filters(venue_list)
            self.modify_request.add_context_action(action)
        if left_check is not False:
            self.modify_request.click_checkbox_left()
        if right_check is not False:
            self.modify_request.click_checkbox_right()
        call(self.ar_service.modifyRFQTile, self.modify_request.build())

    def send_rfq(self):
        call(self.ar_service.sendRFQOrder, self.base_details.build())

    def place_order(self, side: str = None, venue: str = None):
        if venue is not None:
            self.place_order_request.set_venue(venue)
        if side == self.sell_side:
            self.place_order_request.set_action(RFQTileOrderSide.SELL)
        if side == self.buy_side:
            self.place_order_request.set_action(RFQTileOrderSide.BUY)
        call(self.ar_service.placeRFQOrder, self.place_order_request.build())

    def cancel_rfq(self):
        call(self.ar_service.cancelRFQ, self.base_details.build())
    # endregion
