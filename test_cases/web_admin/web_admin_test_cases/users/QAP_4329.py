import sys
import time
import traceback

from custom import basic_custom_actions
from test_cases.web_admin.web_admin_core.pages.general.common.common_page import CommonPage

from test_cases.web_admin.web_admin_core.pages.login.login_page import LoginPage
from test_cases.web_admin.web_admin_core.pages.root.side_menu import SideMenu
from test_cases.web_admin.web_admin_core.pages.users.users.users_page import UsersPage
from test_cases.web_admin.web_admin_core.pages.users.users.users_user_details_sub_wizard import \
    UsersUserDetailsSubWizard
from test_cases.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_4329(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id)
        self.login = "adm02"
        self.password = "adm02"
        self.user_id = "gbarrett"
        self.first_name = "George"

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
        try:
            self.precondition()
            users_page = UsersPage(self.web_driver_container)
            side_menu = SideMenu(self.web_driver_container)
            user_details_sub_wizard = UsersUserDetailsSubWizard(self.web_driver_container)
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

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
