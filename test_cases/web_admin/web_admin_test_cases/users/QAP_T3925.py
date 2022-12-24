import random
import sys
import time
import traceback
import string

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.pages.users.users.users_assignments_sub_wizard import UsersAssignmentsSubWizard
from test_framework.web_admin_core.pages.users.users.users_values_sub_wizard import UsersValuesSubWizard
from test_framework.web_admin_core.pages.users.users.users_page import UsersPage
from test_framework.web_admin_core.pages.users.users.users_permissions_sub_wizard import UsersPermissionsSubWizard
from test_framework.web_admin_core.pages.users.users.users_user_details_sub_wizard import UsersUserDetailsSubWizard
from test_framework.web_admin_core.pages.users.users.users_wizard import UsersWizard
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T3925(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.user_for_clone = self.data_set.get_user("user_7")
        self.ext_id_client = ''.join("EID" + str(random.randint(1, 1000)))
        self.new_user_id = ''.join("UID" + str(random.randint(1, 1000)))
        self.ext_venue_id = ''.join("VID" + str(random.randint(1, 1000)))
        self.perm_role = "Permissions for administrator users"
        self.desk = [self.data_set.get_desk("desk_3"), self.data_set.get_desk("desk_1")]
        self.email = self.data_set.get_email("email_1")
        self.first_name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.last_name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        time.sleep(2)
        side_menu = SideMenu(self.web_driver_container)
        side_menu.open_users_page()
        time.sleep(2)
        users_page = UsersPage(self.web_driver_container)
        users_page.set_user_id(self.user_for_clone)
        time.sleep(2)
        users_page.click_on_more_actions()
        time.sleep(1)
        users_page.click_on_clone_at_more_actions()
        time.sleep(2)
        login_sub_wizard = UsersValuesSubWizard(self.web_driver_container)
        login_sub_wizard.set_user_id(self.new_user_id)
        login_sub_wizard.set_ext_id_client(self.ext_id_client)
        login_sub_wizard.set_ext_id_venue(self.ext_venue_id)
        login_sub_wizard.set_password_expiration("")
        details_tab = UsersUserDetailsSubWizard(self.web_driver_container)
        details_tab.set_first_name(self.first_name)
        details_tab.set_last_name(self.last_name)
        details_tab.set_mail(self.email)
        assignments_tab = UsersAssignmentsSubWizard(self.web_driver_container)
        assignments_tab.click_on_desks()
        time.sleep(1)
        assignments_tab.set_desks(self.desk)
        time.sleep(1)
        assignments_tab.click_on_desks()
        time.sleep(1)
        permission_tab = UsersPermissionsSubWizard(self.web_driver_container)
        permission_tab.set_perm_role(self.perm_role)
        time.sleep(1)
        users_wizard = UsersWizard(self.web_driver_container)
        users_wizard.click_on_save_changes()

    def test_context(self):
        try:
            self.precondition()

            users_page = UsersPage(self.web_driver_container)
            users_page.set_user_id(self.new_user_id)
            time.sleep(1)

            self.verify("User has been cloned", self.new_user_id, users_page.get_user_id())
        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
