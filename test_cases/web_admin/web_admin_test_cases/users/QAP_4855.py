import random
import string
import sys
import time
import traceback

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.pages.users.users.users_assignments_sub_wizard import UsersAssignmentsSubWizard
from test_framework.web_admin_core.pages.users.users.users_login_sub_wizard import UsersLoginSubWizard
from test_framework.web_admin_core.pages.users.users.users_page import UsersPage
from test_framework.web_admin_core.pages.users.users.users_wizard import UsersWizard
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_4855(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.client = self.data_set.get_client("client_1")
        self.user_id = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.type = self.data_set.get_client_type("client_type_1")
        self.desks = [self.data_set.get_desk("desk_1"), self.data_set.get_desk("desk_3")]

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        time.sleep(2)
        side_menu.open_users_page()
        users_page = UsersPage(self.web_driver_container)
        time.sleep(2)
        users_page.click_on_new_button()
        time.sleep(2)
        user_login_sub_wizard = UsersLoginSubWizard(self.web_driver_container)
        user_login_sub_wizard.set_user_id(self.user_id)
        time.sleep(1)
        user_login_sub_wizard.set_generate_pin_code_checkbox()
        time.sleep(1)
        user_login_sub_wizard.set_generate_password_checkbox()
        assignments_sub_wizard = UsersAssignmentsSubWizard(self.web_driver_container)
        time.sleep(1)
        assignments_sub_wizard.click_on_desks()
        time.sleep(1)
        assignments_sub_wizard.set_desks(self.desks)
        time.sleep(1)

    def test_context(self):
        try:
            self.precondition()
            users_wizard = UsersWizard(self.web_driver_container)
            try:
                users_wizard.click_on_save_changes()
                self.verify("New user saved correctly", True, True)
            except Exception as e:
                self.verify("New user not saved", True, e.__class__.__name__)

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
