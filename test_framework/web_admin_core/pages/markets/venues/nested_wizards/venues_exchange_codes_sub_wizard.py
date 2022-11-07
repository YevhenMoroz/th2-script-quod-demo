from test_framework.web_admin_core.pages.common_page import CommonPage
from test_framework.web_admin_core.pages.markets.venues.venues_constants import VenuesConstants
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer


class VenuesExchangeCodesSubWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def click_on_plus_button(self):
        self.find_by_xpath(VenuesConstants.EXCHANGE_CODES_TAB_PLUS_BUTTON_XPATH).click()

    def click_on_checkmark(self):
        self.find_by_xpath(VenuesConstants.EXCHANGE_CODES_TAB_CHECKMARK_BUTTON_XPATH).click()

    def click_on_close(self):
        self.find_by_xpath(VenuesConstants.EXCHANGE_CODES_TAB_CLOSE_BUTTON_XPATH).click()

    def click_on_edit(self):
        self.find_by_xpath(VenuesConstants.EXCHANGE_CODES_TAB_EDIT_BUTTON_XPATH).click()

    def click_on_delete(self):
        self.find_by_xpath(VenuesConstants.EXCHANGE_CODES_TAB_DELETE_BUTTON_XPATH).click()

    def set_venue(self, value):
        self.set_combobox_value(VenuesConstants.EXCHANGE_CODES_TAB_VENUE_XPATH, value)

    def get_venue(self):
        return self.get_text_by_xpath(VenuesConstants.EXCHANGE_CODES_TAB_VENUE_XPATH)

    def set_exchange_code_mic(self, value):
        self.set_text_by_xpath(VenuesConstants.EXCHANGE_CODES_TAB_EXCHANGE_CODE_MIC_XPATH, value)

    def get_exchange_code_mic(self):
        return self.get_text_by_xpath(VenuesConstants.EXCHANGE_CODES_TAB_EXCHANGE_CODE_MIC_XPATH)

    def set_reuters_exchange_code(self, value):
        self.set_text_by_xpath(VenuesConstants.EXCHANGE_CODES_TAB_REUTERS_EXCHANGE_CODE_XPATH, value)

    def get_reuters_exchange_code(self):
        return self.get_text_by_xpath(VenuesConstants.EXCHANGE_CODES_TAB_REUTERS_EXCHANGE_CODE_XPATH)

    def set_bloomberg_exchange_code(self, value):
        self.set_text_by_xpath(VenuesConstants.EXCHANGE_CODES_TAB_BLOOMBERG_EXCHANGE_CODE_XPATH, value)

    def get_bloomberg_exchange_code(self):
        return self.get_text_by_xpath(VenuesConstants.EXCHANGE_CODES_TAB_BLOOMBERG_EXCHANGE_CODE_XPATH)

    def set_refinitiv_composite_exchange_code(self, value):
        self.set_text_by_xpath(VenuesConstants.EXCHANGE_CODES_TAB_REFINITIV_COMPOSITE_EXCHANGE_CODE_XPATH, value)

    def get_refinitiv_composite_exchange_code(self):
        return self.get_text_by_xpath(VenuesConstants.EXCHANGE_CODES_TAB_REFINITIV_COMPOSITE_EXCHANGE_CODE_XPATH)

    def set_bloomberg_composite_exchange_code(self, value):
        self.set_text_by_xpath(VenuesConstants.EXCHANGE_CODES_TAB_BLOOMBERG_COMPOSITE_EXCHANGE_XPATH, value)

    def get_bloomberg_composite_exchange_code(self):
        return self.get_text_by_xpath(VenuesConstants.EXCHANGE_CODES_TAB_BLOOMBERG_COMPOSITE_EXCHANGE_XPATH)
