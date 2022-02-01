from test_cases.web_admin.web_admin_core.pages.common_page import CommonPage
from test_cases.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer


class PositionsPage(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    # TODO: implement methods, if something changed in FE part, please take a look
    # region Filter values in main page
    def get_symbol(self):
        pass

    def get_instr_type(self):
        pass

    def get_exchange(self):
        pass

    def get_total_qty(self):
        pass

    def get_reserved_qty(self):
        pass

    def get_covered_qty(self):
        pass

    def get_leaves_buy_qty(self):
        pass

    def get_leaves_sell_qty(self):
        pass

    def get_cumulative_buy_amt(self):
        pass

    def get_cumulative_sell_amt(self):
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

    def click_on_copy_panel(self):
        pass

    def click_on_maximize_button(self):
        pass

    def click_on_minimize_button(self):
        pass

    def click_on_close_positions_wizard(self):
        pass
