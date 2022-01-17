import sys
import time
import traceback

from custom import basic_custom_actions
from test_cases.web_admin.web_admin_core.pages.login.login_page import LoginPage
from test_cases.web_admin.web_admin_core.pages.root.side_menu import SideMenu
from test_cases.web_admin.web_admin_core.pages.users.users.users_page import UsersPage
from test_cases.web_admin.web_admin_core.pages.users.users.users_role_sub_wizard import UsersRoleSubWizard
from test_cases.web_admin.web_admin_core.pages.users.users.users_user_details_sub_wizard import UsersUserDetailsSubWizard
from test_cases.web_admin.web_admin_core.pages.users.users.users_wizard import UsersWizard
from test_cases.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_3145(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id)
        self.user_id = "adm03"
        self.perm_role = "Permissions for FIX Clients"
        self.email = "test"

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.set_login("adm02")
        login_page.set_password("adm02")
        login_page.click_login_button()
        login_page.check_is_login_successful()
        side_menu = SideMenu(self.web_driver_container)
        time.sleep(2)
        side_menu.open_users_page()
        time.sleep(2)
        users_page = UsersPage(self.web_driver_container)
        users_page.set_user_id(self.user_id)
        time.sleep(3)
        users_page.click_on_more_actions()
        time.sleep(2)
        users_page.click_on_edit_at_more_actions()
        time.sleep(2)

    def test_context(self):
        try:
            self.precondition()
            role_wizard = UsersRoleSubWizard(self.web_driver_container)
            users_page = UsersPage(self.web_driver_container)
            details_sub_wizard = UsersUserDetailsSubWizard(self.web_driver_container)
            details_sub_wizard.set_mail(self.email)
            time.sleep(1)
            role_wizard.set_perm_role(self.perm_role)
            wizard = UsersWizard(self.web_driver_container)
            wizard.click_on_save_changes()
            time.sleep(2)
            users_page.set_user_id(self.user_id)
            time.sleep(3)
            users_page.click_on_more_actions()
            time.sleep(2)
            users_page.click_on_edit_at_more_actions()
            time.sleep(2)
            self.verify("Is Perm Role saved correctly ?", self.perm_role, role_wizard.get_perm_role())
        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
