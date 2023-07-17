import time

from selenium.webdriver import ActionChains

from test_framework.web_admin_core.pages.common_page import CommonPage
from test_framework.web_admin_core.pages.users.users.users_constants import UsersConstants
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer


class UsersRoutesSubWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def click_on_plus_button(self):
        """
        ActionChains helps to avoid falling test when adding several quantities at once.
        (The usual "click" method fails because after adding the first entry, the cursor remains on the "edit" button
        and the pop-up of edit btn covers half of the "+" button)
        """
        element = self.find_by_xpath(UsersConstants.PLUS_BUTTON_AT_ROUTES_SUB_WIZARD)
        action = ActionChains(self.web_driver_container.get_driver())
        action.move_to_element(element)
        action.click()
        action.perform()

    def click_on_checkmark_button(self):
        self.find_by_xpath(UsersConstants.CHECKMARK_AT_ROUTES_SUB_WIZARD).click()

    def click_on_cancel_button(self):
        self.find_by_xpath(UsersConstants.CANCEL_AT_ROUTES_SUB_WIZARD).click()

    def click_on_edit_button(self):
        self.find_by_xpath(UsersConstants.EDIT_AT_ROUTES_SUB_WIZARD).click()

    def click_on_delete_button(self):
        self.find_by_xpath(UsersConstants.DELETE_AT_ROUTES_WIZARD).click()

    def click_on_delete_button_for_last_entry_in_table(self):
        self.find_by_xpath(UsersConstants.DELETE_LAST_ENTRY_AT_ROUTE_WIZARD).click()

    # set and get

    def set_route(self, value):
        self.set_combobox_value(UsersConstants.ROUTE_AT_ROUTES_SUB_WIZARD, value)

    def get_route(self):
        return self.get_text_by_xpath(UsersConstants.ROUTE_AT_ROUTES_SUB_WIZARD)

    def get_all_routes_from_drop_menu(self):
        self.set_text_by_xpath(UsersConstants.ROUTE_AT_ROUTES_SUB_WIZARD, "")
        time.sleep(1)
        return self.get_all_items_from_drop_down(UsersConstants.DROP_DOWN_MENU_XPATH)

    def get_all_route_in_table(self):
        return self.get_all_items_from_table_column(UsersConstants.ROUTE_IN_ROUTE_TABLE_SUB_WIZARD)

    def set_route_user_name(self, value):
        self.set_text_by_xpath(UsersConstants.ROUTE_USER_NAME_AT_ROUTES_SUB_WIZARD, value)

    def get_route_user_name(self):
        return self.get_text_by_xpath(UsersConstants.ROUTE_USER_NAME_AT_ROUTES_SUB_WIZARD)

    # filters

    def set_route_filter(self, value):
        self.set_text_by_xpath(UsersConstants.ROUTE_FILTER_AT_ROUTES_SUB_WIZARD, value)

    def set_route_user_name_filter(self, value):
        self.set_text_by_xpath(UsersConstants.ROUTE_USER_NAME_FILTER_AT_ROUTES_SUB_WIZARD, value)
