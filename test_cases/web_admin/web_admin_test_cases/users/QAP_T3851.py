import sys
import time
import traceback

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.general.common.common_page import CommonPage
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.pages.users.users.users_page import UsersPage
from test_framework.web_admin_core.pages.users.users.users_wizard import UsersWizard
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T3851(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.user_id = self.data_set.get_user("user_6")

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        time.sleep(2)
        side_menu = SideMenu(self.web_driver_container)
        side_menu.open_users_page()
        time.sleep(2)
        users_page = UsersPage(self.web_driver_container)
        users_page.set_user_id(self.user_id)
        time.sleep(2)

    def check_verify(self):
        users_page = UsersPage(self.web_driver_container)
        if not users_page.is_user_enable_disable():
            users_page.click_on_enable_disable_button()
            time.sleep(2)
            self.verify("User enable", True, users_page.is_user_enable_disable())
        else:
            users_page.click_on_enable_disable_button()
            time.sleep(2)
            self.verify("User disable", False, users_page.is_user_enable_disable())

    def test_context(self):
        try:
            self.precondition()

            users_page = UsersPage(self.web_driver_container)
            users_wizard = UsersWizard(self.web_driver_container)
            common_page = CommonPage(self.web_driver_container)

            self.check_verify()
            common_page.click_on_info_error_message_pop_up()
            time.sleep(1)
            common_page.click_on_user_icon()
            common_page.click_on_logout()
            time.sleep(2)
            login_page = LoginPage(self.web_driver_container)
            login_page.login_to_web_admin(self.login, self.password)
            side_menu = SideMenu(self.web_driver_container)
            time.sleep(2)
            side_menu.open_users_page()
            users_page.set_user_id(self.user_id)
            time.sleep(2)
            self.check_verify()

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
