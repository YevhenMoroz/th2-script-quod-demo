from test_cases.web_admin.web_admin_core.pages.positions.wash_books.wash_books_constants import WashBookConstants
from test_cases.web_admin.web_admin_core.pages.common_page import CommonPage
from test_cases.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer


class WashBookRoutesSubWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    # region ~~ROUTES~~
    def click_on_plus_button(self):
        self.find_by_xpath(WashBookConstants.PLUS_AT_ROUTES_TAB).click()

    def click_on_checkmark(self):
        self.find_by_xpath(WashBookConstants.CHECKMARK_AT_ROUTES_TAB).click()

    def click_on_cancel(self):
        self.find_by_xpath(WashBookConstants.CANCEL_AT_ROUTES_TAB).click()

    def click_on_edit(self):
        self.find_by_xpath(WashBookConstants.EDIT_AT_ROUTES_TAB).click()

    def click_on_delete(self):
        self.find_by_xpath(WashBookConstants.DELETE_AT_ROUTES_TAB).click()

    # set and get

    def set_default_route(self, value):
        self.set_combobox_value(WashBookConstants.DEFAULT_ROUTE_AT_ROUTES_TAB, value)

    def get_default_route(self):
        return self.get_text_by_xpath(WashBookConstants.DEFAULT_ROUTE_AT_ROUTES_TAB)

    def set_route_account_name(self, value):
        self.set_text_by_xpath(WashBookConstants.ROUTE_ACCOUNT_NAME_AT_ROUTES_TAB, value)

    def get_route_account_name(self):
        return self.get_text_by_xpath(WashBookConstants.ROUTE_ACCOUNT_NAME_AT_ROUTES_TAB)

    def set_route(self, value):
        self.set_combobox_value(WashBookConstants.ROUTE_AT_ROUTES_TAB, value)

    def get_route(self):
        return self.get_text_by_xpath(WashBookConstants.ROUTE_AT_ROUTES_TAB)

    # filters

    def set_route_account_name_filter(self, value):
        self.set_text_by_xpath(WashBookConstants.ROUTE_ACCOUNT_NAME_FILTER_AT_ROUTES_TAB, value)

    def set_route_filter(self, value):
        self.set_text_by_xpath(WashBookConstants.ROUTE_FILTER_AT_ROUTES_TAB, value)

    # endregion
