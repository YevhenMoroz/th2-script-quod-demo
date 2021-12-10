import random
import sys
import time
import traceback

from custom import basic_custom_actions
from test_cases.web_admin.web_admin_core.pages.login.login_page import LoginPage
from test_cases.web_admin.web_admin_core.pages.root.side_menu import SideMenu
from test_cases.web_admin.web_admin_core.pages.users.users.users_assignments_sub_wizard import UsersAssignmentsSubWizard
from test_cases.web_admin.web_admin_core.pages.users.users.users_login_sub_wizard import UsersLoginSubWizard
from test_cases.web_admin.web_admin_core.pages.users.users.users_page import UsersPage
from test_cases.web_admin.web_admin_core.pages.users.users.users_role_sub_wizard import UsersRoleSubWizard
from test_cases.web_admin.web_admin_core.pages.users.users.users_user_details_sub_wizard import UsersUserDetailsSubWizard
from test_cases.web_admin.web_admin_core.pages.users.users.users_wizard import UsersWizard
from test_cases.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_2405(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id)
        self.login = "adm02"
        self.password = "adm02"
        self.user_id = ''.join("test " + str(random.randint(1, 1000)))
        self.password_at_login_wizard = ''.join("pass" + str(random.randint(1, 1000)))
        self.perm_role = "Permissions for administrator users"
        self.desks = ("DESK A", "Quod Desk")
        self.new_user_id = ''.join("id" + str(random.randint(1, 1000)))
        self.new_password = ''.join("pass" + str(random.randint(1, 1000)))
        self.pin_code = "333"
        self.email = "test"

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        time.sleep(2)
        side_menu.open_users_page()
        users_page = UsersPage(self.web_driver_container)
        time.sleep(2)
        users_page.click_on_new_button()
        login_sub_wizard = UsersLoginSubWizard(self.web_driver_container)
        time.sleep(2)
        login_sub_wizard.set_user_id(self.user_id)
        time.sleep(2)
        login_sub_wizard.set_pin_code(self.pin_code)
        time.sleep(1)
        login_sub_wizard.set_password(self.password)
        time.sleep(2)
        role_sub_wizard = UsersRoleSubWizard(self.web_driver_container)
        role_sub_wizard.set_perm_role(self.perm_role)
        time.sleep(2)
        assignments_sub_wizard = UsersAssignmentsSubWizard(self.web_driver_container)
        assignments_sub_wizard.click_on_desks()
        time.sleep(2)
        user_details_sub_wizard = UsersUserDetailsSubWizard(self.web_driver_container)
        user_details_sub_wizard.set_mail(self.email)
        time.sleep(1)
        assignments_sub_wizard.set_desks(self.desks)
        time.sleep(1)
        users_wizard = UsersWizard(self.web_driver_container)
        users_wizard.click_on_save_changes()
        time.sleep(3)
        users_page.set_user_id(self.user_id)
        time.sleep(2)
        users_page.click_on_more_actions()
        users_page.click_on_clone_at_more_actions()
        time.sleep(2)
        login_sub_wizard.set_user_id(self.new_user_id)
        time.sleep(2)
        login_sub_wizard.set_pin_code(self.pin_code)
        time.sleep(2)
        login_sub_wizard.set_password(self.new_password)
        time.sleep(2)
        login_sub_wizard.set_password_expiration("11/10/2022")
        time.sleep(1)
        users_wizard.click_on_save_changes()
        time.sleep(2)
        users_wizard.click_on_logout_button()
        time.sleep(3)
        login_page.login_to_web_admin(self.new_user_id, self.new_password)
        time.sleep(2)

    def test_context(self):
        try:
            self.precondition()
            login_page = LoginPage(self.web_driver_container)
            self.verify("Login to web adm with new user", True, login_page.check_is_web_admin_preloaded())
        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
