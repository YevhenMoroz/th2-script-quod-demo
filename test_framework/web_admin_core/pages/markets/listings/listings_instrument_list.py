from test_framework.web_admin_core.pages.common_page import CommonPage
from test_framework.web_admin_core.pages.markets.listings.listings_constants import ListingsConstants
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer


class ListingsInstrumentListSubWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def click_on_plus(self):
        self.find_by_xpath(ListingsConstants.INSTRUMENT_LIST_TAB_PLUS_BUTTON_XPATH).click()

    def click_on_checkmark(self):
        self.find_by_xpath(ListingsConstants.INSTRUMENT_LIST_TAB_CHECKMARK_BUTTON_XPATH).click()

    def click_on_close(self):
        self.find_by_xpath(ListingsConstants.INSTRUMENT_LIST_TAB_CLOSE_BUTTON_XPATH).click()

    def click_on_edit(self):
        self.find_by_xpath(ListingsConstants.INSTRUMENT_LIST_TAB_CLOSE_BUTTON_XPATH).click()

    def click_on_delete(self):
        self.find_by_xpath(ListingsConstants.INSTRUMENT_LIST_TAB_DELETE_BUTTON_XPATH).click()

    def set_instrument_list_filter(self, value):
        self.set_text_by_xpath(ListingsConstants.INSTRUMENT_LIST_TAB_INSTRUMENT_LIST_FILTER_XPATH, value)

    def set_instrument_list(self, value):
        self.set_combobox_value(ListingsConstants.INSTRUMENT_LIST_TAB_INSTRUMENT_LIST_XPATH, value)

    def get_instrument_list(self):
        return self.get_text_by_xpath(ListingsConstants.INSTRUMENT_LIST_TAB_INSTRUMENT_LIST_XPATH)
