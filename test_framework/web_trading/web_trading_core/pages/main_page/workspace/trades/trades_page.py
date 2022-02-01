from test_cases.web_admin.web_admin_core.pages.common_page import CommonPage
from test_cases.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer


class TradesPage(CommonPage):
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

    def get_excel_id(self):
        pass

    def get_side(self):
        pass

    def get_qty(self):
        pass

    def get_execution_price(self):
        pass

    def get_execution_type(self):
        pass

    def get_avg_price(self):
        pass

    def get_cumulative_qty(self):
        pass

    def get_leaves_qty(self):
        pass

    def get_order_status(self):
        pass

    def get_transaction_time(self):
        pass

    # endregion

    # region Visible columns
    def click_on_field_chooser_button(self):
        pass

    def select_visible_columns(self, value):
        pass

    def click_on_hide_all(self):
        pass

    def click_on_show_all(self):
        pass

    # endregion

    # region Advanced filtering
    def click_on_advanced_filtering_button(self):
        pass

    # endregion

    def click_on_copy_panel_button(self):
        pass

    def click_on_maximize_button(self):
        pass

    def click_on_minimize_button(self):
        pass

    def click_on_close_watch_list_button(self):
        pass

    # region Auxiliary menu on the symbol

    def click_on_buy_button(self):
        pass

    def click_on_sell_button(self):
        pass

    def click_on_remove_button(self):
        pass

    def click_on_market_depth_button(self):
        pass

    def click_on_times_and_sales_button(self):
        pass
# endregion
