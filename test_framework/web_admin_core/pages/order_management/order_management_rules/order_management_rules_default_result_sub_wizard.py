from test_framework.web_admin_core.pages.common_page import CommonPage
from test_framework.web_admin_core.pages.order_management.order_management_rules.order_management_rules_constants import \
    OrderManagementRulesConstants

from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer


class OrderManagementRulesDefaultResultSubWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def click_on_edit(self):
        self.find_by_xpath(OrderManagementRulesConstants.DefaultResultAtConditions.EDIT_XPATH).click()

    def click_on_checkmark(self):
        self.find_by_xpath(
            OrderManagementRulesConstants.DefaultResultAtConditions.CHECKMARK_XPATH).click()

    def click_on_close(self):
        self.find_by_xpath(OrderManagementRulesConstants.DefaultResultAtConditions.CANCEL_XPATH).click()

    def click_on_plus_at_results(self):
        self.find_by_xpath(OrderManagementRulesConstants.DefaultResultAtConditions.PLUS_BUTTON_AT_RESULTS_XPATH)

    def click_on_edit_at_results(self):
        self.find_by_xpath(OrderManagementRulesConstants.DefaultResultAtConditions.EDIT_AT_RESULTS_XPATH).click()

    def click_on_delete(self):
        self.find_by_xpath(OrderManagementRulesConstants.DefaultResultAtConditions.DELETE_AT_RESULTS_XPATH).click()

    def set_default_result_name(self, value):
        self.set_text_by_xpath(OrderManagementRulesConstants.DefaultResultAtConditions.NAME, value)

    def get_default_result_name(self):
        return self.get_text_by_xpath(OrderManagementRulesConstants.DefaultResultAtConditions.NAME)

    def set_qty_precision(self, value):
        self.set_text_by_xpath(OrderManagementRulesConstants.DefaultResultAtConditions.QTY_PRECISION, value)

    def get_qty_precision(self):
        return self.get_text_by_xpath(OrderManagementRulesConstants.DefaultResultAtConditions.QTY_PRECISION)

    def click_on_hold_order(self):
        self.find_by_xpath(OrderManagementRulesConstants.DefaultResultAtConditions.HOLD_ORDER_CHECKBOX).click()

    def set_exec_policy(self, value):
        self.set_combobox_value(OrderManagementRulesConstants.DefaultResultAtConditions.EXEC_POLICY_AT_RESULTS_XPATH, value)

    def get_exec_policy(self):
        return self.get_text_by_xpath(OrderManagementRulesConstants.DefaultResultAtConditions.EXEC_POLICY_AT_RESULTS_XPATH)

    def set_exec_policy_filter(self, value):
        self.set_text_by_xpath(OrderManagementRulesConstants.DefaultResultAtConditions.EXEC_POLICY_FILTER_XPATH, value)

    def set_percentage(self, value):
        self.set_text_by_xpath(OrderManagementRulesConstants.DefaultResultAtConditions.PERCENTAGE_AT_RESULTS_XPATH, value)

    def get_percentage(self):
        return self.get_text_by_xpath(OrderManagementRulesConstants.DefaultResultAtConditions.PERCENTAGE_AT_RESULTS_XPATH)

    def set_percentage_filter(self, value):
        self.set_text_by_xpath(OrderManagementRulesConstants.DefaultResultAtConditions.PERCENTAGE_FILTER_XPATH, value)

    def set_price_origin(self, value):
        self.set_combobox_value(OrderManagementRulesConstants.DefaultResultAtConditions.PRICE_ORIGIN_AT_RESULTS_XPATH, value)

    def get_price_origin(self):
        return self.get_text_by_xpath(OrderManagementRulesConstants.DefaultResultAtConditions.PRICE_ORIGIN_AT_RESULTS_XPATH)

    def set_execution_strategy(self, value):
        self.set_combobox_value(OrderManagementRulesConstants.DefaultResultAtConditions.EXECUTION_STRATEGY_AT_RESULTS_XPATH, value)

    def get_execution_strategy(self):
        return self.get_text_by_xpath(OrderManagementRulesConstants.DefaultResultAtConditions.EXECUTION_STRATEGY_AT_RESULTS_XPATH)

    def set_strategy_type(self, value):
        self.set_combobox_value(OrderManagementRulesConstants.DefaultResultAtConditions.STRATEGY_TYPE_AT_RESULTS_XPATH, value)

    def get_strategy_type(self):
        return self.get_text_by_xpath(OrderManagementRulesConstants.DefaultResultAtConditions.STRATEGY_TYPE_AT_RESULTS_XPATH)

    def set_sor_execution_strategy(self, value):
        self.set_combobox_value(OrderManagementRulesConstants.DefaultResultAtConditions.SOR_EXECUTION_STRATEGY_AT_RESULTS_XPATH, value)

    def get_sor_execution_strategy(self):
        return self.get_text_by_xpath(OrderManagementRulesConstants.DefaultResultAtConditions.SOR_EXECUTION_STRATEGY_AT_RESULTS_XPATH)

    def set_venue(self, value):
        self.set_combobox_value(OrderManagementRulesConstants.DefaultResultAtConditions.VENUE_AT_RESULTS_XPATH, value)

    def get_venue(self):
        return self.get_text_by_xpath(OrderManagementRulesConstants.DefaultResultAtConditions.VENUE_AT_RESULTS_XPATH)

    def set_route(self, value):
        self.set_combobox_value(OrderManagementRulesConstants.DefaultResultAtConditions.ROUTE_AT_RESULTS_XPATH, value)

    def get_route(self):
        return self.get_text_by_xpath(OrderManagementRulesConstants.DefaultResultAtConditions.ROUTE_AT_RESULTS_XPATH)
