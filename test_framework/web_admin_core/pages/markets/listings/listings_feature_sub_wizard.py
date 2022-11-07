import time

from test_framework.web_admin_core.pages.common_page import CommonPage
from test_framework.web_admin_core.pages.markets.listings.listings_constants import ListingsConstants
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer


class ListingsFeatureSubWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def set_order_book_visibility(self, value):
        self.set_text_by_xpath(ListingsConstants.FEATURE_TAB_ORDER_BOOK_VISIBILITY_XPATH, value)

    def get_order_book_visibility(self):
        return self.get_text_by_xpath(ListingsConstants.FEATURE_TAB_ORDER_BOOK_VISIBILITY_XPATH)

    def set_contract_multiplier(self, value):
        self.set_text_by_xpath(ListingsConstants.FEATURE_TAB_CONTRACT_MULTIPLIER_XPATH, value)

    def get_contract_multiplier(self):
        return self.get_text_by_xpath(ListingsConstants.FEATURE_TAB_CONTRACT_MULTIPLIER_XPATH)

    def is_contract_multiplier_empty(self):
        if "has-value" in self.find_by_xpath(ListingsConstants.FEATURE_TAB_CONTRACT_MULTIPLIER_XPATH)\
                .get_attribute("class"):
            return False
        return True

    def set_forward_point_divisor(self, value):
        self.set_text_by_xpath(ListingsConstants.FEATURE_TAB_FORWARD_POINT_DIVISOR_XPATH, value)

    def get_forward_point_divisor(self):
        return self.get_text_by_xpath(ListingsConstants.FEATURE_TAB_FORWARD_POINT_DIVISOR_XPATH)

    def set_composite_listing_id(self, value):
        self.set_text_by_xpath(ListingsConstants.FEATURE_TAB_COMPOSITE_LISTING_ID_XPATH, value)

    def get_composite_listing_id(self):
        return self.get_text_by_xpath(ListingsConstants.FEATURE_TAB_COMPOSITE_LISTING_ID_XPATH)

    def set_composite_venue_name(self, value):
        self.set_text_by_xpath(ListingsConstants.FEATURE_TAB_COMPOSITE_VENUE_NAME_XPATH, value)

    def get_composite_venue_name(self):
        return self.get_text_by_xpath(ListingsConstants.FEATURE_TAB_COMPOSITE_VENUE_NAME_XPATH)

    def set_default_trading_session(self, value):
        self.set_combobox_value(ListingsConstants.FEATURE_TAB_DEFAULT_TRADING_SESSION_XPATH, value)

    def get_default_trading_session(self):
        return self.get_text_by_xpath(ListingsConstants.FEATURE_TAB_COMPOSITE_VENUE_NAME_XPATH)

    def click_on_async_indicator(self):
        self.find_by_xpath(ListingsConstants.FEATURE_TAB_ASYNC_INDICATOR_CHECKBOX_XPATH).click()

    def is_async_indicator_checked(self):
        return self.is_checkbox_selected(ListingsConstants.FEATURE_TAB_ASYNC_INDICATOR_CHECKBOX_XPATH)

    def click_on_cross_through_usd(self):
        self.find_by_xpath(ListingsConstants.FEATURE_TAB_CROSS_THROUGH_USD_CHECKBOX_XPATH).click()

    def is_cross_through_usd_checked(self):
        return self.is_checkbox_selected(ListingsConstants.FEATURE_TAB_CROSS_THROUGH_USD_CHECKBOX_XPATH)

    def click_on_cross_through_eur_to_usd(self):
        self.find_by_xpath(ListingsConstants.FEATURE_TAB_CROSS_THROUGH_EUR_TO_USD_CHECKBOX_XPATH).click()

    def is_cross_through_eur_to_usd_checked(self):
        return self.is_checkbox_selected(ListingsConstants.FEATURE_TAB_CROSS_THROUGH_EUR_TO_USD_CHECKBOX_XPATH)

    def click_on_is_refinitiv_composite(self):
        self.find_by_xpath(ListingsConstants.FEATURE_TAB_IS_REFINITIV_COMPOSITE_XPATH).click()

    def is_is_refinitiv_composite_checked(self):
        return self.is_checkbox_selected(ListingsConstants.FEATURE_TAB_IS_REFINITIV_COMPOSITE_XPATH)

    def click_on_implied_in_support(self):
        self.find_by_xpath(ListingsConstants.FEATURE_TAB_IMPLIED_IN_SUPPORT_CHECKBOX_XPATH).click()

    def is_impied_in_support_checked(self):
        return self.is_checkbox_selected(ListingsConstants.FEATURE_TAB_IMPLIED_IN_SUPPORT_CHECKBOX_XPATH)

    def click_on_cross_through_eur(self):
        self.find_by_xpath(ListingsConstants.FEATURE_TAB_CROSS_THROUGH_EUR_CHECKBOX_XPATH).click()

    def is_cross_through_eur_checked(self):
        return self.is_checkbox_selected(ListingsConstants.FEATURE_TAB_CROSS_THROUGH_EUR_CHECKBOX_XPATH)

    def click_on_through_usd_to_eur(self):
        self.find_by_xpath(ListingsConstants.FEATURE_TAB_CROSS_THROUGH_USD_TO_EUR_CHECKBOX_XPATH).click()

    def is_through_usd_to_eur_checked(self):
        return self.is_checkbox_selected(ListingsConstants.FEATURE_TAB_CROSS_THROUGH_USD_TO_EUR_CHECKBOX_XPATH)

    def click_on_algo_included(self):
        self.find_by_xpath(ListingsConstants.FEATURE_TAB_ALGO_INCLUDED_CHECKBOX_XPATH).click()

    def is_algo_included_checked(self):
        return self.is_checkbox_selected(ListingsConstants.FEATURE_TAB_ALGO_INCLUDED_CHECKBOX_XPATH)

    def click_on_persist_historic_time_sales(self):
        self.find_by_xpath(ListingsConstants.FEATURE_TAB_PERSIST_HISTORIC_TIME_SALES_XPATH).click()

    def is_persist_historic_time_sales_checked(self):
        return self.is_checkbox_selected(ListingsConstants.FEATURE_TAB_PERSIST_HISTORIC_TIME_SALES_XPATH)

    def click_on_is_bloomberg_composite(self):
        self.find_by_xpath(ListingsConstants.FEATURE_TAB_IS_BLOOMBERG_COMPOSITE_XPATH).click()

    def is_is_bloomberg_composite(self):
        return self.is_checkbox_selected(ListingsConstants.FEATURE_TAB_IS_BLOOMBERG_COMPOSITE_XPATH)