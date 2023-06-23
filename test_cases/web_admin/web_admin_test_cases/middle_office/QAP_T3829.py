import time

from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.middle_office.commissions.commissions_page import CommissionsPage
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T3829(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        time.sleep(2)
        side_menu.open_commissions_page()
        time.sleep(2)

    def test_context(self):

        self.precondition()
        main_page = CommissionsPage(self.web_driver_container)
        time.sleep(2)
        try:
            main_page.click_on_more_actions()
            time.sleep(2)
            main_page.click_on_delete(True)
            time.sleep(1)
            self.verify("Commission deleted correctly", True, True)
        except Exception:
            self.verify("Commission not deleted", True, False)
