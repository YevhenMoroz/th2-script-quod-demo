from datetime import datetime
import timestring
from custom.verifier import Verifier
from test_framework.win_gui_wrappers.forex.aggregates_rates_tile import AggregatesRatesTile
from win_gui_modules.aggregated_rates_wrappers import ModifyRFQTileRequest, ContextAction, PlaceRFQRequest, \
    RFQTileOrderSide, ExtractRFQTileValues
from custom import basic_custom_actions as bca
from win_gui_modules.utils import call


class RFQTile(AggregatesRatesTile):
    def __init__(self, case_id, session_id, index: int = 0):
        super().__init__(case_id, session_id, index)
        self.modify_request = ModifyRFQTileRequest(details=self.base_details)
        self.place_order_request = PlaceRFQRequest(details=self.base_details)
        self.extraction_request = ExtractRFQTileValues(details=self.base_details)
        self.create_tile_call = self.ar_service.createRFQTile
        self.close_tile_call = self.ar_service.closeRFQTile
        self.close_window_call = self.ar_service.closeWindow
        self.extract_call = self.ar_service.extractRFQTileValues
        self.set_default_params()

    def set_default_params(self):
        self.verifier = Verifier(self.case_id)
        self.extraction_request.set_extraction_id(self.extraction_id)
        self.extraction_request = ExtractRFQTileValues(details=self.base_details)

    # region Actions
    def modify_rfq_tile(self, from_cur: str = None, to_cur: str = None, near_qty: str = None, far_qty: str = None,
                        near_tenor: str = None, far_tenor: str = None, client: str = None,
                        near_maturity_date: int = None, far_maturity_date: int = None, left_check: bool = False,
                        near_date: int = None, far_date: int = None, right_check: bool = False,
                        single_venue: str = None, venue_list: list = None, change_currency: bool = False,
                        clear_far_tenor: bool = False):
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
            self.modify_request.set_maturity_date(bca.get_t_plus_date(near_maturity_date, is_weekend_holiday=False))
        if far_maturity_date is not None:
            self.modify_request.set_maturity_date(bca.get_t_plus_date(far_maturity_date, is_weekend_holiday=False))
        if near_date is not None:
            self.modify_request.set_settlement_date(bca.get_t_plus_date(near_date, is_weekend_holiday=False))
        if far_date is not None:
            self.modify_request.set_far_leg_settlement_date(bca.get_t_plus_date(far_date, is_weekend_holiday=False))
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
        if change_currency is not False:
            self.modify_request.set_change_currency(change_currency)
        if clear_far_tenor is not False:
            self.modify_request.clear_far_leg_tenor(clear_far_tenor)
        call(self.ar_service.modifyRFQTile, self.modify_request.build())
        self.clear_details([self.modify_request])
        self.set_default_params()

    def send_rfq(self):
        call(self.ar_service.sendRFQOrder, self.base_details.build())

    def place_order(self, side: str, venue: str = None):
        if venue is not None:
            self.place_order_request.set_venue(venue)
        if side == self.sell_side:
            self.place_order_request.set_action(RFQTileOrderSide.SELL)
        if side == self.buy_side:
            self.place_order_request.set_action(RFQTileOrderSide.BUY)
        call(self.ar_service.placeRFQOrder, self.place_order_request.build())
        self.clear_details([self.place_order_request])
        self.set_default_params()

    def cancel_rfq(self):
        call(self.ar_service.cancelRFQ, self.base_details.build())

    # endregion

    # region Extraction
    def check_currency_pair(self, currency_pair: str = None):
        self.verifier.set_event_name("Check currency pair")
        self.extraction_request.extract_currency_pair(currency_pair)
        response = call(self.extract_call, self.extraction_request.build())
        extract_currency_pair = response[currency_pair]
        self.verifier.compare_values("Currency pair", currency_pair, extract_currency_pair)
        self.verifier.verify()
        self.clear_details([self.extraction_request])
        self.set_default_params()

    def check_currency(self, currency: str = None):
        self.verifier.set_event_name("Check currency")
        self.extraction_request.extract_currency(currency)
        response = call(self.extract_call, self.extraction_request.build())
        extract_currency = response[currency]
        self.verifier.compare_values("Currency", currency, extract_currency)
        self.verifier.verify()
        self.clear_details([self.extraction_request])
        self.set_default_params()

    def check_qty(self, near_qty: str = None, far_qty: str = None):
        self.verifier.set_event_name("Check Qty")
        if near_qty is not None:
            self.extraction_request.extract_quantity(near_qty)
            response = call(self.extract_call, self.extraction_request.build())
            extract_qty = response[near_qty].replace(',', '')[:-3]
            self.verifier.compare_values("Near Qty", near_qty, extract_qty)

        if far_qty is not None:
            self.extraction_request.extract_far_leg_qty(far_qty)
            response = call(self.extract_call, self.extraction_request.build())
            extract_qty = response[far_qty].replace(',', '')[:-3]
            self.verifier.compare_values("Far Qty", far_qty, extract_qty)
        self.verifier.verify()
        self.clear_details([self.extraction_request])
        self.set_default_params()

    def check_tenor(self, near_tenor: str = None, far_tenor: str = None):
        self.verifier.set_event_name("Check tenor")
        if near_tenor is not None:
            self.extraction_request.extract_tenor(near_tenor)
            response = call(self.extract_call, self.extraction_request.build())
            extract_tenor = response[near_tenor]
            self.verifier.compare_values("Near tenor", near_tenor, extract_tenor)
        if far_tenor is not None:
            self.extraction_request.extract_far_leg_tenor(far_tenor)
            response = call(self.extract_call, self.extraction_request.build())
            extract_tenor = response[far_tenor]
            self.verifier.compare_values("Far tenor", far_tenor, extract_tenor)
        self.verifier.verify()
        self.clear_details([self.extraction_request])
        self.set_default_params()

    def check_date(self, near_date: str = None, far_date: str = None):
        self.verifier.set_event_name("Check date")
        if near_date is not None:
            self.extraction_request.extract_near_settlement_date(near_date)
            response = call(self.extract_call, self.extraction_request.build())
            extract_date = response[near_date]
            extract_date = str(timestring.Date(extract_date))
            self.verifier.compare_values("Near date", near_date, extract_date)
        if far_date is not None:
            self.extraction_request.extract_far_leg_settlement_date(far_date)
            response = call(self.extract_call, self.extraction_request.build())
            extract_date = response[far_date]
            extract_date = str(timestring.Date(extract_date))
            self.verifier.compare_values("Far date", far_date, extract_date)
        self.verifier.verify()
        self.clear_details([self.extraction_request])
        self.set_default_params()

    def check_diff(self, near_date: str = None, far_date: str = None):
        self.verifier.set_event_name("Check diff")
        dif = str(datetime.strptime(far_date, '%Y-%m-%d %H:%M:%S') - datetime.strptime(near_date,
                                                                                       '%Y-%m-%d %H:%M:%S'))[:6]
        self.extraction_request.extract_swap_diff_days(dif)
        response = call(self.extract_call, self.extraction_request.build())
        extracted_diff = response[dif]
        self.verifier.compare_values("Difference", dif, extracted_diff)
        self.verifier.verify()
        self.clear_details([self.extraction_request])
        self.set_default_params()

    def check_client_beneficiary(self, client: str = None, beneficiary: str = None):
        self.verifier.set_event_name("Check Client and Beneficiary")
        if client is not None:
            self.extraction_request.extract_client(client)
            response = call(self.extract_call, self.extraction_request.build())
            extracted_client = response[client]
            self.verifier.compare_values("Client", client, extracted_client)
        if beneficiary is not None:
            self.extraction_request.extract_beneficiary(beneficiary)
            response = call(self.extract_call, self.extraction_request.build())
            extracted_beneficiary = response[beneficiary]
            self.verifier.compare_values("Client", beneficiary, extracted_beneficiary)
        self.verifier.verify()
        self.clear_details([self.extraction_request])
        self.set_default_params()

    def extract_price(self, bid_large: str = None, bid_small: str = None, ask_large: str = None, ask_small: str = None,
                      best_bid: str = None, best_ask: str = None):
        if bid_large is not None:
            self.extraction_request.extract_best_bid_large(bid_large)
        if bid_small is not None:
            self.extraction_request.extract_best_bid_small(bid_small)
        if ask_large is not None:
            self.extraction_request.extract_best_ask_large(ask_large)
        if ask_small is not None:
            self.extraction_request.extract_best_ask_small(ask_small)
        if best_bid is not None:
            self.extraction_request.extract_best_bid(best_bid)
        if best_ask is not None:
            self.extraction_request.extract_best_ask(best_ask)
        response = call(self.extract_call, self.extraction_request.build())
        self.clear_details([self.extraction_request])
        self.set_default_params()
        return response

    def check_checkboxes(self, left_checkbox: str = None, right_checkbox: str = None):
        self.verifier.set_event_name("Check checkboxes")
        if left_checkbox is not None:
            self.extraction_request.extract_left_checkbox(left_checkbox)
            response = call(self.extract_call, self.extraction_request.build())
            lef_check = response[left_checkbox]
            self.verifier.compare_values("Left Checkbox", left_checkbox, lef_check)
        if right_checkbox is not None:
            self.extraction_request.extract_right_checkbox(right_checkbox)
            response = call(self.extract_call, self.extraction_request.build())
            right_check = response[right_checkbox]
            self.verifier.compare_values("Right Checkbox", right_checkbox, right_check)
        self.verifier.verify()
        self.clear_details([self.extraction_request])
        self.set_default_params()

    def check_labels(self, left_label: str = None, right_label: str = None):
        self.verifier.set_event_name("Check labels")
        if left_label is not None:
            self.extraction_request.extract_cur_label_left(left_label)
            response = call(self.extract_call, self.extraction_request.build())
            left = response[left_label]
            self.verifier.compare_values("Left label", left_label, left)
        if right_label is not None:
            self.extraction_request.extract_cur_label_right(right_label)
            response = call(self.extract_call, self.extraction_request.build())
            right = response[right_label]
            self.verifier.compare_values("Right label", right_label, right)
        self.verifier.verify()
        self.clear_details([self.extraction_request])
        self.set_default_params()

    def check_buttons(self, buy_button: str = None, sell_button: str = None, send_button: str = None):
        self.verifier.set_event_name("Check buttons")
        if buy_button is not None:
            self.extraction_request.extract_is_buy_button_enabled(buy_button)
            response = call(self.extract_call, self.extraction_request.build())
            buy = response[buy_button]
            self.verifier.compare_values("Buy button", buy_button, buy)
        if sell_button is not None:
            self.extraction_request.extract_is_sell_button_enabled(sell_button)
            response = call(self.extract_call, self.extraction_request.build())
            sell = response[sell_button]
            self.verifier.compare_values("Sell button", sell_button, sell)
        if send_button is not None:
            self.extraction_request.extract_send_button_text(send_button)
            response = call(self.extract_call, self.extraction_request.build())
            send = response[send_button]
            self.verifier.compare_values("Send button", send_button, send)
        self.verifier.verify()
        self.clear_details([self.extraction_request])
        self.set_default_params()

        # endregion
