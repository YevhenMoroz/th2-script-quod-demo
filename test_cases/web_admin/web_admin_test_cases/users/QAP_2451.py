import sys
import time
import traceback

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.pages.users.users.users_page import UsersPage
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_2451(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.set_login(self.data_set.get_user("user_5"))
        login_page.set_password(self.data_set.get_password("password_2"))
        for i in range(52):
            login_page.click_login_button()
            time.sleep(1)
        login_page.check_is_login_successful()
        login_page.set_login(self.data_set.get_user("user_1"))
        login_page.set_password(self.data_set.get_password("password_1"))
        login_page.click_login_button()
        login_page.check_is_login_successful()
        side_menu = SideMenu(self.web_driver_container)
        time.sleep(2)
        side_menu.open_users_page()
        time.sleep(2)

    def test_context(self):
        try:
            self.precondition()
            users_page = UsersPage(self.web_driver_container)
            users_page.set_user_id(self.data_set.get_user("user_5"))
            time.sleep(2)
            users_page.click_on_lock_unlock_button()
            time.sleep(2)
            self.verify("After click on unlock", "unlock", users_page.get_lock_unlock_status())

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
