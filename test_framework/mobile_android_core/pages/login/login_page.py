from test_framework.mobile_android_core.pages.login.login_constant import LoginConstants
from test_framework.mobile_android_core.utils.common_page import CommonPage
from test_framework.mobile_android_core.utils.driver import AppiumDriver

class LoginPage(CommonPage):
    def __init__(self, driver: AppiumDriver):
        super().__init__(driver)

    def set_email(self, email):
        self.Waiter.WaitUntilClickableByXPath(LoginConstants.EMAIL)
        email_input = self.find_by_xpath(LoginConstants.EMAIL)
        email_input.click()
        self.appium_driver.wait_time(1)
        email_input.send_keys(email)

    def set_password(self, password):
        self.Waiter.WaitUntilClickableByXPath(LoginConstants.PASSWORD)
        password_input = self.find_by_xpath(LoginConstants.PASSWORD)
        password_input.click()
        self.appium_driver.wait_time(1)
        password_input.send_keys(password)

    def click_on_login_button(self):
        self.find_by_xpath(LoginConstants.LOGIN_BUTTON).click()

    def login_to_mobile_trading(self, email, password):
        try:
            self.set_email(email)
            self.appium_driver.wait_time(1)

            self.set_password(password)
            self.appium_driver.wait_time(1)

            self.click_on_login_button()
        except Exception as e:
            print("Login fail " + e.__class__.__name__)


