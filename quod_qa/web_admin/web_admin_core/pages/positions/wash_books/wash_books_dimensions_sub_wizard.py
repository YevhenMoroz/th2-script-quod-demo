from quod_qa.web_admin.web_admin_core.pages.positions.wash_books.wash_books_constants import WashBookConstants
from quod_qa.web_admin.web_admin_core.pages.common_page import CommonPage
from quod_qa.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer


class WashBookDimensionsSubWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    # region ~~DIMENSIONS TAB~~
    def click_on_plus_button(self):
        self.find_by_xpath(WashBookConstants.PLUS_AT_DIMENSIONS_TAB).click()

    def click_on_checkmark(self):
        self.find_by_xpath(WashBookConstants.CHECKMARK_AT_DIMENSIONS_TAB).click()

    def click_on_cancel(self):
        self.find_by_xpath(WashBookConstants.CANCEL_AT_DIMENSIONS_TAB).click()

    def click_on_edit(self):
        self.find_by_xpath(WashBookConstants.EDIT_AT_DIMENSIONS_TAB).click()

    def click_on_delete(self):
        self.find_by_xpath(WashBookConstants.DELETE_AT_DIMENSIONS_TAB).click()

    # set and get
    def set_venue_account(self, value):
        self.set_text_by_xpath(WashBookConstants.VENUE_ACCOUNT_AT_DIMENSIONS_TAB, value)

    def get_venue_account(self):
        return self.get_text_by_xpath(WashBookConstants.VENUE_ACCOUNT_AT_DIMENSIONS_TAB)

    def set_venue(self, value):
        self.set_combobox_value(WashBookConstants.VENUE_AT_AT_DIMENSIONS_TAB, value)

    def get_venue(self):
        return self.get_text_by_xpath(WashBookConstants.VENUE_AT_AT_DIMENSIONS_TAB)

    def set_account_id_source(self, value):
        self.set_combobox_value(WashBookConstants.ACCOUNT_ID_SOURCE_AT_DIMENSIONS_TAB, value)

    def get_account_id_source(self):
        return self.get_text_by_xpath(WashBookConstants.ACCOUNT_ID_SOURCE_AT_DIMENSIONS_TAB)

    def set_default_route(self, value):
        self.set_combobox_value(WashBookConstants.DEFAULT_ROUTE_AT_DIMENSIONS_TAB, value)

    def get_default_route(self):
        return self.get_text_by_xpath(WashBookConstants.DEFAULT_ROUTE_AT_DIMENSIONS_TAB)

    # filters

    def set_venue_account_filter(self, value):
        self.set_text_by_xpath(WashBookConstants.VENUE_ACCOUNT_FILTER_AT_DIMENSIONS_TAB, value)

    def set_venue_filter(self, value):
        self.set_text_by_xpath(WashBookConstants.VENUE_FILTER_AT_DIMENSIONS_TAB, value)

    def set_account_id_source_filter(self, value):
        self.set_text_by_xpath(WashBookConstants.ACCOUNT_ID_SOURCE_AT_DIMENSIONS_TAB, value)

    def set_default_route_filter(self, value):
        self.set_text_by_xpath(WashBookConstants.DEFAULT_ROUTE_FILTER_AT_DIMENSIONS_TAB, value)
    # endregion
