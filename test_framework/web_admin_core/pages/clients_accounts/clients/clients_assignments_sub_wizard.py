import time
from test_framework.web_admin_core.pages.clients_accounts.clients.clients_constants import ClientsConstants
from test_framework.web_admin_core.pages.common_page import CommonPage
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer


class ClientsAssignmentsSubWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def set_user_manager(self, value):
        self.set_combobox_value(ClientsConstants.ASSIGNMENTS_TAB_USER_MANAGER_XPATH, value)

    def get_user_manager(self):
        return self.get_text_by_xpath(ClientsConstants.ASSIGNMENTS_TAB_USER_MANAGER_XPATH)

    def get_all_user_manager_from_drop_menu(self):
        self.set_text_by_xpath(ClientsConstants.ASSIGNMENTS_TAB_USER_MANAGER_XPATH, "")
        time.sleep(1)
        return self.get_all_items_from_drop_down(ClientsConstants.DROP_DOWN_MENU_XPATH)

    def is_user_manager_field_displayed_and_has_correct_name(self):
        return self.is_element_present(ClientsConstants.ASSIGNMENTS_TAB_USER_MANAGER_LABEL_XPATH)

    def set_desk(self, value):
        self.set_multiselect_field_value(ClientsConstants.ASSIGNMENTS_TAB_DESK_XPATH, value)

    def get_desk(self):
        return self.get_text_by_xpath(ClientsConstants.ASSIGNMENTS_TAB_DESK_XPATH)

    def is_desk_field_displayed_and_has_correct_name(self):
        return self.is_element_present(ClientsConstants.ASSIGNMENTS_TAB_DESK_LABEL_XPATH)

    def click_on_account_link(self, account_name):
        self.find_by_xpath(ClientsConstants.ASSIGNMENTS_TAB_ACCOUNT_NAME_XPATH.format(account_name)).click()

    def click_on_client_list_link(self, client_list_name):
        self.find_by_xpath(ClientsConstants.ASSIGNMENTS_TAB_ACCOUNT_NAME_XPATH.format(client_list_name)).click()

    def get_all_assigned_accounts(self) -> list:
        return [_.text.strip() for _ in self.find_elements_by_xpath(ClientsConstants.ASSIGNMENTS_TAB_ACCOUNTS_XPATH)]
    
    def get_all_assigned_client_lists(self) -> list:
        return [_.text.strip() for _ in self.find_elements_by_xpath(ClientsConstants.ASSIGNMENTS_TAB_CLIENT_LISTS_XPATH)]

