from test_framework.win_gui_wrappers.fe_trading_constant import Side
from test_framework.win_gui_wrappers.forex.client_pricing_tile import ClientPricingTile
from win_gui_modules.client_pricing_wrappers import ModifyClientRFQTileRequest, ClientRFQTileOrderDetails
from win_gui_modules.utils import call


class ClientRFQTile(ClientPricingTile):
    def __init__(self, case_id, session_id, index: int = 0):
        super().__init__(case_id, session_id, index)
        self.modify_request = ModifyClientRFQTileRequest(data=self.base_data)
        self.place_order_request = ClientRFQTileOrderDetails(data=self.base_data)
        self.create_tile_call = self.cp_service.createClientRFQTile
        self.close_tile_call = self.cp_service.closeClientRFQTile
        self.modify_call = self.cp_service.modifyRFQTile
        self.send_call = self.cp_service.sendRFQOrder
        self.place_order_call = self.cp_service.placeClientRFQOrder

    def modify_rfq_tile(self, from_cur: str = None, to_cur: str = None, near_qty: str = None, far_qty: str = None,
                        near_tenor: str = None, far_tenor: str = None, client: str = None,
                        clientTier: str = None, change_currency: bool = False):
        if from_cur is not None:
            self.modify_request.set_from_curr(from_cur)
        if to_cur is not None:
            self.modify_request.set_to_curr(to_cur)
        if near_qty is not None:
            self.modify_request.change_near_leg_qty(near_qty)
        if far_qty is not None:
            self.modify_request.change_far_leg_qty(far_qty)
        if near_tenor is not None:
            self.modify_request.change_near_tenor(near_tenor)
        if far_tenor is not None:
            self.modify_request.change_far_tenor(far_tenor)
        if client is not None:
            self.modify_request.change_client(client)
        if change_currency is not False:
            self.modify_request.change_currency(change_currency)
        if clientTier is not None:
            self.modify_request.change_client_tier(clientTier)

        call(self.cp_service.modifyRFQTile, self.modify_request.build())
        self.clear_details([self.modify_request])

    def send_rfq(self):
        call(self.send_call, self.base_data)

    def place_order(self, side: Side):
        if side is Side.sell:
            self.place_order_request.set_action_sell()
        if side is Side.buy:
            self.place_order_request.set_action_buy()
        call(self.place_order_call, self.place_order_request.build())
        self.clear_details([self.place_order_request])
