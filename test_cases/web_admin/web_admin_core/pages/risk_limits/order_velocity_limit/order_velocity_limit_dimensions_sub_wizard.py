import time

from test_cases.web_admin.web_admin_core.pages.common_page import CommonPage
from test_cases.web_admin.web_admin_core.pages.risk_limits.order_velocity_limit.order_velocity_limit_constants import \
    OrderVelocityLimitConstants
from test_cases.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer


class OrderVelocityLimitDimensionsSubWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def set_client(self, value):
        self.set_combobox_value(OrderVelocityLimitConstants.DIMENSIONS_TAB_CLIENT_XPATH, value)

    def get_client(self):
        return self.get_text_by_xpath(OrderVelocityLimitConstants.DIMENSIONS_TAB_CLIENT_XPATH)

    def set_side(self, value):
        self.set_combobox_value(OrderVelocityLimitConstants.DIMENSIONS_TAB_SIDE_XPATH, value)

    def get_side(self):
        return self.get_text_by_xpath(OrderVelocityLimitConstants.DIMENSIONS_TAB_SIDE_XPATH)

    def set_instr_symbol(self, value):
        self.set_combobox_value(OrderVelocityLimitConstants.DIMENSIONS_TAB_INSTR_SYMBOL_XPATH, value)

    def get_instr_symbol(self):
        return self.get_text_by_xpath(OrderVelocityLimitConstants.DIMENSIONS_TAB_INSTR_SYMBOL_XPATH)

    # TODO: functionality is not completed yet
    def set_listing(self, value):
        self.set_text_by_xpath(OrderVelocityLimitConstants.DIMENSIONS_TAB_LISTING_XPATH, value)

    def get_listing(self):
        pass

    def click_on_all_orders(self):
        self.find_by_xpath(OrderVelocityLimitConstants.DIMENSIONS_TAB_ALL_ORDERS_CHECKBOX_XPATH).click()
