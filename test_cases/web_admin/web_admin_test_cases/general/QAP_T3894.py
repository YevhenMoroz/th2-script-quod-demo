import time

from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.pages.general.common.common_page import CommonPage
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.general.settings.settings_page import SettingsPage
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T3894(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        time.sleep(2)

    def test_context(self):

        self.precondition()

        side_menu = SideMenu(self.web_driver_container)
        side_menu.open_settings_page()
        time.sleep(2)

        common_page = CommonPage(self.web_driver_container)
        common_page.refresh_page(True)

        settings_page = SettingsPage(self.web_driver_container)
        self.verify("Page is not changed after reload", True, settings_page.is_title_page_displayed())

        current_url = common_page.get_current_page_url()
        common_page.open_new_browser_tab_and_set_url(current_url)

        time.sleep(2)
        self.verify("Users page of WebAdmin is opened, login page is not displayed, login is not requested.",
                    True, settings_page.is_title_page_displayed())
