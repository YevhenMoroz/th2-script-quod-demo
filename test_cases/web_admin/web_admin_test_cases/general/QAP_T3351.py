import time

from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T3351(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.email = 'test@test'

    def test_context(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.click_on_forgot_password_link()
        time.sleep(1)
        login_page.click_on_back_link()
        self.verify("Main page open", True, login_page.is_login_page_opened())

        login_page.click_on_forgot_password_link()
        time.sleep(1)
        login_page.set_email(self.email)
        login_page.click_on_reset_password_button()
        time.sleep(2)

        self.verify("Main page open", True, login_page.is_login_page_opened())
        self.verify("After change password info message is appears",
                    "A password reset link has been sent.",
                    login_page.get_change_password_info_message())

