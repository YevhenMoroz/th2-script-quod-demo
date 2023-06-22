import random
import string
import time

from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.pages.users.users.users_assignments_sub_wizard import UsersAssignmentsSubWizard
from test_framework.web_admin_core.pages.users.users.users_values_sub_wizard import UsersValuesSubWizard
from test_framework.web_admin_core.pages.users.users.users_user_details_sub_wizard import UsersUserDetailsSubWizard
from test_framework.web_admin_core.pages.users.users.users_page import UsersPage
from test_framework.web_admin_core.pages.users.users.users_wizard import UsersWizard
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T3688(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.client = self.data_set.get_client("client_1")
        self.user_id = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.ext_id_client = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.type = self.data_set.get_client_type("client_type_1")
        self.desks = [self.data_set.get_desk("desk_1"), self.data_set.get_desk("desk_3")]
        self.email = self.data_set.get_email("email_1")

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        time.sleep(2)
        side_menu = SideMenu(self.web_driver_container)
        side_menu.open_users_page()
        time.sleep(2)
        users_page = UsersPage(self.web_driver_container)
        users_page.click_on_new_button()
        time.sleep(2)
        user_login_sub_wizard = UsersValuesSubWizard(self.web_driver_container)
        user_login_sub_wizard.set_user_id(self.user_id)
        user_login_sub_wizard.set_ext_id_client(self.ext_id_client)
        time.sleep(1)
        user_login_sub_wizard.set_ping_required_checkbox()
        time.sleep(1)
        user_details_sub_wizard = UsersUserDetailsSubWizard(self.web_driver_container)
        user_details_sub_wizard.set_mail(self.email)
        time.sleep(1)
        assignments_sub_wizard = UsersAssignmentsSubWizard(self.web_driver_container)
        assignments_sub_wizard.click_on_desks()
        time.sleep(1)
        assignments_sub_wizard.set_desks(self.desks)
        time.sleep(1)

    def test_context(self):
        self.precondition()
        users_wizard = UsersWizard(self.web_driver_container)
        try:
            users_wizard.click_on_save_changes()
            time.sleep(2)
            users_page = UsersPage(self.web_driver_container)
            users_page.set_user_id(self.user_id)
            time.sleep(2)
            self.verify("New user saved correctly", self.user_id, users_page.get_user_id())
        except Exception as e:
            self.verify("New user not saved", True, e.__class__.__name__)
