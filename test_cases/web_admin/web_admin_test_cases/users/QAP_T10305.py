import time

from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.pages.general.common.common_page import CommonPage
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T10305(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)

        login_page.login_to_web_admin(self.login, self.password)

    def test_context(self):
        side_menu = SideMenu(self.web_driver_container)
        common_page = CommonPage(self.web_driver_container)
        login_page = LoginPage(self.web_driver_container)

        self.precondition()

        side_menu.open_users_page()
        time.sleep(2)
        current_url = common_page.get_current_page_url()
        common_page.open_new_browser_tab_and_set_url(current_url)
        common_page.click_on_user_icon()
        common_page.click_on_logout()
        time.sleep(2)
        common_page.switch_to_browser_tab_or_window(0)
        side_menu.click_user_lists_tab()
        time.sleep(2)

        self.verify("Login page is opened", True, login_page.is_login_page_opened())
