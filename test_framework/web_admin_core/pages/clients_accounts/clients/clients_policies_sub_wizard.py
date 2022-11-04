import time

from test_framework.web_admin_core.pages.clients_accounts.clients.clients_constants import ClientsConstants
from test_framework.web_admin_core.pages.common_page import CommonPage
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer


class ClientsPoliciesSubWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def set_default_execution_strategies(self, value):
        self.set_combobox_value(ClientsConstants.POLICIES_TAB_DEFAULT_EXECUTION_STRATEGY_XPATH, value)

    def get_default_execution_strategies(self):
        return self.get_text_by_xpath(ClientsConstants.POLICIES_TAB_DEFAULT_EXECUTION_STRATEGY_XPATH)

    def set_default_sor_execution_strategy(self, value):
        self.set_combobox_value(ClientsConstants.POLICIES_TAB_DEFAULT_SOR_EXECUTION_STRATEGY_XPATH, value)

    def set_default_routing_instruction(self, value):
        self.set_combobox_value(ClientsConstants.POLICIES_TAB_DEFAULT_ROUTING_INSTRUCTION_XPATH, value)

    def get_default_routing_instruction(self):
        return self.get_text_by_xpath(ClientsConstants.POLICIES_TAB_DEFAULT_ROUTING_INSTRUCTION_XPATH)

    def set_default_algo_type(self, value):
        self.set_combobox_value(ClientsConstants.POLICIES_TAB_DEFAULT_ALGO_TYPE_XPATH, value)

    def get_default_algo_type(self):
        return self.get_text_by_xpath(ClientsConstants.POLICIES_TAB_DEFAULT_ALGO_TYPE_XPATH)

    def set_custom_validation_rules(self, value):
        self.set_combobox_value(ClientsConstants.POLICIES_TAB_CUSTOM_VALIDATION_RULES_XPATH, value)

    def get_custom_validation_rules(self):
        return self.get_text_by_xpath(ClientsConstants.POLICIES_TAB_CUSTOM_VALIDATION_RULES_XPATH)

    def click_on_manage_custom_validation_rules(self):
        self.find_by_xpath(ClientsConstants.POLICIES_TAB_MANAGE_CUSTOM_VALIDATION_RULES_XPATH).click()

    def is_default_execution_strategy_has_italic_font(self):
        self.set_text_by_xpath(ClientsConstants.POLICIES_TAB_DEFAULT_EXECUTION_STRATEGY_XPATH, "de")
        time.sleep(2)
        try:
            self.find_by_xpath(ClientsConstants.POLICIES_TAB_LIST_OF_DEFAULT_STRATEGIES_XPATH).click()
            return True
        except Exception:
            return False
