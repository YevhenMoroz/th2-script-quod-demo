from quod_qa.web_admin.web_admin_core.pages.common_page import CommonPage
from quod_qa.web_admin.web_admin_core.pages.users.users.users_constants import UsersConstants
from quod_qa.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer


class UsersLoginSubWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    # get and set

    def set_user_id(self, value):
        self.set_text_by_xpath(UsersConstants.USER_ID_AT_LOGIN_SUB_WIZARD, value)

    def set_password(self, value):
        self.set_text_by_xpath(UsersConstants.PASSWORD_AT_LOGIN_SUB_WIZARD, value)

    def set_ext_id_client(self, value):
        self.set_text_by_xpath(UsersConstants.EXT_ID_CLIENT_AT_LOGIN_SUB_WIZARD, value)

    def get_ext_id_client(self):
        return self.get_text_by_xpath(UsersConstants.EXT_ID_CLIENT_AT_LOGIN_SUB_WIZARD)

    def set_ext_id_venue(self, value):
        self.set_text_by_xpath(UsersConstants.EXT_ID_VENUE_AT_LOGIN_SUB_WIZARD, value)

    def get_ext_id_venue(self):
        return self.get_text_by_xpath(UsersConstants.EXT_ID_VENUE_AT_LOGIN_SUB_WIZARD)

    def set_ext_entitlement_key(self, value):
        self.set_text_by_xpath(UsersConstants.EXT_ENTITLEMENT_AT_LOGIN_SUB_WIZARD, value)

    def get_ext_entitlement_key(self):
        self.get_text_by_xpath(UsersConstants.EXT_ENTITLEMENT_AT_LOGIN_SUB_WIZARD)

    def set_password_expiration(self, value):
        self.set_text_by_xpath(UsersConstants.PASSWORD_EXPIRATION_AT_LOGIN_SUB_WIZARD, value)

    def get_password_expiration(self):
        return self.get_text_by_xpath(UsersConstants.PASSWORD_AT_LOGIN_SUB_WIZARD)

    def set_counterpart(self, value):
        self.set_combobox_value(UsersConstants.COUNTERPART_AT_LOGIN_SUB_WIZARD, value)

    def get_counterpart(self):
        return self.get_text_by_xpath(UsersConstants.COUNTERPART_AT_LOGIN_SUB_WIZARD)

    # checkboxes
    def set_generate_pin_code_checkbox(self):
        self.find_by_xpath(UsersConstants.GENERATE_PIN_CODE_CHECKBOX_AT_LOGIN_SUB_WIZARD).click()

    def is_generate_pin_code_checkbox_selected(self):
        return self.is_checkbox_selected(UsersConstants.GENERATE_PIN_CODE_CHECKBOX_AT_LOGIN_SUB_WIZARD)

    def set_generate_password_checkbox(self):
        self.find_by_xpath(UsersConstants.GENERATE_PASSWORD_CHECKBOX_AT_LOGIN_SUB_WIZARD).click()

    def is_generate_password_checkbox_selected(self):
        return self.is_checkbox_selected(UsersConstants.GENERATE_PASSWORD_CHECKBOX_AT_LOGIN_SUB_WIZARD)

    def set_confirm_follow_up_checkbox(self):
        self.find_by_xpath(UsersConstants.CONFIRM_FOLLOW_UP_CHECKBOX_AT_LOGIN_SUB_WIZARD).click()

    def is_confirm_follow_up_checkbox_selected(self):
        return self.is_checkbox_selected(UsersConstants.CONFIRM_FOLLOW_UP_CHECKBOX_AT_LOGIN_SUB_WIZARD)

    def set_first_time_login_checkbox(self):
        self.find_by_xpath(UsersConstants.FIRST_TIME_LOGIN_CHECKBOX_AT_LOGIN_SUB_WIZARD).click()

    def is_first_time_login_checkbox_selected(self):
        return self.is_checkbox_selected(UsersConstants.FIRST_TIME_LOGIN_CHECKBOX_AT_LOGIN_SUB_WIZARD)

    def set_ping_required_checkbox(self):
        self.find_by_xpath(UsersConstants.PING_REQUIRED_CHECKBOX_AT_LOGIN_SUB_WIZARD).click()

    def is_ping_required_checkbox_selected(self):
        return self.is_checkbox_selected(UsersConstants.PING_REQUIRED_CHECKBOX_AT_LOGIN_SUB_WIZARD)

    # click on
    def click_on_manage_button(self):
        self.find_by_xpath(UsersConstants.MANAGE_AT_LOGIN_SUB_WIZARD).click()
