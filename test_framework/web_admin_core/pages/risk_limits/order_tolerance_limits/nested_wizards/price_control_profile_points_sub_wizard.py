from test_framework.web_admin_core.pages.common_page import CommonPage
from test_framework.web_admin_core.pages.risk_limits.order_tolerance_limits.constants import \
    OrderToleranceLimitsConstants
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer


class PriceControlProfilePointsSubWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def click_on_plus_button(self):
        self.find_by_xpath(
            OrderToleranceLimitsConstants.PRICE_CONTROL_PROFILE_POINTS_SUB_WIZARD_PLUS_BUTTON_XPATH).click()

    def click_on_checkmark_button(self):
        self.find_by_xpath(
            OrderToleranceLimitsConstants.PRICE_CONTROL_PROFILE_POINTS_SUB_WIZARD_CHECKMARK_BUTTON_XPATH).click()

    def click_on_close_button(self):
        self.find_by_xpath(
            OrderToleranceLimitsConstants.PRICE_CONTROL_PROFILE_POINTS_SUB_WIZARD_CLOSE_BUTTON_XPATH).click()

    def click_on_edit_button(self):
        self.find_by_xpath(
            OrderToleranceLimitsConstants.PRICE_CONTROL_PROFILE_POINTS_SUB_WIZARD_EDIT_BUTTON_XPATH).click()

    def click_on_delete(self):
        self.find_by_xpath(
            OrderToleranceLimitsConstants.PRICE_CONTROL_PROFILE_POINTS_SUB_WIZARD_DELETE_BUTTON_XPATH).click()

    def set_hard_limit_price_filter(self, value):
        self.set_text_by_xpath(
            OrderToleranceLimitsConstants.PRICE_CONTROL_PROFILE_POINTS_SUB_WIZARD_HARD_LIMIT_PRICE_FILTER_XPATH, value)

    def set_hard_limit_price(self, value):
        self.set_text_by_xpath(
            OrderToleranceLimitsConstants.PRICE_CONTROL_PROFILE_POINTS_SUB_WIZARD_HARD_LIMIT_PRICE_XPATH, value)

    def get_hard_limit_price(self):
        return self.get_text_by_xpath(
            OrderToleranceLimitsConstants.PRICE_CONTROL_PROFILE_POINTS_SUB_WIZARD_HARD_LIMIT_PRICE_XPATH)

    def set_soft_limit_price_filter(self, value):
        self.set_text_by_xpath(
            OrderToleranceLimitsConstants.PRICE_CONTROL_PROFILE_POINTS_SUB_WIZARD_SOFT_LIMIT_PRICE_FILTER_XPATH, value)

    def set_soft_limit_price(self, value):
        self.set_text_by_xpath(
            OrderToleranceLimitsConstants.PRICE_CONTROL_PROFILE_POINTS_SUB_WIZARD_SOFT_LIMIT_PRICE_XPATH, value)

    def get_soft_limit_price(self, value):
        self.get_text_by_xpath(
            OrderToleranceLimitsConstants.PRICE_CONTROL_PROFILE_POINTS_SUB_WIZARD_SOFT_LIMIT_PRICE_XPATH, value)

    def set_upper_limit_filter(self, value):
        self.set_text_by_xpath(
            OrderToleranceLimitsConstants.PRICE_CONTROL_PROFILE_POINTS_SUB_WIZARD_UPPER_LIMIT_FILTER_XPATH, value)

    def set_upper_limit(self, value):
        self.set_text_by_xpath(OrderToleranceLimitsConstants.PRICE_CONTROL_PROFILE_POINTS_SUB_WIZARD_UPPER_LIMIT_XPATH,
                               value)

    def get_upper_limit(self):
        self.get_text_by_xpath(OrderToleranceLimitsConstants.PRICE_CONTROL_PROFILE_POINTS_SUB_WIZARD_UPPER_LIMIT_XPATH)
