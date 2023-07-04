import time

from test_framework.web_admin_core.pages.general.settings.settings_page import SettingsPage
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T3907(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.settings = "Treshold"

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        side_menu.open_settings_page()
        time.sleep(1)
        settings_page = SettingsPage(self.web_driver_container)
        settings_page.set_settings(self.settings)
        time.sleep(1)

    def test_context(self):

        self.precondition()
        settings_page = SettingsPage(self.web_driver_container)

        self.verify("Row not displayed", False, settings_page.is_setting_displayed())
