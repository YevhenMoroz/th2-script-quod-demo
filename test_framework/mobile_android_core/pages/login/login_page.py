from test_framework.mobile_android_core.pages.login.login_constant import LoginConstants
from test_framework.mobile_android_core.utils.common_page import CommonPage
from test_framework.mobile_android_core.utils.driver import AppiumDriver
from test_framework.mobile_android_core.utils.waits import Waits

class LoginPage(CommonPage):
    def __init__(self, driver: AppiumDriver):
        super().__init__(driver)
        self.Waiter = Waits(self.appium_driver.appium_driver,5)

    def set_email(self, email):
        self.Waiter.WaitUntilClickableByXPath(LoginConstants.EMAIL)
        email_input = self.find_by_xpath(LoginConstants.EMAIL)
        email_input.click()
        self.appium_driver.wait_time(1)
        email_input.send_keys(email)

    def set_password(self, password):
        password_input = self.find_by_xpath(LoginConstants.PASSWORD)
        password_input.click()
        # time.sleep(1)
        # self.appium_driver.wait_time(1)
        self.appium_driver.wait_time(1)
        # self.appium_driver.implicitly_wait(1)
        password_input.send_keys(password)

    def click_on_continue_button(self):
        self.find_by_xpath(LoginConstants.CONTINUE).click()

    def click_on_login_button(self):
        self.find_by_xpath(LoginConstants.LOGIN_BUTTON).click()

    def login_to_mobile_trading(self, email, password):
        try:
            self.set_email(email)
            self.appium_driver.wait_time(1)
            # self.appium_driver.implicitly_wait(1)
            self.click_on_continue_button()
            self.appium_driver.wait_time(1)
            # self.appium_driver.implicitly_wait(1)
            self.set_password(password)
            self.appium_driver.wait_time(1)
            # self.appium_driver.implicitly_wait(1)
            self.click_on_login_button()
        except Exception as e:
            print("Login fail " + e.__class__.__name__)

    # def get_attribute_email(self, name):
    #     try:
    #         return self.get_attribute_of_element_by_xpath(LoginConstants.EMAIL_LOGIN, name)
    #     except Exception as e:
    #         print(e)
    #
    # def get_attribute_auth(self, name):
    #     try:
    #         return self.get_attribute_of_element_by_xpath(LoginConstants.AUTHENTICATION_FAILURE, name)
    #     except Exception as e:
    #         print(e)
    #
    # def get_attribute_incorrect_password(self, name):
    #     try:
    #         return self.get_attribute_of_element_by_xpath(LoginConstants.INCORRECT_PASSWORD, name)
    #     except Exception as e:
    #         print(e)
    #
    # def get_attribute_invalid_email(self, name):
    #     try:
    #         # print(self.get_element_by_xpath(LoginConstants.EMAIL_LOGIN, "clickable"))
    #         return self.get_attribute_of_element_by_xpath(LoginConstants.INVALID_EMAIL, name)
    #     except Exception as e:
    #         print(e)

    def open_login_page(self, email):
        try:
            self.set_email(email)
            self.appium_driver.wait_time(1)
            # self.appium_driver.implicitly_wait(1)
            self.click_on_continue_button()

        except Exception as e:
            print("Login fail " + e.__class__.__name__)


