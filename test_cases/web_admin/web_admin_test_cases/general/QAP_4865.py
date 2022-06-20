import sys
import time
import traceback

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.general.common.common_page import CommonPage
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_4865(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        time.sleep(2)
        common_page = CommonPage(self.web_driver_container)
        common_page.click_on_refresh_page_button()
        time.sleep(2)
        common_page.click_on_user_icon()
        time.sleep(2)
        common_page.click_on_logout()
        time.sleep(2)
        login_page.login_to_web_admin(self.login, self.password)

    def test_context(self):

        try:
            self.precondition()
            side_menu = SideMenu(self.web_driver_container)
            try:
                side_menu.open_users_page()
                self.verify("All works correctly", True, True)
            except Exception as e:
                self.verify("Header not active !", True, e.__class__.__name__)

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
