import time

from test_framework.web_admin_core.pages.common_page import CommonPage
from test_framework.web_admin_core.pages.middle_office.commissions.commissions_constants import CommissionsConstants
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer


class CommissionsDimensionsSubWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def set_instr_type(self, value):
        self.select_value_from_dropdown_list(CommissionsConstants.DIMENSIONS_TAB_INSTR_TYPE_XPATH, value)

    def get_instr_type(self):
        return self.get_text_by_xpath(CommissionsConstants.DIMENSIONS_TAB_INSTR_TYPE_XPATH)
    
    def get_all_instr_types_from_drop_menu(self):
        self.find_by_xpath(CommissionsConstants.DIMENSIONS_TAB_INSTR_TYPE_XPATH).click()
        time.sleep(1)
        return self.get_all_items_from_drop_down(CommissionsConstants.DROP_DOWN_MENU_XPATH)

    def set_venue(self, value):
        self.set_combobox_value(CommissionsConstants.DIMENSIONS_TAB_VENUE_XPATH, value)

    def get_venue(self):
        return self.get_text_by_xpath(CommissionsConstants.DIMENSIONS_TAB_VENUE_XPATH)
    
    def get_all_venues_from_drop_menu(self):
        self.find_by_xpath(CommissionsConstants.DIMENSIONS_TAB_VENUE_XPATH).click()
        time.sleep(1)
        return self.get_all_items_from_drop_down(CommissionsConstants.DROP_DOWN_MENU_XPATH)

    def set_venue_list(self, value):
        self.set_combobox_value(CommissionsConstants.VALUES_TAB_VENUE_LIST_XPATH, value)

    def get_venue_list(self):
        return self.get_text_by_xpath(CommissionsConstants.VALUES_TAB_VENUE_LIST_XPATH)

    def get_all_venue_list_from_drop_menu(self):
        self.find_by_xpath(CommissionsConstants.VALUES_TAB_VENUE_LIST_XPATH).click()
        time.sleep(2)
        return self.get_all_items_from_drop_down(CommissionsConstants.DROP_DOWN_MENU_XPATH)

    def is_venue_list_field_displayed(self):
        return self.is_element_present(CommissionsConstants.VALUES_TAB_VENUE_LIST_XPATH)

    def set_side(self, value):
        self.select_value_from_dropdown_list(CommissionsConstants.DIMENSIONS_TAB_SIDE_XPATH, value)

    def get_side(self):
        return self.get_text_by_xpath(CommissionsConstants.DIMENSIONS_TAB_SIDE_XPATH)

    def get_all_side_from_drop_menu(self):
        self.find_by_xpath(CommissionsConstants.DIMENSIONS_TAB_SIDE_XPATH).click()
        time.sleep(1)
        return self.get_all_items_from_drop_down(CommissionsConstants.DROP_DOWN_MENU_XPATH)

    def set_execution_policy(self, value):
        self.select_value_from_dropdown_list(CommissionsConstants.DIMENSIONS_TAB_EXECUTION_POLICY_XPATH, value)

    def get_execution_policy(self):
        return self.get_text_by_xpath(CommissionsConstants.DIMENSIONS_TAB_EXECUTION_POLICY_XPATH)

    def get_all_execution_policy_from_drop_menu(self):
        self.find_by_xpath(CommissionsConstants.DIMENSIONS_TAB_EXECUTION_POLICY_XPATH).click()
        time.sleep(1)
        return self.get_all_items_from_drop_down(CommissionsConstants.DROP_DOWN_MENU_XPATH)

    def set_virtual_account(self, value):
        self.set_combobox_value(CommissionsConstants.DIMENSIONS_TAB_VIRTUAL_ACCOUNT_XPATH, value)

    def get_virtual_account(self):
        return self.get_text_by_xpath(CommissionsConstants.DIMENSIONS_TAB_VIRTUAL_ACCOUNT_XPATH)

    def set_client(self, value):
        self.set_combobox_value(CommissionsConstants.DIMENSIONS_TAB_CLIENT_XPATH, value)

    def get_client(self):
        return self.get_text_by_xpath(CommissionsConstants.DIMENSIONS_TAB_CLIENT_XPATH)

    def get_all_client_from_drop_menu(self):
        self.find_by_xpath(CommissionsConstants.DIMENSIONS_TAB_CLIENT_XPATH).click()
        time.sleep(1)
        return self.get_all_items_from_drop_down(CommissionsConstants.DROP_DOWN_MENU_XPATH)

    def set_client_group(self, value):
        self.set_combobox_value(CommissionsConstants.DIMENSIONS_TAB_CLIENT_GROUP_XPATH, value)

    def get_client_group(self):
        return self.get_text_by_xpath(CommissionsConstants.DIMENSIONS_TAB_CLIENT_GROUP_XPATH)

    def set_client_list(self, value):
        self.set_combobox_value(CommissionsConstants.DIMENSIONS_TAB_CLIENT_LIST_XPATH, value)

    def get_client_list(self):
        return self.get_text_by_xpath(CommissionsConstants.DIMENSIONS_TAB_CLIENT_LIST_XPATH)

    def get_all_client_list_from_drop_menu(self):
        self.find_by_xpath(CommissionsConstants.DIMENSIONS_TAB_CLIENT_LIST_XPATH).click()
        time.sleep(1)
        return self.get_all_items_from_drop_down(CommissionsConstants.DROP_DOWN_MENU_XPATH)

    def clear_client_list_field(self):
        self.set_text_by_xpath(CommissionsConstants.DIMENSIONS_TAB_CLIENT_LIST_XPATH, "")

    def is_client_list_contains_text(self):
         return self.find_by_xpath(CommissionsConstants.DIMENSIONS_TAB_CLIENT_LIST_XPATH).get_attribute("value") == ""

