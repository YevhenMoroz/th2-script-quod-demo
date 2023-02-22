from test_framework.web_admin_core.pages.common_page import CommonPage
from test_framework.web_admin_core.pages.markets.listings.listings_constants import ListingsConstants
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer


class ListingsCurrencySubWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def set_currency(self, value):
        self.set_combobox_value(ListingsConstants.CURRENCY_TAB_CURRENCY_XPATH, value)

    def get_currency(self):
        return self.get_text_by_xpath(ListingsConstants.CURRENCY_TAB_CURRENCY_XPATH)

    def is_currency_field_enabled(self):
        return self.is_field_enabled(ListingsConstants.CURRENCY_TAB_CURRENCY_XPATH)

    def set_instr_currency(self, value):
        self.set_combobox_value(ListingsConstants.CURRENCY_TAB_INSTR_CURRENCY_XPATH, value)

    def get_instr_currency(self):
        return self.get_text_by_xpath(ListingsConstants.CURRENCY_TAB_INSTR_CURRENCY_XPATH)

    def set_base_currency(self, value):
        self.set_combobox_value(ListingsConstants.CURRENCY_TAB_BASE_CURRENCY_XPATH, value)

    def get_base_currency(self):
        return self.get_text_by_xpath(ListingsConstants.CURRENCY_TAB_BASE_CURRENCY_XPATH)

    def set_quote_currency(self, value):
        self.set_combobox_value(ListingsConstants.CURRENCY_TAB_QUOTE_CURRENCY_XPATH, value)

    def get_quote_currency(self):
        return self.get_text_by_xpath(ListingsConstants.CURRENCY_TAB_QUOTE_CURRENCY_XPATH)

    def set_strike_currency(self, value):
        self.set_combobox_value(ListingsConstants.CURRENCY_TAB_STRIKE_CURRENCY_XPATH, value)

    def get_strike_currency(self):
        return self.get_text_by_xpath(ListingsConstants.CURRENCY_TAB_STRIKE_CURRENCY_XPATH)

