from test_cases.web_admin.web_admin_core.pages.common_page import CommonPage
from test_cases.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer


class OrderBookPage(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    # TODO: implement methods, if something changed in FE part, please take a look

    # region Filter values in main page
    def get_symbol(self):
        pass

    def get_instr_type(self):
        pass

    def get_order_id(self):
        pass

    def get_account_code(self):
        pass

    def get_side(self):
        pass

    def get_order_qty(self):
        pass

    def get_price(self):
        pass

    def get_avg_price(self):
        pass

    def get_leaves_qty(self):
        pass

    def get_order_type(self):
        pass

    def get_cum_qty(self):
        pass

    def get_order_status(self):
        pass

    def get_expire_date(self):
        pass

    def get_settle_date(self):
        pass

    def get_settle_type(self):
        pass

    def get_time_in_force(self):
        pass

    def get_free_notes(self):
        pass

    def get_account(self):
        pass

    def get_transaction_time(self):
        pass

    def get_cl_ord_id(self):
        pass

    # endregion

    def click_on_field_chooser_button(self):
        pass

    def select_visible_columns(self, value):
        pass

    def click_on_hide_all(self):
        pass

    def click_on_show_all(self):
        pass

    # region order filter switch
    def click_on_switch_at_order_filter(self):
        pass

    def set_from_date(self, date):
        pass

    def set_to_date(self, date):
        pass

    def click_on_search_button(self):
        pass

    # endregion

    # region Auxiliary menu on the symbol

    def click_on_buy_button(self):
        pass

    def click_on_sell_button(self):
        pass

    def click_on_remove_button(self):
        pass

    def click_on_modify_button(self):
        pass

    def click_on_market_depth_button(self):
        pass

    def click_on_times_and_sales_button(self):
        pass

    def click_on_order_cancel_button(self):
        pass

    def click_on_re_order_button(self):
        pass
# endregion
