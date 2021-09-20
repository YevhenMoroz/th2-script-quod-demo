from quod_qa.web_admin.web_admin_core.pages.common_page import CommonPage
from quod_qa.web_admin.web_admin_core.pages.reference_data.listings.listings_constants import ListingsConstants
from quod_qa.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer


class ListingsFeatureSubWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def set_order_book_visibility(self, value):
        self.set_text_by_xpath(ListingsConstants.FEATURE_TAB_ORDER_BOOK_VISIBILITY_XPATH, value)

    def get_order_book_visibility(self):
        return self.get_text_by_xpath(ListingsConstants.FEATURE_TAB_ORDER_BOOK_VISIBILITY_XPATH)

    def set_forward_point_divisor(self, value):
        self.set_text_by_xpath(ListingsConstants.FEATURE_TAB_FORWARD_POINT_DIVISOR_XPATH, value)

    def get_forward_point_divisor(self):
        return self.get_text_by_xpath(ListingsConstants.FEATURE_TAB_FORWARD_POINT_DIVISOR_XPATH)

    def click_on_async_indicator(self):
        self.find_by_xpath(ListingsConstants.FEATURE_TAB_ASYNC_INDICATOR_CHECKBOX_XPATH).click()

    def click_on_cross_through_usd(self):
        self.find_by_xpath(ListingsConstants.FEATURE_TAB_CROSS_THROUGH_USD_CHECKBOX_XPATH).click()

    def click_cross_through_eur_to_usd(self):
        self.find_by_xpath(ListingsConstants.FEATURE_TAB_CROSS_THROUGH_EUR_TO_USD_CHECKBOX_XPATH).click()

    def click_on_implied_in_support(self):
        self.find_by_xpath(ListingsConstants.FEATURE_TAB_IMPLIED_IN_SUPPORT_CHECKBOX_XPATH).click()

    def click_on_cross_through_eur(self):
        self.find_by_xpath(ListingsConstants.FEATURE_TAB_CROSS_THROUGH_EUR_CHECKBOX_XPATH).click()

    def click_on_through_usd_to_eur(self):
        self.find_by_xpath(ListingsConstants.FEATURE_TAB_CROSS_THROUGH_USD_TO_EUR_CHECKBOX_XPATH).click()

    def click_on_algo_included(self):
        self.find_by_xpath(ListingsConstants.FEATURE_TAB_ALGO_INCLUDED_CHECKBOX_XPATH).click()
