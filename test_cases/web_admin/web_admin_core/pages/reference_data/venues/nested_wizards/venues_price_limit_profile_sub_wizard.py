from test_cases.web_admin.web_admin_core.pages.common_page import CommonPage
from test_cases.web_admin.web_admin_core.pages.reference_data.venues.venues_constants import VenuesConstants
from test_cases.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer


class VenuesPriceLimitProfileSubWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def click_on_plus_button(self):
        self.find_by_xpath(VenuesConstants.PRICE_LIMIT_PROFILES_TAB_PLUS_BUTTON_XPATH).click()

    def click_on_checkmark(self):
        self.find_by_xpath(VenuesConstants.PRICE_LIMIT_PROFILES_TAB_CHECKMARK_BUTTON_XPATH).click()

    def click_on_close(self):
        self.find_by_xpath(VenuesConstants.PRICE_LIMIT_PROFILES_TAB_CLOSE_BUTTON_XPATH).click()

    def click_on_edit(self):
        self.find_by_xpath(VenuesConstants.PRICE_LIMIT_PROFILES_TAB_EDIT_BUTTON_XPATH).click()

    def click_on_delete(self):
        self.find_by_xpath(VenuesConstants.PRICE_LIMIT_PROFILES_TAB_DELETE_BUTTON_XPATH).click()

    def set_external_id(self, value):
        self.set_text_by_xpath(VenuesConstants.PRICE_LIMIT_PROFILES_TAB_EXTERNAL_ID_XPATH, value)

    def get_external_id(self):
        return self.get_text_by_xpath(VenuesConstants.PRICE_LIMIT_PROFILES_TAB_EXTERNAL_ID_XPATH)

    def set_external_id_filter(self, value):
        self.set_text_by_xpath(VenuesConstants.PRICE_LIMIT_PROFILES_TAB_EXTERNAL_ID_FILTER_XPATH, value)

    def set_trading_reference_price_type(self, value):
        self.set_combobox_value(VenuesConstants.PRICE_LIMIT_PROFILES_TAB_TRADING_REFERENCE_PRICE_TYPE_XPATH, value)

    def get_trading_reference_price_type(self):
        return self.get_text_by_xpath(VenuesConstants.PRICE_LIMIT_PROFILES_TAB_TRADING_REFERENCE_PRICE_TYPE_XPATH)

    def set_trading_reference_price_type_filter(self, value):
        self.set_text_by_xpath(VenuesConstants.PRICE_LIMIT_PROFILES_TAB_TRADING_REFERENCE_PRICE_TYPE_FILTER_XPATH,
                               value)

    def set_price_limit_type(self, value):
        self.set_combobox_value(VenuesConstants.PRICE_LIMIT_PROFILES_TAB_PRICE_LIMIT_TYPE_XPATH, value)

    def get_price_limit_type(self):
        return self.get_text_by_xpath(VenuesConstants.PRICE_LIMIT_PROFILES_TAB_PRICE_LIMIT_TYPE_XPATH)

    def set_price_limit_type_filter(self, value):
        self.set_text_by_xpath(VenuesConstants.PRICE_LIMIT_PROFILES_TAB_PRICE_LIMIT_TYPE_FILTER_XPATH, value)

    def set_price_limit_field_name(self, value):
        self.set_text_by_xpath(VenuesConstants.PRICE_LIMIT_PROFILES_TAB_PRICE_LIMIT_FIELD_NAME_XPATH, value)

    def get_price_limit_field_name(self):
        return self.get_text_by_xpath(VenuesConstants.PRICE_LIMIT_PROFILES_TAB_PRICE_LIMIT_FIELD_NAME_XPATH)

    def set_price_limit_field_name_filter(self, value):
        self.set_text_by_xpath(VenuesConstants.PRICE_LIMIT_PROFILES_TAB_PRICE_LIMIT_FIELD_NAME_FILTER_XPATH, value)

    # ----------Price limit points-----

    def click_on_plus_button_at_price_limit_points(self):
        self.find_by_xpath(VenuesConstants.PRICE_LIMIT_POINTS_TAB_PLUS_BUTTON_XPATH).click()

    def click_on_checkmark_at_price_limit_points(self):
        self.find_by_xpath(VenuesConstants.PRICE_LIMIT_POINTS_TAB_CHECKMARK_BUTTON_XPATH).click()

    def click_on_close_at_price_limit_points(self):
        self.find_by_xpath(VenuesConstants.PRICE_LIMIT_POINTS_TAB_CLOSE_BUTTON_XPATH).click()

    def click_on_edit_at_price_limit_points(self):
        self.find_by_xpath(VenuesConstants.PRICE_LIMIT_POINTS_TAB_EDIT_BUTTON_XPATH).click()

    def click_on_delete_at_price_limit_points(self):
        self.find_by_xpath(VenuesConstants.PRICE_LIMIT_POINTS_TAB_DELETE_BUTTON_XPATH).click()

    def set_limit_price(self, value):
        self.set_text_by_xpath(VenuesConstants.PRICE_LIMIT_POINTS_TAB_LIMIT_PRICE_XPATH, value)

    def get_limit_price(self):
        return self.get_text_by_xpath(VenuesConstants.PRICE_LIMIT_POINTS_TAB_LIMIT_PRICE_XPATH)

    def set_limit_price_filter(self, value):
        self.set_text_by_xpath(VenuesConstants.PRICE_LIMIT_POINTS_TAB_LIMIT_PRICE_FILTER_XPATH, value)

    def set_auction_limit_price(self, value):
        self.set_text_by_xpath(VenuesConstants.PRICE_LIMIT_POINTS_TAB_AUCTION_LIMIT_PRICE_XPATH, value)

    def get_auction_limit_price(self):
        return self.get_text_by_xpath(VenuesConstants.PRICE_LIMIT_POINTS_TAB_AUCTION_LIMIT_PRICE_XPATH)

    def set_auction_limit_price_filter(self, value):
        self.set_text_by_xpath(VenuesConstants.PRICE_LIMIT_POINTS_TAB_AUCTION_LIMIT_PRICE_FILTER_XPATH, value)

    def set_upper_limit(self, value):
        self.set_text_by_xpath(VenuesConstants.PRICE_LIMIT_POINTS_TAB_UPPER_LIMIT_XPATH, value)

    def get_upper_limit(self):
        return self.get_text_by_xpath(VenuesConstants.PRICE_LIMIT_POINTS_TAB_UPPER_LIMIT_XPATH)

    def set_upper_limit_filter(self, value):
        self.set_text_by_xpath(VenuesConstants.PRICE_LIMIT_POINTS_TAB_UPPER_LIMIT_FILTER_XPATH, value)

        













