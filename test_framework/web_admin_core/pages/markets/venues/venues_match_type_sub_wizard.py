from test_framework.web_admin_core.pages.common_page import CommonPage
from test_framework.web_admin_core.pages.markets.venues.venues_constants import VenuesConstants
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer


class VenuesMatchTypeSubWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def click_on_plus_button(self):
        self.find_by_xpath(VenuesConstants.MATCH_TYPE_TAB_PLUS_BUTTON_XPATH).click()

    def click_on_checkmark(self):
        self.find_by_xpath(VenuesConstants.MATCH_TYPE_TAB_CHECKMARK_BUTTON_XPATH).click()

    def click_on_close(self):
        self.find_by_xpath(VenuesConstants.MATCH_TYPE_TAB_CLOSE_BUTTON_XPATH).click()

    def click_on_edit(self):
        self.find_by_xpath(VenuesConstants.MATCH_TYPE_TAB_EDIT_BUTTON_XPATH).click()

    def click_on_delete(self):
        self.find_by_xpath(VenuesConstants.MATCH_TYPE_TAB_DELETE_BUTTON_XPATH).click()

    def set_name(self, value):
        self.set_text_by_xpath(VenuesConstants.MATCH_TYPE_TAB_NAME_XPATH, value)

    def set_name_filter(self, value):
        self.set_text_by_xpath(VenuesConstants.MATCH_TYPE_TAB_NAME_XPATH, value)

    def get_name(self):
        return self.get_text_by_xpath(VenuesConstants.MATCH_TYPE_TAB_NAME_XPATH)

    def set_match_type(self, value):
        self.set_combobox_value(VenuesConstants.MATCH_TYPE_TAB_MATCH_TYPE_XPATH, value)

    def get_match_type(self):
        self.get_text_by_xpath(VenuesConstants.MATCH_TYPE_TAB_MATCH_TYPE_XPATH)

    def set_match_type_filter(self, value):
        self.set_text_by_xpath(VenuesConstants.MATCH_TYPE_TAB_MATCH_TYPE_FILTER_XPATH, value)
