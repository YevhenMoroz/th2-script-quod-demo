from test_framework.web_admin_core.pages.common_page import CommonPage
from test_framework.web_admin_core.pages.risk_limits.order_velocity_limits.constants import \
    OrderVelocityLimitsConstants
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer


class OrderVelocityLimitsValuesSubWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def set_order_velocity_limit_name(self, value):
        self.set_text_by_xpath(OrderVelocityLimitsConstants.VALUES_TAB_ORDER_VELOCITY_LIMIT_NAME_XPATH, value)

    def get_order_velocity_limit_name(self):
        return self.get_text_by_xpath(OrderVelocityLimitsConstants.VALUES_TAB_ORDER_VELOCITY_LIMIT_NAME_XPATH)

    def set_max_amount(self, value):
        self.set_text_by_xpath(OrderVelocityLimitsConstants.VALUES_TAB_MAX_AMOUNT_XPATH, value)

    def get_max_amount(self):
        return self.get_text_by_xpath(OrderVelocityLimitsConstants.VALUES_TAB_MAX_AMOUNT_XPATH)

    def set_moving_time_window(self, value):
        self.set_text_by_xpath(OrderVelocityLimitsConstants.VALUES_TAB_MOVING_TIME_WINDOW_XPATH, value)

    def get_moving_time_window(self):
        return self.get_text_by_xpath(OrderVelocityLimitsConstants.VALUES_TAB_MOVING_TIME_WINDOW_XPATH)

    def set_max_quantity(self, value):
        self.set_text_by_xpath(OrderVelocityLimitsConstants.VALUES_TAB_MAX_QUANTITY_XPATH, value)

    def get_max_quantity(self):
        return self.get_text_by_xpath(OrderVelocityLimitsConstants.VALUES_TAB_MAX_QUANTITY_XPATH)

    def set_max_order_actions(self, value):
        self.set_text_by_xpath(OrderVelocityLimitsConstants.VALUES_TAB_MAX_ORDER_ACTIONS_XPATH, value)

    def get_max_order_actions(self):
        return self.get_text_by_xpath(OrderVelocityLimitsConstants.VALUES_TAB_MAX_ORDER_ACTIONS_XPATH)

    def click_on_blocked_rule_checkbox(self):
        self.find_by_xpath(OrderVelocityLimitsConstants.VALUES_TAB_BLOCKED_RULE_CHECKBOX_XPATH).click()

    def click_on_auto_reset(self):
        self.find_by_xpath(OrderVelocityLimitsConstants.VALUES_TAB_AUTO_RESET_CHECKBOX_XPATH).click()
