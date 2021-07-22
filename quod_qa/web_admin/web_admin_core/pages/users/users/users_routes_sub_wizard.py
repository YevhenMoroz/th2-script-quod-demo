from quod_qa.web_admin.web_admin_core.pages.common_page import CommonPage
from quod_qa.web_admin.web_admin_core.pages.users.users.users_constants import UsersConstants
from quod_qa.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer


class UsersRoutesSubWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def click_on_plus_button(self):
        self.find_by_xpath(UsersConstants.PLUS_BUTTON_AT_ROUTES_SUB_WIZARD).click()

    def click_on_checkmark_button(self):
        self.find_by_xpath(UsersConstants.CHECKMARK_AT_ROUTES_SUB_WIZARD).click()

    def click_on_cancel_button(self):
        self.find_by_xpath(UsersConstants.CANCEL_AT_ROUTES_SUB_WIZARD).click()

    def click_on_edit_button(self):
        self.find_by_xpath(UsersConstants.EDIT_AT_ROUTES_SUB_WIZARD).click()

    def click_on_delete_button(self):
        self.find_by_xpath(UsersConstants.DELETE_AT_ROUTES_WIZARD).click()

    # set and get

    def set_route(self, value):
        self.set_combobox_value(UsersConstants.ROUTE_AT_ROUTES_SUB_WIZARD, value)

    def get_route(self):
        return self.get_text_by_xpath(UsersConstants.ROUTE_AT_ROUTES_SUB_WIZARD)

    def set_route_user_name(self, value):
        self.set_text_by_xpath(UsersConstants.ROUTE_USER_NAME_AT_ROUTES_SUB_WIZARD, value)

    def get_route_user_name(self):
        return self.get_text_by_xpath(UsersConstants.ROUTE_USER_NAME_AT_ROUTES_SUB_WIZARD)

    # filters

    def set_route_filter(self, value):
        self.set_text_by_xpath(UsersConstants.ROUTE_FILTER_AT_ROUTES_SUB_WIZARD, value)

    def set_route_user_name_filter(self, value):
        self.set_text_by_xpath(UsersConstants.ROUTE_USER_NAME_FILTER_AT_ROUTES_SUB_WIZARD, value)
