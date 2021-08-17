import time

from quod_qa.web_admin.web_admin_core.pages.common_page import CommonPage
from quod_qa.web_admin.web_admin_core.pages.order_management.order_management_rules.order_management_rules_constants import \
    OrderManagementRulesConstants

from quod_qa.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer


class OrderManagementRulesConditionsSubWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def click_on_plus(self):
        self.find_by_xpath(OrderManagementRulesConstants.CONDITIONS_TAB_PLUS_XPATH).click()

    def click_on_checkmark(self):
        self.find_by_xpath(
            OrderManagementRulesConstants.CONDITIONS_TAB_CHECKMARK_XPATH).click()

    def click_on_close(self):
        self.find_by_xpath(OrderManagementRulesConstants.CONDITIONS_TAB_CANCEL_XPATH).click()

    def click_on_edit(self):
        self.find_by_xpath(OrderManagementRulesConstants.CONDITIONS_TAB_EDIT_XPATH).click()

    def click_on_enabled_disable(self, confirmation):
        self.find_by_xpath(OrderManagementRulesConstants.CONDITIONS_TAB_ENABLE_DISABLE_BUTTON_XPATH).click()
        time.sleep(2)
        if confirmation:
            self.find_by_xpath(OrderManagementRulesConstants.OK_BUTTON_XPATH).click()
        else:
            self.find_by_xpath(OrderManagementRulesConstants.CANCEL_BUTTON_XPATH).click()

    def set_name(self, value):
        self.set_text_by_xpath(OrderManagementRulesConstants.CONDITIONS_TAB_NAME_XPATH, value)

    def get_name(self):
        return self.get_text_by_xpath(OrderManagementRulesConstants.CONDITIONS_TAB_NAME_XPATH)

    def set_name_filter(self, value):
        self.set_text_by_xpath(OrderManagementRulesConstants.CONDITIONS_TAB_NAME_FILTER_XPATH, value)

    def set_qty_precision(self, value):
        self.set_text_by_xpath(OrderManagementRulesConstants.CONDITIONS_TAB_QTY_PRECISION_XPATH, value)

    def get_qty_precision(self):
        return self.get_text_by_xpath(OrderManagementRulesConstants.CONDITIONS_TAB_QTY_PRECISION_XPATH)

    def click_on_hold_order(self):
        self.find_by_xpath(OrderManagementRulesConstants.CONDITIONS_TAB_HOLD_ORDER_CHECKBOX).click()

    def click_on_and(self):
        self.find_by_xpath(OrderManagementRulesConstants.CONDITIONS_TAB_AND_RADIO_BUTTON).click()

    def click_on_or(self):
        self.find_by_xpath(OrderManagementRulesConstants.CONDITIONS_TAB_OR_RADIO_BUTTON).click()

    def click_on_add_condition(self):
        self.find_by_xpath(OrderManagementRulesConstants.CONDITIONS_TAB_ADD_CONDITION_BUTTON).click()

    def set_client(self, value):
        self.set_combobox_value(OrderManagementRulesConstants.CONDITIONS_TAB_CLIENT, value)

    def get_client(self):
        return self.get_text_by_xpath(OrderManagementRulesConstants.CONDITIONS_TAB_CLIENT)

    # results

    def click_on_plus_at_results_sub_wizard(self):
        self.find_by_xpath(OrderManagementRulesConstants.RESULTS_SUB_WIZARD_PLUS_XPATH).click()

    def click_on_checkmark_at_results_sub_wizard(self):
        self.find_by_xpath(OrderManagementRulesConstants.RESULTS_SUB_WIZARD_CHECKMARK_XPATH).click()

    def click_on_cancel_at_results_sub_wizard(self):
        self.find_by_xpath(OrderManagementRulesConstants.RESULTS_SUB_WIZARD_CANCEL_XPATH).click()

    def click_on_edit_at_results_sub_wizard(self):
        self.find_by_xpath(OrderManagementRulesConstants.RESULTS_SUB_WIZARD_EDIT_XPATH).click()

    def click_on_delete_at_results_sub_wizard(self):
        self.find_by_xpath(OrderManagementRulesConstants.RESULTS_SUB_WIZARD_DELETE_XPATH).click()

    def set_exec_policy(self, value):
        self.set_combobox_value(OrderManagementRulesConstants.RESULTS_SUB_WIZARD_EXEC_POLICY_XPATH, value)

    def get_exec_policy(self):
        return self.get_text_by_xpath(OrderManagementRulesConstants.RESULTS_SUB_WIZARD_EXEC_POLICY_XPATH)

    def set_exec_policy_filter(self, value):
        self.set_combobox_value(OrderManagementRulesConstants.RESULTS_SUB_WIZARD_EXEC_POLICY_FILTER_XPATH, value)

    def set_percentage(self, value):
        self.set_text_by_xpath(OrderManagementRulesConstants.RESULTS_SUB_WIZARD_PERCENTAGE_XPATH, value)

    def get_percentage(self):
        return self.get_text_by_xpath(OrderManagementRulesConstants.RESULTS_SUB_WIZARD_PERCENTAGE_XPATH)

    def set_percentage_filter(self, value):
        self.set_text_by_xpath(OrderManagementRulesConstants.RESULTS_SUB_WIZARD_PERCENTAGE_FILTER_XPATH, value)

    def set_price_origin(self, value):
        self.set_combobox_value(OrderManagementRulesConstants.RESULTS_SUB_WIZARD_PRICE_ORIGIN_XPATH, value)

    def get_price_origin(self):
        return self.get_text_by_xpath(OrderManagementRulesConstants.RESULTS_SUB_WIZARD_PRICE_ORIGIN_XPATH)

    def set_execution_strategy(self, value):
        self.set_combobox_value(OrderManagementRulesConstants.RESULTS_SUB_WIZARD_EXECUTION_STRATEGY_XPATH, value)

    def get_execution_strategy(self):
        return self.get_text_by_xpath(OrderManagementRulesConstants.RESULTS_SUB_WIZARD_EXECUTION_STRATEGY_XPATH)

    def set_strategy_type(self, value):
        self.set_combobox_value(OrderManagementRulesConstants.RESULTS_SUB_WIZARD_STRATEGY_TYPE_XPATH, value)

    def get_strategy_type(self):
        return self.get_text_by_xpath(OrderManagementRulesConstants.RESULTS_SUB_WIZARD_STRATEGY_TYPE_XPATH)

    def set_sor_execution_strategy(self, value):
        self.set_combobox_value(OrderManagementRulesConstants.RESULTS_SUB_WIZARD_SOR_EXECUTION_STRATEGY_XPATH, value)

    def get_sor_execution_strategy(self):
        return self.get_text_by_xpath(OrderManagementRulesConstants.RESULTS_SUB_WIZARD_SOR_EXECUTION_STRATEGY_XPATH)

    def set_venue(self, value):
        self.set_combobox_value(OrderManagementRulesConstants.RESULTS_SUB_WIZARD_VENUE_XPATH, value)

    def get_venue(self):
        return self.get_text_by_xpath(OrderManagementRulesConstants.RESULTS_SUB_WIZARD_VENUE_XPATH)

    def set_route(self, value):
        self.set_combobox_value(OrderManagementRulesConstants.RESULTS_SUB_WIZARD_ROUTE_XPATH, value)

    def get_route(self):
        return self.get_text_by_xpath(OrderManagementRulesConstants.RESULTS_SUB_WIZARD_ROUTE_XPATH)
