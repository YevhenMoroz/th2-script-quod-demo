import sys
import time
import traceback

from custom import basic_custom_actions
from quod_qa.web_admin.web_admin_core.pages.general.common.common_page import CommonPage
from quod_qa.web_admin.web_admin_core.pages.login.login_page import LoginPage
from quod_qa.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer
from quod_qa.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_680(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id)
        self.login = "adm02"
        self.password = "adm02"

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.set_login(self.login)
        login_page.set_password(self.password)
        login_page.click_login_button()
        login_page.check_is_login_successful()

    def test_context(self):
        try:

            self.precondition()
            self.verify("Login successful", True, True)
            time.sleep(2)
            common_page = CommonPage(self.web_driver_container)
            common_page.click_on_user_icon()
            time.sleep(2)
            common_page.click_on_logout()
            self.verify("Logout successful", True, True)

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)