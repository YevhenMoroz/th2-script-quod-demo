from quod_qa.web_admin.web_admin_core.pages.common_page import CommonPage
from quod_qa.web_admin.web_admin_core.pages.order_management.order_management_rules.order_management_rules_constants import \
    OrderManagementRulesConstants

from quod_qa.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer


class OrderManagementRulesDefaultResultSubWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def click_on_plus(self):
        self.find_by_xpath(OrderManagementRulesConstants.DEFAULT_RESULT_TAB_PLUS_XPATH).click()

    def click_on_checkmark(self):
        self.find_by_xpath(
            OrderManagementRulesConstants.DEFAULT_RESULT_TAB_CHECKMARK_XPATH).click()

    def click_on_close(self):
        self.find_by_xpath(OrderManagementRulesConstants.DEFAULT_RESULT_TAB_CANCEL_XPATH).click()

    def click_on_edit(self):
        self.find_by_xpath(OrderManagementRulesConstants.DEFAULT_RESULT_TAB_EDIT_XPATH).click()

    def click_on_delete(self):
        self.find_by_xpath(OrderManagementRulesConstants.DEFAULT_RESULT_TAB_DELETE_XPATH).click()

    def set_default_result_name(self, value):
        self.set_text_by_xpath(OrderManagementRulesConstants.DEFAULT_RESULT_TAB_DEFAULT_RESULT_NAME, value)

    def get_default_result_name(self):
        return self.get_text_by_xpath(OrderManagementRulesConstants.DEFAULT_RESULT_TAB_DEFAULT_RESULT_NAME)

    def set_qty_precision(self, value):
        self.set_text_by_xpath(OrderManagementRulesConstants.DEFAULT_RESULT_TAB_QTY_PRECISION, value)

    def get_qty_precision(self):
        return self.get_text_by_xpath(OrderManagementRulesConstants.DEFAULT_RESULT_TAB_QTY_PRECISION)

    def click_on_hold_order(self):
        self.find_by_xpath(OrderManagementRulesConstants.DEFAULT_RESULT_TAB_HOLD_ORDER_CHECKBOX).click()

    def set_exec_policy(self, value):
        self.set_combobox_value(OrderManagementRulesConstants.DEFAULT_RESULT_TAB_EXEC_POLICY_XPATH, value)

    def get_exec_policy(self):
        return self.get_text_by_xpath(OrderManagementRulesConstants.DEFAULT_RESULT_TAB_EXEC_POLICY_XPATH)

    def set_exec_policy_filter(self, value):
        self.set_text_by_xpath(OrderManagementRulesConstants.DEFAULT_RESULT_TAB_EXEC_POLICY_XPATH, value)

    def set_percentage(self, value):
        self.set_text_by_xpath(OrderManagementRulesConstants.DEFAULT_RESULT_TAB_PERCENTAGE_XPATH, value)

    def get_percentage(self):
        return self.get_text_by_xpath(OrderManagementRulesConstants.DEFAULT_RESULT_TAB_PERCENTAGE_XPATH)

    def set_percentage_filter(self, value):
        self.set_text_by_xpath(OrderManagementRulesConstants.DEFAULT_RESULT_TAB_PERCENTAGE_XPATH, value)

    def set_price_origin(self, value):
        self.set_combobox_value(OrderManagementRulesConstants.DEFAULT_RESULT_TAB_PRICE_ORIGIN_XPATH, value)

    def get_price_origin(self):
        return self.get_text_by_xpath(OrderManagementRulesConstants.DEFAULT_RESULT_TAB_PRICE_ORIGIN_XPATH)

    def set_execution_strategy(self, value):
        self.set_combobox_value(OrderManagementRulesConstants.DEFAULT_RESULT_TAB_EXECUTION_STRATEGY_XPATH, value)

    def get_execution_strategy(self):
        return self.get_text_by_xpath(OrderManagementRulesConstants.DEFAULT_RESULT_TAB_EXECUTION_STRATEGY_XPATH)

    def set_strategy_type(self, value):
        self.set_combobox_value(OrderManagementRulesConstants.DEFAULT_RESULT_TAB_STRATEGY_TYPE_XPATH, value)

    def get_strategy_type(self):
        return self.get_text_by_xpath(OrderManagementRulesConstants.DEFAULT_RESULT_TAB_STRATEGY_TYPE_XPATH)

    def set_sor_execution_strategy(self, value):
        self.set_combobox_value(OrderManagementRulesConstants.DEFAULT_RESULT_TAB_SOR_EXECUTION_STRATEGY_XPATH, value)

    def get_sor_execution_strategy(self):
        return self.get_text_by_xpath(OrderManagementRulesConstants.DEFAULT_RESULT_TAB_SOR_EXECUTION_STRATEGY_XPATH)

    def set_venue(self, value):
        self.set_combobox_value(OrderManagementRulesConstants.DEFAULT_RESULT_TAB_VENUE_XPATH, value)

    def get_venue(self):
        return self.get_text_by_xpath(OrderManagementRulesConstants.DEFAULT_RESULT_TAB_VENUE_XPATH)

    def set_route(self, value):
        self.set_combobox_value(OrderManagementRulesConstants.DEFAULT_RESULT_TAB_ROUTE_XPATH, value)

    def get_route(self):
        return self.get_text_by_xpath(OrderManagementRulesConstants.DEFAULT_RESULT_TAB_ROUTE_XPATH)
