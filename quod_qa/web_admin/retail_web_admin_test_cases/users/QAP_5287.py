import time
import traceback

from selenium.common.exceptions import TimeoutException

from custom import basic_custom_actions
from quod_qa.web_admin.web_admin_core.pages.login.login_page import LoginPage
from quod_qa.web_admin.web_admin_core.pages.root.side_menu import SideMenu
from quod_qa.web_admin.web_admin_core.pages.users.users.users_page import UsersPage
from quod_qa.web_admin.web_admin_core.pages.users.users.users_role_sub_wizard import UsersRoleSubWizard
from quod_qa.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer
from quod_qa.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_5287(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id)
        self.login = "adm02"
        self.password = "adm02"

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

    def test_context(self):
        try:
            self.precondition()
            user_role_sub_wizard = UsersRoleSubWizard(self.web_driver_container)
            try:
                self.verify("Is perm role field displayed", True, user_role_sub_wizard.is_perm_role_field_visible())
                self.verify("Is perm op field displayed", True, user_role_sub_wizard.is_perm_op_field_visible())
                self.verify("Is group field displayed", True, user_role_sub_wizard.is_group_field_visible())
            except Exception:
                self.verify("Some fields in role tab not visible", True, False)

            try:
                user_role_sub_wizard.is_role_id_field_visible()
            except TimeoutException:
                self.verify("Is role id field NOT displayed", True, True)

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            print(traceback.format_exc() + " Search in ->  " + self.__class__.__name__)
