from selenium.webdriver.common.keys import Keys

from test_cases.web_admin.web_admin_core.pages.common_page import CommonPage
from test_cases.web_admin.web_admin_core.pages.middle_office.commissions.commissions_constants import CommissionsConstants
from test_cases.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer


class CommissionsDimensionsSubWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def set_instr_type(self, value):
        self.set_combobox_value(CommissionsConstants.DIMENSIONS_TAB_INSTR_TYPE_XPATH, value)

    def get_instr_type(self):
        return self.get_text_by_xpath(CommissionsConstants.DIMENSIONS_TAB_INSTR_TYPE_XPATH)

    def set_venue(self, value):
        self.set_combobox_value(CommissionsConstants.DIMENSIONS_TAB_VENUE_XPATH, value)

    def get_venue(self):
        return self.get_text_by_xpath(CommissionsConstants.DIMENSIONS_TAB_VENUE_XPATH)

    def set_side(self, value):
        self.set_combobox_value(CommissionsConstants.DIMENSIONS_TAB_SIDE_XPATH, value)

    def get_side(self):
        return self.get_text_by_xpath(CommissionsConstants.DIMENSIONS_TAB_SIDE_XPATH)

    def set_execution_policy(self, value):
        self.set_combobox_value(CommissionsConstants.DIMENSIONS_TAB_EXECUTION_POLICY_XPATH, value)

    def get_execution_policy(self):
        return self.get_text_by_xpath(CommissionsConstants.DIMENSIONS_TAB_EXECUTION_POLICY_XPATH)

    def set_virtual_account(self, value):
        self.set_combobox_value(CommissionsConstants.DIMENSIONS_TAB_VIRTUAL_ACCOUNT_XPATH, value)

    def get_virtual_account(self):
        return self.get_text_by_xpath(CommissionsConstants.DIMENSIONS_TAB_VIRTUAL_ACCOUNT_XPATH)

    def set_client(self, value):
        self.set_combobox_value(CommissionsConstants.DIMENSIONS_TAB_CLIENT_XPATH, value)

    def get_client(self):
        return self.get_text_by_xpath(CommissionsConstants.DIMENSIONS_TAB_CLIENT_XPATH)

    def set_client_group(self, value):
        self.set_combobox_value(CommissionsConstants.DIMENSIONS_TAB_CLIENT_GROUP_XPATH, value)

    def get_client_group(self):
        return self.get_text_by_xpath(CommissionsConstants.DIMENSIONS_TAB_CLIENT_GROUP_XPATH)

    def set_client_list(self, value):
        self.set_combobox_value(CommissionsConstants.DIMENSIONS_TAB_CLIENT_LIST_XPATH, value)

    def get_client_list(self):
        return self.get_text_by_xpath(CommissionsConstants.DIMENSIONS_TAB_CLIENT_LIST_XPATH)

    def set_commission_amount_type(self, value):
        self.set_combobox_value(CommissionsConstants.DIMENSIONS_TAB_COMMISSION_AMOUNT_TYPE_XPATH, value)

    def get_commission_amount_type(self):
        return self.get_text_by_xpath(CommissionsConstants.DIMENSIONS_TAB_COMMISSION_AMOUNT_TYPE_XPATH)

    def set_commission_profile(self, value):
        self.set_combobox_value(CommissionsConstants.DIMENSIONS_TAB_COMMISSION_PROFILE_XPATH, value)

    def get_commission_profile(self):
        return self.get_text_by_xpath(CommissionsConstants.DIMENSIONS_TAB_COMMISSION_PROFILE_XPATH)

    def click_on_manage_commission_profile(self):
        self.find_by_xpath(CommissionsConstants.DIMENSIONS_TAB_MANAGE_COMMISSION_PROFILE_XPATH).click()

    def clear_client_list_field(self):
        self.set_text_by_xpath(CommissionsConstants.DIMENSIONS_TAB_CLIENT_LIST_XPATH," ")

    def is_client_list_contains_text(self):
         return self.find_by_xpath(CommissionsConstants.DIMENSIONS_TAB_CLIENT_LIST_XPATH).get_attribute("value") == ""

