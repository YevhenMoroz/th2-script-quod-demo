from test_framework.web_admin_core.pages.common_page import CommonPage
from test_framework.web_admin_core.pages.risk_limits.order_tolerance_limits.constants import \
    OrderToleranceLimitsConstants

from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer


class OrderToleranceLimitsDimensionsSubWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def set_listing_group(self, value):
        self.set_combobox_value(OrderToleranceLimitsConstants.VALUES_TAB_LISTING_GROUP_XPATH, value)

    def get_listing_group(self):
        return self.get_text_by_xpath(OrderToleranceLimitsConstants.VALUES_TAB_LISTING_GROUP_XPATH)

    def set_instr_type(self, value):
        self.set_combobox_value(OrderToleranceLimitsConstants.VALUES_TAB_INSTR_TYPE_XPATH, value)

    def get_instr_type(self):
        return self.get_text_by_xpath(OrderToleranceLimitsConstants.VALUES_TAB_INSTR_TYPE_XPATH)

    def set_listing(self, value):
        self.set_text_by_xpath(OrderToleranceLimitsConstants.VALUES_TAB_LISTING_XPATH, value)

    def get_listing(self):
        return self.get_text_by_xpath(OrderToleranceLimitsConstants.VALUES_TAB_LISTING_XPATH)

    def click_on_per_listing_checkbox(self):
        self.find_by_xpath(OrderToleranceLimitsConstants.VALUES_TAB_PER_LISTING_CHECKBOX_XPATH).click()

    def set_user(self, value):
        self.set_combobox_value(OrderToleranceLimitsConstants.VALUES_TAB_USER_XPATH, value)

    def get_user(self):
        return self.get_text_by_xpath(OrderToleranceLimitsConstants.VALUES_TAB_USER_XPATH)

    def set_client(self, value):
        self.set_combobox_value(OrderToleranceLimitsConstants.VALUES_TAB_CLIENT_XPATH, value)

    def get_client(self):
        return self.get_text_by_xpath(OrderToleranceLimitsConstants.VALUES_TAB_CLIENT_XPATH)

    def set_client_group(self, value):
        self.set_combobox_value(OrderToleranceLimitsConstants.VALUES_TAB_CLIENT_GROUP_XPATH, value)

    def get_client_group(self):
        return self.get_text_by_xpath(OrderToleranceLimitsConstants.VALUES_TAB_CLIENT_GROUP_XPATH)

    def set_venue(self, value):
        self.set_combobox_value(OrderToleranceLimitsConstants.VALUES_TAB_VENUE_XPATH, value)

    def get_venue(self):
        return self.get_text_by_xpath(OrderToleranceLimitsConstants.VALUES_TAB_VENUE_XPATH)

    def set_sub_venue(self, value):
        self.set_combobox_value(OrderToleranceLimitsConstants.VALUES_TAB_SUB_VENUE_XPATH, value)

    def get_sub_venue(self):
        return self.get_text_by_xpath(OrderToleranceLimitsConstants.VALUES_TAB_SUB_VENUE_XPATH)
