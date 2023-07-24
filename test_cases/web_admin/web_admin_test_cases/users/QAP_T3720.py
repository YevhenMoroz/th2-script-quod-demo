import time

from test_framework.web_admin_core.pages.general.common.common_page import CommonPage
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.pages.users.users.users_page import UsersPage
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T3720(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.user_id = self.data_set.get_user("user_7")
        self.first_name = self.data_set.get_first_user_name("first_user_name_1")

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        time.sleep(2)
        side_menu.open_users_page()
        time.sleep(2)
        users_page = UsersPage(self.web_driver_container)
        users_page.set_user_id(self.user_id)
        time.sleep(2)
        users_page.click_on_more_actions()
        time.sleep(2)
        users_page.click_on_pin_row_at_more_actions()
        time.sleep(2)

    def test_context(self):
        self.precondition()
        users_page = UsersPage(self.web_driver_container)
        self.verify("Is user {}".format(self.user_id) + " pinned ", self.first_name,
                    users_page.get_first_name())
        users_page.click_on_more_actions()
        time.sleep(2)
        users_page.click_on_unpin_row_at_more_action()
        time.sleep(2)
        common = CommonPage(self.web_driver_container)
        common.click_on_user_icon()
        time.sleep(2)
        common.click_on_dark_theme()
        time.sleep(2)
        users_page.set_user_id(self.user_id)
        time.sleep(2)
        users_page.click_on_more_actions()
        time.sleep(2)
        users_page.click_on_pin_row_at_more_actions()
        self.verify("After click on dark theme. Is user {}".format(self.user_id) + " pinned ", self.first_name,
                    users_page.get_first_name())
        time.sleep(2)
        users_page.click_on_more_actions()
        time.sleep(2)
        users_page.click_on_unpin_row_at_more_action()
