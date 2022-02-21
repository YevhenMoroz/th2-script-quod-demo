import sys
import time
import traceback

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.general.settings.settings_page import SettingsPage
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_2544(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.settings = "CURRENCYSWAPPRICING"

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        side_menu.open_settings_page()
        time.sleep(2)
        settings_page = SettingsPage(self.web_driver_container)
        settings_page.set_settings(self.settings)
        time.sleep(2)

    def test_context(self):

        try:
            self.precondition()
            settings_page = SettingsPage(self.web_driver_container)
            try:
                settings_page.get_settings()
                self.verify("Error", True, True)
            except Exception as e:
                self.verify("Row not displayed , it's ok", "TimeoutException", e.__class__.__name__)

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)

