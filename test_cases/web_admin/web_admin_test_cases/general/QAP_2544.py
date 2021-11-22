import time
import traceback

from selenium.common.exceptions import TimeoutException

from custom import basic_custom_actions
from test_cases.web_admin.web_admin_core.pages.general.common.common_page import CommonPage
from test_cases.web_admin.web_admin_core.pages.general.settings.settings_page import SettingsPage
from test_cases.web_admin.web_admin_core.pages.login.login_page import LoginPage
from test_cases.web_admin.web_admin_core.pages.root.side_menu import SideMenu
from test_cases.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_2544(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id)
        self.login = "adm02"
        self.password = "adm02"
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
            print(traceback.format_exc() + " Search in ->  " + self.__class__.__name__)
