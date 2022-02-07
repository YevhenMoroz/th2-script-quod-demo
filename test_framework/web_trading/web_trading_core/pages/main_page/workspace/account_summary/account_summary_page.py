from test_cases.web_admin.web_admin_core.pages.common_page import CommonPage
from test_cases.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer


class AccountSummaryPage(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    # TODO: implement methods, if something changed in FE part, please take a look

    # region Filter values in main page
    def get_cash_account(self):
        pass

    def get_currency(self):
        pass

    def get_available_cash(self):
        pass

    def get_transaction_holding_amount(self):
        pass

    def get_reserved_amount(self):
        pass

    def get_buying_power(self):
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

    def click_on_close_button(self):
        pass
