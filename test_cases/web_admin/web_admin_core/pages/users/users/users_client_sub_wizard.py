from test_cases.web_admin.web_admin_core.pages.common_page import CommonPage
from test_cases.web_admin.web_admin_core.pages.users.users.users_constants import UsersConstants
from test_cases.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer


class UsersClientSubWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def click_on_plus_button(self):
        self.find_by_xpath(UsersConstants.PLUS_BUTTON_AT_CLIENT_SUB_WIZARD).click()

    def click_on_checkmark_button(self):
        self.find_by_xpath(UsersConstants.CHECKMARK_AT_CLIENT_WIZARD).click()

    def click_on_cancel_button(self):
        self.find_by_xpath(UsersConstants.CANCEL_AT_CLIENT_SUB_WIZARD).click()

    def click_on_edit_button(self):
        self.find_by_xpath(UsersConstants.EDIT_AT_CLIENT_SUB_WIZARD).click()

    def click_on_delete_button(self):
        self.find_by_xpath(UsersConstants.DELETE_AT_CLIENT_SUB_WIZARD).click()

    # get and set
    def set_client(self, value):
        self.set_combobox_value(UsersConstants.CLIENT_AT_CLIENT_SUB_WIZARD, value)

    def get_client(self):
        return self.get_text_by_xpath(UsersConstants.CLIENT_AT_CLIENT_SUB_WIZARD)

    def set_type(self, value):
        self.set_combobox_value(UsersConstants.TYPE_AT_CLIENT_SUB_WIZARD, value)

    def get_type(self):
        return self.get_text_by_xpath(UsersConstants.TYPE_AT_CLIENT_SUB_WIZARD)

    def set_client_filter(self, value):
        self.set_text_by_xpath(UsersConstants.CLIENT_FILTER_AT_CLIENT_SUB_WIZARD, value)

    def set_type_filter(self, value):
        self.set_text_by_xpath(UsersConstants.TYPE_FILTER_AT_CLIENT_SUB_WIZARD, value)

    def is_such_record_already_exist(self):
        return self.find_by_xpath(UsersConstants.RECORD_EXIST_EXCEPTION).text == "Such a record already exists"















