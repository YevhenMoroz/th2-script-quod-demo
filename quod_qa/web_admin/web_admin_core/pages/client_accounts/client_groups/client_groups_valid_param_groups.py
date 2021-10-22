from quod_qa.web_admin.web_admin_core.pages.client_accounts.client_groups.client_groups_constants import \
    ClientGroupsConstants
from quod_qa.web_admin.web_admin_core.pages.common_page import CommonPage
from quod_qa.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer


class ClientGroupsValidParamGroupsSubWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def click_on_plus(self):
        self.find_by_xpath(ClientGroupsConstants.VALID_PARAM_GROUPS_TAB_PLUS_XPATH).click()

    def click_on_edit(self):
        self.find_by_xpath(ClientGroupsConstants.VALID_PARAM_GROUPS_TAB_EDIT_XPATH).click()

    def click_on_delete(self):
        self.find_by_xpath(ClientGroupsConstants.VALID_PARAM_GROUPS_TAB_DELETE_XPATH).click()

    def click_on_checkmark(self):
        self.find_by_xpath(ClientGroupsConstants.VALID_PARAM_GROUPS_TAB_CHECKMARK_XPATH).click()

    def click_on_close(self):
        self.find_by_xpath(ClientGroupsConstants.VALID_PARAM_GROUPS_TAB_CLOSE_XPATH).click()

    def click_on_plus_at_parameters(self):
        self.find_by_xpath(ClientGroupsConstants.VALID_PARAM_GROUPS_PARAMETERS_TAB_PLUS_XPATH).click()

    def click_on_edit_at_parameters(self):
        self.find_by_xpath(ClientGroupsConstants.VALID_PARAM_GROUPS_PARAMETERS_TAB_EDIT_XPATH).click()

    def click_on_delete_at_parameters(self):
        self.find_by_xpath(ClientGroupsConstants.VALID_PARAM_GROUPS_PARAMETERS_TAB_DELETE_XPATH).click()

    def click_on_checkmark_at_parameters(self):
        self.find_by_xpath(ClientGroupsConstants.VALID_PARAM_GROUPS_PARAMETERS_TAB_CHECKMARK_XPATH).click()

    def click_on_close_at_parameters(self):
        self.find_by_xpath(ClientGroupsConstants.VALID_PARAM_GROUPS_PARAMETERS_TAB_CLOSE_XPATH).click()

    def set_name(self, value):
        self.set_text_by_xpath(ClientGroupsConstants.VALID_PARAM_GROUPS_TAB_NAME_XPATH,value)

    def get_name(self):
        return self.get_text_by_xpath(ClientGroupsConstants.VALID_PARAM_GROUPS_TAB_NAME_XPATH)

    def set_name_filter(self, value):
        self.set_text_by_xpath(ClientGroupsConstants.VALID_PARAM_GROUPS_TAB_NAME_FILTER_XPATH,value)

    def set_parameter(self,value):
        self.set_combobox_value(ClientGroupsConstants.VALID_PARAM_GROUPS_PARAMETERS_TAB_PARAMETER_XPATH,value)

    def get_parameter(self):
        return self.get_text_by_xpath(ClientGroupsConstants.VALID_PARAM_GROUPS_PARAMETERS_TAB_PARAMETER_XPATH)

    def set_parameter_filter(self, value):
        self.set_text_by_xpath(ClientGroupsConstants.VALID_PARAM_GROUPS_PARAMETERS_TAB_PARAMETER_FILTER_XPATH,value)

    def set_value(self,value):
        self.set_text_by_xpath(ClientGroupsConstants.VALID_PARAM_GROUPS_PARAMETERS_TAB_VALUE_XPATH,value)

    def get_value(self):
        return self.get_text_by_xpath(ClientGroupsConstants.VALID_PARAM_GROUPS_PARAMETERS_TAB_VALUE_XPATH)

    def set_value_filter(self,value):
        self.set_text_by_xpath(ClientGroupsConstants.VALID_PARAM_GROUPS_PARAMETERS_TAB_VALUE_FILTER_XPATH, value)

    def set_rule(self,value):
        self.set_combobox_value(ClientGroupsConstants.DIMENSIONS_TAB_CUSTOM_VALIDATION_RULES_XPATH, value)

    def get_rule(self):
        return self.get_text_by_xpath(ClientGroupsConstants.DIMENSIONS_TAB_CUSTOM_VALIDATION_RULES_XPATH)

    def set_rule_filter(self, value):
        self.set_text_by_xpath(ClientGroupsConstants.VALID_PARAM_GROUPS_PARAMETERS_TAB_RULE_FILTER_XPATH,value)






























