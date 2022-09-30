import time

from selenium.webdriver.common.keys import Keys

from test_framework.web_admin_core.pages.common_page import CommonPage
from test_framework.web_admin_core.pages.login.login_constants import LoginConstants
from test_framework.web_admin_core.pages.root.root_constants import RootConstants
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer


class LoginPage(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def set_login(self, login: str):
        login_input = self.find_by_css_selector(LoginConstants.LOGIN_INPUT_CSS_SELECTOR)
        login_input.send_keys(Keys.CONTROL + "a")
        login_input.send_keys(Keys.DELETE)
        login_input.send_keys(login)

    def set_password(self, password: str):
        password_input = self.find_by_css_selector(LoginConstants.PASSWORD_INPUT_CSS_SELECTOR)
        password_input.send_keys(Keys.CONTROL + "a")
        password_input.send_keys(Keys.DELETE)
        password_input.send_keys(password)

    def click_login_button(self):
        login_button = self.find_by_xpath(LoginConstants.LOGIN_BUTTON_XPATH)
        login_button.click()

    def check_is_login_successful(self):
        self.find_by_css_selector(RootConstants.HEADER_CONTAINER_CSS_SELECTOR)

    def is_login_page_opened(self):
        return self.is_element_present(LoginConstants.LOGIN_PAGE_ADMIN_XPATH)

    def get_unsuccessful_login_message(self):
        return self.find_by_xpath(LoginConstants.LOGIN_ERROR_MESSAGE_XPATH).text

    def login_to_web_admin(self, login, password):
        self.set_login(login)
        self.set_password(password)
        time.sleep(1)
        self.click_login_button()
        self.check_is_login_successful()

    def is_change_password_page_opened(self):
        return self.is_element_present(LoginConstants.CHANGE_PASSWORD_PAGE_XPATH)

    def click_on_forgot_password_link(self):
        self.find_by_xpath(LoginConstants.FORGOT_PASSWORD_LINK_XPATH).click()

    def click_on_back_link(self):
        self.find_by_xpath(LoginConstants.BACK_LINK_XPATH).click()

    def set_email(self, value: str):
        self.set_text_by_xpath(LoginConstants.EMAIL_INPUT_XPATH, value)

    def click_on_reset_password_button(self):
        self.find_by_xpath(LoginConstants.RESET_PASSWORD_BUTTON_XPATH).click()

    def get_change_password_info_message(self):
        return self.find_by_xpath(LoginConstants.CHANGE_PASSWORD_INFO_MESSAGE_XPATH).text

    def get_title_text_of_login_page(self):
        elements_with_text = self.find_elements_by_xpath(LoginConstants.LOGIN_PAGE_TITLE_TEXT_XPATH)
        full_text = ' '.join([elements_with_text[i].text for i in range(len(elements_with_text))])
        return full_text
