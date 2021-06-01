from quod_qa.web_admin.web_admin_core.pages.common_page import CommonPage
from quod_qa.web_admin.web_admin_core.pages.login.login_constants import LoginConstants
from quod_qa.web_admin.web_admin_core.pages.root.root_constants import RootConstants
from quod_qa.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer


class LoginPage(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def set_login(self, login: str):
        login_input = self.find_by_css_selector(LoginConstants.LOGIN_INPUT_CSS_SELECTOR)
        login_input.send_keys(login)

    def set_password(self, password: str):
        password_input = self.find_by_css_selector(LoginConstants.PASSWORD_INPUT_CSS_SELECTOR)
        password_input.send_keys(password)

    def click_login_button(self):
        login_button = self.find_by_xpath(LoginConstants.LOGIN_BUTTON_XPATH)
        login_button.click()

    def check_is_login_successful(self):
        self.find_by_css_selector(RootConstants.HEADER_CONTAINER_CSS_SELECTOR)
