import sys
import time
import traceback

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.pages.general.common.common_page import CommonPage
from test_framework.web_admin_core.pages.users.users.users_page import UsersPage
from test_framework.web_admin_core.pages.users.users.users_wizard import UsersWizard
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T9443(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")

    def test_context(self):
        login_page = LoginPage(self.web_driver_container)
        side_menu = SideMenu(self.web_driver_container)
        users_page = UsersPage(self.web_driver_container)
        wizard = UsersWizard(self.web_driver_container)
        common_act = CommonPage(self.web_driver_container)

        try:
            login_page.login_to_web_admin(self.login, self.password)
            side_menu.open_users_page()
            users_page.click_on_more_actions()
            users_page.click_on_edit_at_more_actions()
            time.sleep(1)
            common_act.click_on_user_icon()
            common_act.click_on_logout()
            time.sleep(2)
            login_page.login_to_web_admin(self.login, self.password)
            time.sleep(1)
            wizard.click_on_user_header_link()
            time.sleep(1)
            self.verify("Opened the main page of users and and displayed entities",
                        True, users_page.is_users_displayed())

        except Exception:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            errors = f'"{[traceback.extract_tb(exc_traceback, limit=4)]}"'.replace("\\", "/")
            basic_custom_actions.create_event(f"FAILED", self.test_case_id, status='FAILED',
                                              body="[{\"type\": \"message\", \"data\":" + f"{errors}" + "}]")
            traceback.print_tb(exc_traceback, limit=3, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
