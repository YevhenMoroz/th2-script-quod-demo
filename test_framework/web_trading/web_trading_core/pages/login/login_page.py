import time

from selenium.webdriver.common.keys import Keys
from test_cases.web_admin.web_admin_core.pages.common_page import CommonPage
from test_cases.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_framework.web_trading.web_trading_core.pages.login.login_constants import LoginConstants


class LoginPage(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def set_login(self, login: str):
        login_input = self.find_by_xpath(LoginConstants.LOGIN_INPUT_CSS_SELECTOR)
        login_input.send_keys(Keys.CONTROL + "a")
        login_input.send_keys(Keys.DELETE)
        login_input.send_keys(login)

    def set_password(self, password: str):
        password_input = self.find_by_xpath(LoginConstants.PASSWORD_INPUT_CSS_SELECTOR)
        password_input.send_keys(Keys.CONTROL + "a")
        password_input.send_keys(Keys.DELETE)
        password_input.send_keys(password)

    def click_login_button(self):
        login_button = self.find_by_xpath(LoginConstants.LOGIN_BUTTON_XPATH)
        login_button.click()

    def check_is_web_admin_preloaded(self):
        """
         this method takes the user_name from the loaded web page
        """
        self.find_by_xpath("//*[text()='User']")

    def login_to_web_admin(self, login, password):
        try:
            self.set_login(login)
            self.set_password(password)
            time.sleep(1)
            self.click_login_button()
            self.check_is_web_admin_preloaded()
        except Exception as e:
            print("Login fail" + e.__class__.__name__)

    def get_error_notification(self):
        return self.find_by_xpath(LoginConstants.LOGIN_FAILURE_XPATH).text

    def check_is_login_button_enabled(self):
        return self.is_field_enabled(LoginConstants.LOGIN_BUTTON_XPATH)

    def get_version(self):
        return self.find_by_xpath(LoginConstants.VERSION_XPATH).text

    #region just for reset password test
    #can be using just for one of the application, otherwise need to extend for using
    def write_new_password_if_file(self, path_to_file, password):
            self.write_to_file(path_to_file, password)



    def get_password_from_file(self, path_to_file):
        return self.parse_from_file(path_to_file)
    #endregion