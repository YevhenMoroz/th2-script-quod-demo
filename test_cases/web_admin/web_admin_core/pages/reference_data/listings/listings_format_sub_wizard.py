from test_cases.web_admin.web_admin_core.pages.common_page import CommonPage
from test_cases.web_admin.web_admin_core.pages.reference_data.listings.listings_constants import ListingsConstants
from test_cases.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer


class ListingsFormatSubWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def set_price_format(self, value):
        self.set_text_by_xpath(ListingsConstants.FORMAT_TAB_PRICE_FORMAT_XPATH, value)

    def get_price_format(self):
        return self.get_text_by_xpath(ListingsConstants.FORMAT_TAB_PRICE_FORMAT_XPATH)

    def set_strike_decimal_places(self, value):
        self.set_text_by_xpath(ListingsConstants.FORMAT_TAB_STRIKE_DECIMAL_PLACES_XPATH, value)

    def get_strike_decimal_places(self):
        return self.get_text_by_xpath(ListingsConstants.FORMAT_TAB_STRIKE_DECIMAL_PLACES_XPATH)

    def set_strike_tick_denominator(self, value):
        self.set_text_by_xpath(ListingsConstants.FORMAT_TAB_STRIKE_TICK_DENOMINATOR_XPATH, value)

    def get_strike_tick_denominator(self):
        return self.get_text_by_xpath(ListingsConstants.FORMAT_TAB_STRIKE_TICK_DENOMINATOR_XPATH)

    def set_price_precision(self, value):
        self.set_text_by_xpath(ListingsConstants.FORMAT_TAB_PRICE_PRECISION_XPATH, value)

    def get_price_precision(self):
        return self.get_text_by_xpath(ListingsConstants.FORMAT_TAB_PRICE_PRECISION_XPATH)

    def set_tick_value(self, value):
        self.set_text_by_xpath(ListingsConstants.FORMAT_TAB_TICK_VALUE_XPATH, value)

    def get_tick_value(self):
        return self.get_text_by_xpath(ListingsConstants.FORMAT_TAB_TICK_VALUE_XPATH)

    def set_large_numbers_precision(self, value):
        self.set_text_by_xpath(ListingsConstants.FORMAT_TAB_LARGE_NUMBERS_PRECISION_XPATH, value)

    def get_large_numbers_precision(self):
        return self.get_text_by_xpath(ListingsConstants.FORMAT_TAB_LARGE_NUMBERS_PRECISION_XPATH)

    def set_tick_denominator(self, value):
        self.set_text_by_xpath(ListingsConstants.FORMAT_TAB_TICK_DENOMINATOR_XPATH, value)

    def get_tick_denominator(self):
        return self.get_text_by_xpath(ListingsConstants.FORMAT_TAB_TICK_DENOMINATOR_XPATH)
