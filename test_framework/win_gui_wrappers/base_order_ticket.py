from test_framework.win_gui_wrappers.base_window import BaseWindow
from win_gui_modules.utils import call


class BaseOrderTicket(BaseWindow):
    # region Base constructor
    def __init__(self, case_id, session_id):
        super().__init__(case_id, session_id)
        # Need to override
        self.order_details = None
        self.new_order_details = None
        self.modify_order_details = None
        self.modify_order_details = None
        self.extract_order_ticket_values_request = None
        self.extract_order_ticket_errors_request = None
        self.order_ticket_extracted_value = None
        self.base_tile_data = None
        self.place_order_call = None
        self.amend_order_call = None
        self.split_limit_order_call = None
        self.split_order_call = None
        self.child_care_order_call = None
        self.re_order_leaves_call = None
        self.open_order_ticket_by_double_click_call = None
        self.re_order_call = None
        self.extract_order_ticket_values_call = None
        self.extract_order_ticket_errors_call = None
        self.mass_modify_order_call = None

    # endregion

    # region Set
    def set_order_details(self, client=None, limit=None, stop_price=None, qty=None, order_type=None,
                          tif=None, account=None, display_qty=None, is_sell_side=False, instrument=None):

        if client is not None:
            self.order_details.set_client(client)
        if qty is not None:
            self.order_details.set_quantity(qty)
        if order_type is not None:
            self.order_details.set_order_type(order_type)
        if is_sell_side:
            self.order_details.sell()
        if tif is not None:
            self.order_details.set_tif(tif)
        if limit is not None:
            self.order_details.set_limit(limit)
        if stop_price is not None:
            self.order_details.set_stop_price(stop_price)
        if account is not None:
            self.order_details.set_account(account)
        if display_qty is not None:
            self.order_details.set_display_qty(display_qty)
        return self.order_details

    def set_twap_details(self, strategy_type, start_date=None, start_date_offset="", end_date=None,
                         end_date_offset="", waves=None, aggressivity=None, max_participation=None,
                         slice_duration_min=None, child_display_qty=None, child_min_qty=None):
        twap_details = self.order_details.add_twap_strategy(strategy_type)
        if start_date is not None:
            twap_details.set_start_date(start_date, start_date_offset)
        if end_date is not None:
            twap_details.set_end_date(end_date, end_date_offset)
        if waves is not None:
            twap_details.set_waves(waves)
        if aggressivity is not None:
            twap_details.set_aggressivity(aggressivity)
        if max_participation is not None:
            twap_details.set_max_participation(max_participation)
        if slice_duration_min is not None:
            twap_details.set_slice_duration_min(slice_duration_min)
        if child_display_qty is not None:
            twap_details.set_child_display_qty(child_display_qty)
        if child_min_qty is not None:
            twap_details.set_child_min_qty(child_min_qty)
        return self.order_details

    def set_external_twap_details(self, strategy_type, urgency=None, start_time=None, end_time=None):
        """
        works with MS TWAP(ASIA), MS TWAP(AMERICAS), MS TWAP(EMEA)
        """
        details = self.order_details.add_external_twap_strategy(strategy_type)
        if urgency is not None:
            details.set_urgency(urgency)
        if start_time is not None:
            details.set_start_time(start_time)
        if end_time is not None:
            details.set_end_time(end_time)
        return self.order_details

    def set_synthetic_iceberg_details(self, strategy_type, low_liquidity: bool = False):
        details = self.order_details.add_synthetic_iceberg_strategy(strategy_type)
        details.set_low_liquidity(low_liquidity)

    def set_synthetic_block_details(self, strategy_type, order_mode: str = None):
        details = self.order_details.add_synthetic_block_strategy(strategy_type)
        if not None:
            details.set_order_mode(order_mode)

    # endregion
    # region Get
    def extract_order_ticket_errors(self):
        extract_errors_request = self.extract_order_ticket_errors_request
        extract_errors_request.extract_error_message()
        result = call(self.extract_order_ticket_errors_call, extract_errors_request.build())
        return result

    # endregion
    # region Check
    def check_availability(self, name_list: list):
        for name in name_list:
            field = getattr(self.order_ticket_extracted_value, name)
            self.extract_order_ticket_values_request.get_extract_value(field, name)
        result = call(self.extract_order_ticket_values_call, self.extract_order_ticket_values_request.build())
        return result

    # endregion
    # region Actions
    def create_order(self, lookup=None):
        if lookup is not None:
            self.new_order_details.set_lookup_instr(lookup)
        self.new_order_details.set_order_details(self.order_details)
        call(self.place_order_call, self.new_order_details.build())
        self.clear_details([self.new_order_details, self.order_details])

    def re_order(self):
        self.new_order_details.set_order_details(self.order_details)
        call(self.re_order_call, self.new_order_details.build())
        self.clear_details([self.new_order_details])

    def re_order_leaves(self):
        self.new_order_details.set_order_details(self.order_details)
        call(self.re_order_leaves_call, self.new_order_details.build())
        self.clear_details([self.new_order_details])

    def amend_order(self, filter_list: list = None):
        self.modify_order_details.set_order_details(self.order_details)
        if filter_list is not None:
            self.modify_order_details.set_filter(filter_list)
        call(self.amend_order_call, self.modify_order_details.build())
        self.clear_details([self.modify_order_details])

    def mass_modify_order(self, row_count: int, filter_list: list = None):
        self.modify_order_details.set_order_details(self.order_details)
        self.modify_order_details.set_selected_row_count(row_count)
        if filter_list is not None:
            self.modify_order_details.set_filter(filter_list)
        call(self.mass_modify_order_call, self.modify_order_details.build())
        self.clear_details([self.modify_order_details])

    def split_order(self, filter_list: list = None):
        self.modify_order_details.set_order_details(self.order_details)
        if filter_list is not None:
            self.modify_order_details.set_filter(filter_list)
        call(self.split_order_call, self.modify_order_details.build())
        self.clear_details([self.modify_order_details])

    def split_limit_order(self, filter_list: list = None):
        self.modify_order_details.set_order_details(self.order_details)
        if filter_list is not None:
            self.modify_order_details.set_filter(filter_list)
        call(self.split_limit_order_call, self.modify_order_details.build())
        self.clear_details([self.modify_order_details])

    def child_care(self, filter_list: list = None):
        self.modify_order_details.set_order_details(self.order_details)
        if filter_list is not None:
            self.modify_order_details.set_filter(filter_list)
        call(self.child_care_order_call, self.modify_order_details.build())
        self.clear_details([self.modify_order_details])

    def open_order_ticket_by_double_click(self, filter_list: list = None):
        self.modify_order_details.set_order_details(self.order_details)
        if filter_list is not None:
            self.modify_order_details.set_filter(filter_list)
        call(self.open_order_ticket_by_double_click_call, self.modify_order_details.build())
        self.clear_details([self.modify_order_details])
    # endregion
