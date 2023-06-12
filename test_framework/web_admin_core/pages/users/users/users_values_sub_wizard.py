from test_framework.web_admin_core.pages.common_page import CommonPage
from test_framework.web_admin_core.pages.users.users.users_constants import UsersConstants
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer


class UsersValuesSubWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    # get and set

    def set_user_id(self, value):
        self.set_text_by_xpath(UsersConstants.USER_ID_AT_LOGIN_SUB_WIZARD, value)

    def get_user_id(self):
        return self.get_text_by_xpath(UsersConstants.USER_ID_AT_LOGIN_SUB_WIZARD)

    def set_password(self, value):
        self.set_text_by_xpath(UsersConstants.PASSWORD_AT_LOGIN_SUB_WIZARD, value)

    def set_pin_code(self, value):
        self.set_text_by_xpath(UsersConstants.PIN_CODE_AT_LOGIN_SUB_WIZARD, value)

    def get_pin_code(self):
        return self.get_text_by_xpath(UsersConstants.PIN_CODE_AT_LOGIN_SUB_WIZARD)

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
        return self.get_text_by_xpath(UsersConstants.PASSWORD_EXPIRATION_AT_LOGIN_SUB_WIZARD)

    def set_counterpart(self, value):
        self.set_combobox_value(UsersConstants.COUNTERPART_AT_LOGIN_SUB_WIZARD, value)

    def get_counterpart(self):
        return self.get_text_by_xpath(UsersConstants.COUNTERPART_AT_LOGIN_SUB_WIZARD)

    def set_non_visible_position_flattening_periods(self, value: list):
        self.set_checkbox_list(UsersConstants.NON_VISIBLE_POSITION_FLATTENING_PERIODS, value)

    def get_non_visible_position_flattening_periods(self):
        return self.get_text_by_xpath(UsersConstants.NON_VISIBLE_POSITION_FLATTENING_PERIODS)

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
        return "checked" in self.find_by_xpath(
            UsersConstants.FIRST_TIME_LOGIN_CHECKBOX_AT_LOGIN_SUB_WIZARD).get_attribute("class")

    def set_ping_required_checkbox(self):
        self.find_by_xpath(UsersConstants.PING_REQUIRED_CHECKBOX_AT_LOGIN_SUB_WIZARD).click()

    def is_ping_required_checkbox_selected(self):
        return self.is_checkbox_selected(UsersConstants.PING_REQUIRED_CHECKBOX_AT_LOGIN_SUB_WIZARD)

    # click on
    def click_on_manage_button(self):
        self.find_by_xpath(UsersConstants.MANAGE_AT_LOGIN_SUB_WIZARD).click()

    def click_on_change_password(self):
        self.find_by_xpath(UsersConstants.CHANGE_PASSWORD_BUTTON_AT_LOGIN_SUB_WIZARD).click()

    def set_new_password(self, value):
        self.set_text_by_xpath(UsersConstants.NEW_PASSWORD_AT_LOGIN_SUB_WIZARD, value)

    def set_confirm_new_password(self, value):
        self.set_text_by_xpath(UsersConstants.CONFIRM_NEW_PASSWORD_AT_LOGIN_SUB_WIZARD, value)

    def accept_or_cancel_confirmation_new_password(self, confirm: bool):
        self.find_by_xpath(UsersConstants.CHANGE_PASSWORD_BUTTON_AT_POP_UP_LOGIN_SUB_WIZARD).click() if confirm \
            else self.find_by_xpath(UsersConstants.CANCEL_BUTTON_XPATH).click()

    def get_error_message_text_in_change_password_pop_up(self):
        return self.find_by_xpath(UsersConstants.CHANGE_PASSWORD_POP_UP_ERROR_TEXT).text

    def is_change_password_pop_up_displayed(self):
        return self.is_element_present(UsersConstants.CHANGE_PASSWORD_POP_UP)

    def is_new_password_filed_displayed(self):
        return self.is_element_present(UsersConstants.NEW_PASSWORD_AT_LOGIN_SUB_WIZARD)

    def is_confirm_new_password_field_displayed(self):
        return self.is_element_present(UsersConstants.CONFIRM_NEW_PASSWORD_AT_LOGIN_SUB_WIZARD)
