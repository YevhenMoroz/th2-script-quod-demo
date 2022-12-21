import sys
import time
import traceback

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.pages.general.common.common_page import CommonPage
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.general.settings.settings_page import SettingsPage
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T3881(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)

    def test_context(self):

        try:
            self.precondition()

            common_page = CommonPage(self.web_driver_container)
            current_url = common_page.get_current_page_url()
            common_page.open_new_browser_tab_and_set_url(current_url)
            common_page.click_on_user_icon()
            common_page.click_on_logout()
            common_page.switch_to_browser_tab(0)
            side_menu = SideMenu(self.web_driver_container)
            side_menu.click_on_settings_page_from_side_menu()
            time.sleep(2)
            current_url = common_page.get_current_page_url()
            common_page.open_new_browser_tab_and_set_url(current_url)

            login_page = LoginPage(self.web_driver_container)
            self.verify("Login page is opened", True, login_page.is_login_page_opened())

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
