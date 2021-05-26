from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions

from quod_qa.web_admin.web_admin_core.pages.login.login_constants import LoginConstants
from quod_qa.web_admin.web_admin_core.pages.root.root_constants import RootConstants
from quod_qa.web_admin.web_admin_core.utils.web_driver_utils import find_by_css_selector, find_by_xpath


class LoginPage:
    def __init__(self, web_driver, wait_driver):
        self.web_driver = web_driver
        self.wait_driver = wait_driver

    def set_login(self, login: str):
        login_input = find_by_css_selector(self.wait_driver, LoginConstants.LOGIN_INPUT_CSS_SELECTOR)
        login_input.send_keys(login)

    def set_password(self, password: str):
        password_input = find_by_css_selector(self.wait_driver, LoginConstants.PASSWORD_INPUT_CSS_SELECTOR)
        password_input.send_keys(password)

    def click_login_button(self):
        login_button = find_by_xpath(self.wait_driver, LoginConstants.LOGIN_BUTTON_XPATH)
        login_button.click()

    def check_is_login_successful(self):
        find_by_css_selector(self.wait_driver, RootConstants.HEADER_CONTAINER_CSS_SELECTOR)
