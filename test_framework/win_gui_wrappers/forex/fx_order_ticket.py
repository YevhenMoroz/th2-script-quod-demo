from th2_grpc_act_gui_quod.common_pb2 import BaseTileData
from th2_grpc_act_gui_quod.order_ticket_pb2 import DiscloseFlagEnum

from stubs import Stubs
from test_framework.win_gui_wrappers.base_order_ticket import BaseOrderTicket
from test_framework.win_gui_wrappers.fe_trading_constant import TriggerType
from win_gui_modules.order_book_wrappers import ReleaseFXOrderDetails, ModifyFXOrderDetails
from win_gui_modules.order_ticket import FXOrderDetails, ExtractFxOrderTicketValuesRequest
from win_gui_modules.order_ticket_wrappers import NewFxOrderDetails
from win_gui_modules.utils import call


class FXOrderTicket(BaseOrderTicket):
    # region Constructor
    def __init__(self, case_id, session_id):
        super().__init__(case_id, session_id)
        self.order_details = FXOrderDetails()
        self.new_order_details = None
        self.base_tile_data = BaseTileData(base=self.base_request)
        self.extract_request = ExtractFxOrderTicketValuesRequest(self.base_tile_data)
        self.release_order_request = ReleaseFXOrderDetails(self.base_request)
        self.place_order_call = Stubs.win_act_order_ticket_fx.placeFxOrder
        self.open_order_ticket_by_double_click_call = Stubs.win_act_order_book_fx.openOrderTicketByDoubleClick
        self.modify_order_details = ModifyFXOrderDetails(self.base_request)
        self.amend_order_call = Stubs.win_act_order_book_fx.amendOrder
        self.extract_call = Stubs.win_act_order_ticket_fx.extractFxOrderTicketValues

    def set_order_details(self, price_large=None, price_small=None, limit=None, qty=None, display_qty=None, client=None,
                          tif=None, slippage=None, stop_price=None, order_type=None, place: bool = None,
                          close: bool = False,
                          pending: bool = None, keep_open: bool = None, custom_algo=None,
                          custom_algo_check_box: bool = None,
                          strategy=None, child_strategy=None, click_pips: int = None, click_qty: int = None,
                          click_slippage: int = None, click_stop_price: int = None, click_display_qty: int = None,
                          desk=None,
                          partial_desc: bool = None, disclose_flag: DiscloseFlagEnum = None,
                          add_multilisting_strategy=None,
                          add_twap_strategy=None, expire_time: str = None):
        if price_large is not None:
            self.order_details.set_price_large(str(price_large))
        if price_small is not None:
            self.order_details.set_price_pips(str(price_small))
        if limit is not None:
            self.order_details.set_limit(str(limit))
        if qty is not None:
            self.order_details.set_qty(str(qty))
        if display_qty is not None:
            self.order_details.set_display_qty(str(display_qty))
        if client is not None:
            self.order_details.set_client(client)
        if tif is not None:
            self.order_details.set_tif(tif)
        if slippage is not None:
            self.order_details.set_slippage(str(slippage))
        if expire_time is not None:
            self.order_details.set_expire_date(expire_time)
        if stop_price is not None:
            self.order_details.set_stop_price(str(stop_price))
        if order_type is not None:
            self.order_details.set_order_type(order_type)
        if place is not None:
            self.order_details.set_place(place)
        if close is True:
            self.order_details.set_close()
        if pending is not None:
            self.order_details.set_pending(pending)
        if keep_open is not None:
            self.order_details.set_keep_open(keep_open)
        if custom_algo is not None:
            self.order_details.set_custom_algo(custom_algo)
        if custom_algo_check_box is not None:
            self.order_details.set_custom_algo_check_box(custom_algo_check_box)
        if strategy is not None:
            self.order_details.set_strategy(strategy)
        if child_strategy is not None:
            self.order_details.set_child_strategy(child_strategy)
        if click_pips is not None:
            self.order_details.click_pips(click_pips)
        if click_qty is not None:
            self.order_details.click_qty(click_qty)
        if click_slippage is not None:
            self.order_details.click_slippage(click_slippage)
        if click_stop_price is not None:
            self.order_details.click_stop_price(click_stop_price)
        if click_display_qty is not None:
            self.order_details.click_display_qty(click_display_qty)
        if desk is not None:
            self.order_details.set_care_order(desk)
        if desk is not None and disclose_flag is not None:
            self.order_details.set_care_order(desk, disclose_flag)
        if desk is not None and partial_desc is not None:
            self.order_details.set_care_order(desk, partial_desc)
        if desk is not None and partial_desc is not None and disclose_flag is not None:
            self.order_details.set_care_order(desk, partial_desc, disclose_flag)
        if add_multilisting_strategy is not None:
            self.order_details.add_multilisting_strategy(add_multilisting_strategy)
        if add_twap_strategy is not None:
            self.order_details.add_twap_strategy(add_twap_strategy)
        if add_synth_ord_type_str is not None:
            self.order_details.add_synthetic_strategy()
        return self

    def add_synth_ord_type_str(self, trigger_type: TriggerType):
        synthetic = self.order_details.add_synthetic_strategy()
        if trigger_type is TriggerType.last_trade:
            synthetic.set_trigger_type(trigger_type.value)
        if trigger_type is TriggerType.market_best_bid_offer:
            synthetic.set_trigger_type(trigger_type.value)
        if trigger_type is TriggerType.primary_best_bid_offer:
            synthetic.set_trigger_type(trigger_type.value)
        return self

    def create_order(self, lookup=None, is_mm: bool = False):
        self.order_details.set_place()
        self.new_order_details = NewFxOrderDetails(self.base_request, self.order_details, isMM=is_mm)
        call(self.place_order_call, self.new_order_details.build())
        self.clear_details([self.order_details])

    def extract_order_ticket_errors(self):
        self.extract_request.get_error_message_text("errorMsg")
        response = call(self.extract_call, self.extract_request.build())
        return response["errorMsg"]
