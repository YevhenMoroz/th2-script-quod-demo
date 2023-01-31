import sys
import time
import traceback

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.general.common.common_page import CommonPage
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T9446(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.url = str
        self.error_message = "You are not logged in, please do refresh and log back in"

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        side_menu.open_users_page()

        common_act = CommonPage(self.web_driver_container)
        self.url = common_act.get_current_page_url()
        self.web_driver_container.stop_driver()
        self.web_driver_container.start_driver()
        self.web_driver_container.web_driver.get(self.url)
        time.sleep(5)

    def test_context(self):
        try:
            self.precondition()

            common_act = CommonPage(self.web_driver_container)
            console_error = common_act.get_console_error()

            self.verify("Only 1 error appears in console", 1, len(console_error))
            self.verify("Error related with login", True, self.error_message in console_error[0]["message"])

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
