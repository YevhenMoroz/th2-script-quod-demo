import time

from test_framework.mobile_android_core.pages.login.login_constant import LoginConstants
from test_framework.mobile_android_core.utils.common_page import CommonPage
from test_framework.mobile_android_core.utils.driver import AppiumDriver

class LoginPage(CommonPage):
    def __init__(self, driver: AppiumDriver):
        """
        class contains generic methods for communication with elements located on Login Page
        """
        super().__init__(driver)

    def click_field_username(self):
        """
        click on username field
        """
        self.tap(LoginConstants.fieldUsername)

    def click_field_password(self):
        """
        click on password field
        """
        self.tap(LoginConstants.fieldPassword)

    def click_button_login(self):
        """
        click on login button
        """
        self.tap(LoginConstants.buttonLogin)

    def enter_data_field_username(self, data):
        """
        input data in username field
        """
        self.enter_data(LoginConstants.fieldUsername, data)

    def enter_data_field_password(self, data):
        """
        input data in password field
        """
        self.enter_data(LoginConstants.fieldPassword, data)

    def get_text_field_username(self):
        """
        get text of username field
        """
        return self.get_field_text(LoginConstants.fieldUsername)

    def get_text_field_password(self):
        """
        get text of password field
        """
        return self.get_field_text(LoginConstants.fieldPassword)


    # OLD FRAMEWORK
    # def set_email(self, email):
    #     self.wait_element_presence(LoginConstants.EMAIL)
    #     email_input = self.find_by_xpath(LoginConstants.EMAIL)
    #     email_input.click()
    #     self.wait_edit_mode(LoginConstants.EMAIL)
    #     email_input.send_keys(email)
    #
    # def set_password(self, password):
    #     self.wait_element_presence(LoginConstants.PASSWORD)
    #     password_input = self.find_by_xpath(LoginConstants.PASSWORD)
    #     password_input.click()
    #     self.wait_edit_mode(LoginConstants.PASSWORD)
    #     password_input.send_keys(password)
    #
    # def click_on_login_button(self):
    #     self.find_by_xpath(LoginConstants.LOGIN_BUTTON).click()
    #
    # def login_to_mobile_trading(self, email, password):
    #     try:
    #         self.set_email(email)
    #
    #         self.set_password(password)
    #
    #         self.click_on_login_button()
    #     except Exception as e:
    #         print("Login fail " + e.__class__.__name__)


