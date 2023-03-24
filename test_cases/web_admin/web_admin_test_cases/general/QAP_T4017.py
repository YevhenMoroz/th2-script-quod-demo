import sys
import time
import traceback

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T4017(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_9")
        self.password = "wrong password"
        self.unsuccessful_message = "logon failure, invalid credentials. Error code=QUOD-17512." \
                                    " If the problem persists, please contact the administrator for full details"

    def test_context(self):
        try:

            login_page = LoginPage(self.web_driver_container)
            login_page.set_login(self.login)
            login_page.set_password(self.password)
            login_page.click_login_button()
            time.sleep(2)

            self.verify("Login unsuccessful", self.unsuccessful_message, login_page.get_unsuccessful_login_message())

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
