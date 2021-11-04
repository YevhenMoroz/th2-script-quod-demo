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
        time.sleep(1)

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
        self.find_by_xpath(
            OrderManagementRulesConstants.CONDITIONS_TAB_CONDITIONAL_LOGIC_ADD_CONDITION_BUTTON_XPATH).click()
        time.sleep(1)

    def set_conditional_logic(self,value):
        self.find_by_xpath(OrderManagementRulesConstants.CONDITIONS_TAB_CONDITIONAL_LOGIC_XPATH).click()
        time.sleep(2)
        path = OrderManagementRulesConstants.CONDITIONS_TAB_CONDITIONAL_LOGIC_LIST_XPATH.format(
            value)
        self.select_value_from_dropdown_list(
            path)
        time.sleep(2)

    def set_left_side_at_conditional_logic(self, entity):
        path = OrderManagementRulesConstants.CONDITIONS_TAB_CONDITIONAL_LOGIC_LEFT_SIDE_LIST_OF_ENTITY_XPATH.format(
            entity)
        self.select_value_from_dropdown_list(
            path, entity)

    def set_right_side_at_conditional_logic(self, value):
        self.set_combobox_value(OrderManagementRulesConstants.CONDITIONS_TAB_CONDITIONAL_LOGIC_RIGHT_SIDE_XPATH, value)
        time.sleep(1)

    def set_right_side_list_at_conditional_logic(self, value):
        self.find_by_xpath("//*[@class='input-wrapper ng-star-inserted']").click()
        time.sleep(2)
        path = "//*[@class='cdk-overlay-container']//nb-option[text()='{}']".format(
            value)
        self.select_value_from_dropdown_list(
            path)
        time.sleep(2)


    def click_on_left_side(self):
        self.find_by_xpath(OrderManagementRulesConstants.CONDITIONS_TAB_CONDITIONAL_LOGIC_LEFT_SIDE_XPATH).click()
        time.sleep(2)

    def get_client(self):
        return self.get_text_by_xpath(OrderManagementRulesConstants.CONDITIONS_TAB_CONDITIONAL_LOGIC_RIGHT_SIDE_XPATH)

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
