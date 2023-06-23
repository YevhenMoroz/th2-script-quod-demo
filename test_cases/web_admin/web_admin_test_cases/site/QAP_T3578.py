import time

from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T3578(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)

        self.login = self.data_set.get_user("user_2")
        self.password = self.data_set.get_password("password_2")

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        time.sleep(2)

    def test_context(self):
        self.precondition()

        side_menu = SideMenu(self.web_driver_container)
        side_menu.open_desks_page()
        time.sleep(2)
        self.verify("Only Desks tab displayed",
                    [side_menu.is_institutions_page_tab_displayed(),
                     side_menu.is_zones_page_tab_displayed(),
                     side_menu.is_locations_page_tab_displayed(),
                     side_menu.is_desks_page_tab_displayed()],
                    [False, False, False, True])
