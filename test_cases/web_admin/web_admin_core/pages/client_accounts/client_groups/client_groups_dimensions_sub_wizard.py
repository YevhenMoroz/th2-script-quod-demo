from test_cases.web_admin.web_admin_core.pages.client_accounts.client_groups.client_groups_constants import \
    ClientGroupsConstants
from test_cases.web_admin.web_admin_core.pages.common_page import CommonPage
from test_cases.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer


class ClientGroupsDimensionsSubWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def set_default_execution_strategy(self, value):
        self.set_combobox_value(ClientGroupsConstants.DIMENSIONS_TAB_DEFAULT_EXECUTION_STRATEGY_XPATH, value)

    def get_default_execution_strategy(self):
        return self.get_text_by_xpath(ClientGroupsConstants.DIMENSIONS_TAB_DEFAULT_EXECUTION_STRATEGY_XPATH)

    def set_default_sor_execution_strategy(self, value):
        self.set_combobox_value(ClientGroupsConstants.DIMENSIONS_TAB_DEFAULT_SOR_EXECUTION_STRATEGY_XPATH, value)

    def get_default_sor_execution_strategy(self):
        return self.get_text_by_xpath(ClientGroupsConstants.DIMENSIONS_TAB_DEFAULT_SOR_EXECUTION_STRATEGY_XPATH)

    def set_custom_validation_rules(self, value):
        self.set_combobox_value(ClientGroupsConstants.DIMENSIONS_TAB_CUSTOM_VALIDATION_RULES_XPATH, value)

    def get_custom_validation_rules(self):
        return self.get_text_by_xpath(ClientGroupsConstants.DIMENSIONS_TAB_CUSTOM_VALIDATION_RULES_XPATH)

    def click_on_manage_custom_validation_rules(self):
        self.find_by_xpath(ClientGroupsConstants.DIMENSIONS_TAB_CUSTOM_VALIDATION_RULES_MANAGE_BUTTON_XPATH).click()
