import random
import string
import time
import traceback

from custom import basic_custom_actions
from quod_qa.web_admin.web_admin_core.pages.login.login_page import LoginPage
from quod_qa.web_admin.web_admin_core.pages.root.side_menu import SideMenu
from quod_qa.web_admin.web_admin_core.pages.users.users.users_assignments_sub_wizard import UsersAssignmentsSubWizard
from quod_qa.web_admin.web_admin_core.pages.users.users.users_login_sub_wizard import UsersLoginSubWizard
from quod_qa.web_admin.web_admin_core.pages.users.users.users_page import UsersPage
from quod_qa.web_admin.web_admin_core.pages.users.users.users_role_sub_wizard import UsersRoleSubWizard
from quod_qa.web_admin.web_admin_core.pages.users.users.users_wizard import UsersWizard
from quod_qa.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer
from quod_qa.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_4239(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id)
        self.login = "adm02"
        self.password = "adm02"
        self.pin_code = "333"
        self.user_id = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.password_field = "333"
        self.perm_role = "Permissions for Head of Sale-Dealers role"
        self.desks = ("DESK A", "Quod Desk")

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        time.sleep(2)
        side_menu.open_users_page()
        time.sleep(2)
        users_page = UsersPage(self.web_driver_container)
        users_page.click_on_more_actions()
        time.sleep(1)
        users_page.click_on_clone_at_more_actions()
        time.sleep(1)

    def test_context(self):
        try:
            self.precondition()
            users_page = UsersPage(self.web_driver_container)
            users_login_sub_wizard = UsersLoginSubWizard(self.web_driver_container)
            users_login_sub_wizard.set_user_id(self.user_id)
            users_login_sub_wizard.set_pin_code(self.pin_code)
            users_login_sub_wizard.set_password(self.password_field)
            users_role_sub_wizard = UsersRoleSubWizard(self.web_driver_container)
            time.sleep(2)
            users_role_sub_wizard.set_perm_role(self.perm_role)
            time.sleep(2)
            assignments_sub_wizard = UsersAssignmentsSubWizard(self.web_driver_container)
            assignments_sub_wizard.click_on_desks()
            time.sleep(2)
            assignments_sub_wizard.set_desks(self.desks)
            users_wizard = UsersWizard(self.web_driver_container)
            time.sleep(2)
            users_wizard.click_on_save_changes()
            time.sleep(2)
            users_page.set_user_id(self.user_id)
            time.sleep(2)
            self.verify("is values correctly saved", self.user_id, users_page.get_user_id())
        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            print(traceback.format_exc() + " Search in ->  " + self.__class__.__name__)
