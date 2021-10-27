from quod_qa.win_gui_wrappers.base_window import BaseWindow
from win_gui_modules.utils import call


class BaseOrderTicket(BaseWindow):
    def __init__(self, case_id, base_request):
        super().__init__(case_id, base_request)
        # Need to override

        self.order_details = None
        self.new_order_details = None
        self.modify_order_details = None
        self.extract_order_ticket_values_request = None
        self.extract_order_ticket_errors_request = None
        self.order_ticket_extracted_value = None
        self.place_order_call = None
        self.amend_order_call = None
        self.split_limit_order_call = None
        self.split_order_call = None
        self.child_care_order_call = None
        self.re_order_leaves_order_call = None
        self.re_order_order_call = None
        self.extract_order_ticket_values_call = None
        self.extract_order_ticket_errors_call = None
        self.extract_order_ticket_errors_call = None

    def set_order_details(self, client=None, limit=None, stop_price=None, qty=None, order_type=None,
                          tif=None, account=None, display_qty=None, is_sell_side=False):
        order_details = self.order_details
        if client is not None:
            order_details.set_client(client)
        if qty is not None:
            order_details.set_quantity(qty)
        if order_type is not None:
            order_details.set_order_type(order_type)
        if is_sell_side:
            order_details.sell()
        if tif is not None:
            order_details.set_tif(tif)
        if limit is not None:
            order_details.set_limit(limit)
        if stop_price is not None:
            order_details.set_stop_price(stop_price)
        if account is not None:
            order_details.set_account(account)
        if display_qty is not None:
            order_details.set_display_qty(display_qty)
        return order_details

    def create_order(self, order_details):
        self.new_order_details.set_order_details(order_details)
        call(self.place_order_call, self.new_order_details.build())

    def re_order(self, order_details):
        self.new_order_details.set_order_details(order_details)
        call(self.re_order_order_call, self.new_order_details.build())

    def re_order_leaves(self, order_details):
        self.new_order_details.set_order_details(order_details)
        call(self.re_order_leaves_order_call, self.new_order_details.build())

    def amend_order(self, filter_list: list):
        self.modify_order_details.set_order_details(self.order_details)
        self.modify_order_details.set_filter(filter_list)
        call(self.amend_order_call, self.modify_order_details.build())

    def split_order(self, order_details, filter_list: list):
        self.modify_order_details.set_order_details(order_details)
        self.modify_order_details.set_filter(filter_list)
        call(self.split_order_call, self.modify_order_details.build())

    def split_limit_order(self, order_details, filter_list: list):
        self.modify_order_details.set_order_details(order_details)
        self.modify_order_details.set_filter(filter_list)
        call(self.split_limit_order_call, self.modify_order_details.build())

    def child_care(self, order_details, filter_list: list):
        self.modify_order_details.set_order_details(order_details)
        self.modify_order_details.set_filter(filter_list)
        call(self.child_care_order_call, self.modify_order_details.build())

    def check_availability(self, name_list: [str]):
        for name in name_list:
            field = getattr(self.order_ticket_extracted_value, name)
            self.extract_order_ticket_values_request.get_extract_value(field, name)
        result = call(self.extract_order_ticket_values_call, self.extract_order_ticket_values_request.build())
        return result

    def extract_order_ticket_errors(self):
        extract_errors_request = self.extract_order_ticket_errors_request
        extract_errors_request.extract_error_message()
        result = call(self.extract_order_ticket_errors_call, extract_errors_request.build())
        return result
