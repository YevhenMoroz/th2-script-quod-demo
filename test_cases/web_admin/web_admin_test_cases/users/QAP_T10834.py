import random
import string
import time

from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.pages.users.users.users_user_details_sub_wizard import \
    UsersUserDetailsSubWizard
from test_framework.web_admin_core.pages.users.users.users_assignments_sub_wizard import \
    UsersAssignmentsSubWizard
from test_framework.web_admin_core.pages.users.users.users_permissions_sub_wizard import \
    UsersPermissionsSubWizard
from test_framework.web_admin_core.pages.users.users.users_values_sub_wizard import UsersValuesSubWizard
from test_framework.web_admin_core.pages.users.users.users_page import UsersPage

from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T10834(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")

        self.email = '2@2'
        self.user_id = self.__class__.__name__
        self.ext_id_client = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.institution = self.data_set.get_institution("institution_1")
        self.permission_profile = 'Administrator Permissions'

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        side_menu = SideMenu(self.web_driver_container)

        login_page.login_to_web_admin(self.login, self.password)
        side_menu.open_users_page()

    def test_context(self):
        users_page = UsersPage(self.web_driver_container)
        assignments_tab = UsersAssignmentsSubWizard(self.web_driver_container)
        values_tab = UsersValuesSubWizard(self.web_driver_container)
        details_tab = UsersUserDetailsSubWizard(self.web_driver_container)
        permission_tab = UsersPermissionsSubWizard(self.web_driver_container)

        self.precondition()

        users_page.click_on_new_button()
        values_tab.set_user_id(self.user_id)
        values_tab.set_ext_id_client(self.ext_id_client)
        details_tab.set_mail(self.email)
        assignments_tab.set_institution(self.institution)
        permission_tab.set_permission_profile(self.permission_profile)
        time.sleep(1)
        self.verify("Institution still showing after adding permission",
                    self.institution, assignments_tab.get_institution())
