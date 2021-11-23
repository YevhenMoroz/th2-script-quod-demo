from test_cases.web_admin.web_admin_core.pages.common_page import CommonPage
from test_cases.web_admin.web_admin_core.pages.order_management.order_management_rules.order_management_rules_constants import \
    OrderManagementRulesConstants

from test_cases.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer


class OrderManagementRulesValuesSubWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def set_name(self, value):
        self.set_text_by_xpath(OrderManagementRulesConstants.VALUES_TAB_NAME_XPATH, value)

    def get_name(self):
        return self.get_text_by_xpath(OrderManagementRulesConstants.VALUES_TAB_NAME_XPATH)

    def set_description(self, value):
        self.set_text_by_xpath(OrderManagementRulesConstants.VALUES_TAB_DESCRIPTION_XPATH, value)

    def get_description(self):
        return self.get_text_by_xpath(OrderManagementRulesConstants.VALUES_TAB_DESCRIPTION_XPATH)

    def set_listing_group(self, value):
        self.set_combobox_value(OrderManagementRulesConstants.VALUES_TAB_LISTING_GROUP_XPATH, value)

    def get_listing_group(self):
        return self.get_text_by_xpath(OrderManagementRulesConstants.VALUES_TAB_LISTING_GROUP_XPATH)

    def set_venue(self, value):
        self.set_combobox_value(OrderManagementRulesConstants.VALUES_TAB_VENUE_XPATH, value)

    def get_venue(self):
        return self.get_text_by_xpath(OrderManagementRulesConstants.VALUES_TAB_VENUE_XPATH)

    def set_instr_type(self, value):
        self.set_combobox_value(OrderManagementRulesConstants.VALUES_TAB_INSTR_TYPE_XPATH, value)

    def get_instr_type(self):
        return self.get_text_by_xpath(OrderManagementRulesConstants.VALUES_TAB_INSTR_TYPE_XPATH)

    def set_sub_venue(self, value):
        self.set_combobox_value(OrderManagementRulesConstants.VALUES_TAB_SUB_VENUE_XPATH, value)

    def get_sub_venue(self):
        return self.get_text_by_xpath(OrderManagementRulesConstants.VALUES_TAB_SUB_VENUE_XPATH)

    def set_client(self, value):
        self.set_combobox_value(OrderManagementRulesConstants.VALUES_TAB_CLIENT_XPATH, value)

    def get_client(self):
        return self.get_text_by_xpath(OrderManagementRulesConstants.VALUES_TAB_CLIENT_XPATH)

    def set_user(self, value):
        self.set_combobox_value(OrderManagementRulesConstants.VALUES_TAB_USER_XPATH, value)

    def get_user(self):
        return self.get_text_by_xpath(OrderManagementRulesConstants.VALUES_TAB_USER_XPATH)

    def set_client_group(self, value):
        self.set_combobox_value(OrderManagementRulesConstants.VALUES_TAB_CLIENT_GROUP_XPATH, value)

    def get_client_group(self):
        return self.get_text_by_xpath(OrderManagementRulesConstants.VALUES_TAB_CLIENT_GROUP_XPATH)

    def set_account(self, value):
        self.set_combobox_value(OrderManagementRulesConstants.VALUES_TAB_ACCOUNT_XPATH, value)

    def get_account(self):
        return self.get_text_by_xpath(OrderManagementRulesConstants.VALUES_TAB_ACCOUNT_XPATH)

    def set_strategy_name(self, value):
        self.set_text_by_xpath(OrderManagementRulesConstants.VALUES_TAB_STRATEGY_NAME_XPATH, value)

    def get_strategy_name(self):
        return self.get_text_by_xpath(OrderManagementRulesConstants.VALUES_TAB_STRATEGY_NAME_XPATH)
