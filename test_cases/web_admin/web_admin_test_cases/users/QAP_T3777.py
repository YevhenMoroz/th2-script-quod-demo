import random
import string
import sys
import time
import traceback

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.pages.users.users.users_assignments_sub_wizard import UsersAssignmentsSubWizard
from test_framework.web_admin_core.pages.users.users.users_permissions_sub_wizard import UsersPermissionsSubWizard
from test_framework.web_admin_core.pages.users.users.users_values_sub_wizard import UsersValuesSubWizard
from test_framework.web_admin_core.pages.users.users.users_page import UsersPage
from test_framework.web_admin_core.pages.users.users.users_wizard import UsersWizard
from test_framework.web_admin_core.pages.users.users.users_user_details_sub_wizard import UsersUserDetailsSubWizard
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T3777(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.id = 'adm03'
        self.user_id = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.ext_id_client = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.email = self.data_set.get_email("email_1")
        self.desks = [self.data_set.get_desk("desk_1"), self.data_set.get_desk("desk_2")]
        self.perm_role = self.data_set.get_perm_role("perm_role_2")

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        side_menu.open_users_page()
        users_page = UsersPage(self.web_driver_container)
        users_page.set_user_id(self.id)
        time.sleep(1)
        users_page.click_on_more_actions()
        users_page.click_on_clone_at_more_actions()

    def test_context(self):
        try:
            self.precondition()

            user_login_sub_wizard = UsersValuesSubWizard(self.web_driver_container)
            user_login_sub_wizard.set_user_id(self.user_id)
            user_login_sub_wizard.set_ext_id_client(self.ext_id_client)
            user_login_sub_wizard.set_ext_id_venue("")
            user_login_sub_wizard.set_ping_required_checkbox()
            user_details_sub_wizard = UsersUserDetailsSubWizard(self.web_driver_container)
            user_details_sub_wizard.set_mail(self.email)
            assignments_sub_wizard = UsersAssignmentsSubWizard(self.web_driver_container)
            assignments_sub_wizard.clear_assignments_tab()
            time.sleep(1)
            assignments_sub_wizard.click_on_desks()
            assignments_sub_wizard.set_desks(self.desks)
            permissions_sub_wizard = UsersPermissionsSubWizard(self.web_driver_container)
            permissions_sub_wizard.set_perm_role(self.perm_role)
            users_wizard = UsersWizard(self.web_driver_container)
            users_wizard.click_on_save_changes()
            time.sleep(2)
            users_page = UsersPage(self.web_driver_container)
            users_page.set_user_id(self.user_id)
            time.sleep(1)
            self.verify("User correctly cloned", self.user_id, users_page.get_user_id())
        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
