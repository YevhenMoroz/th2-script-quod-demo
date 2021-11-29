import time
import traceback

from selenium.common.exceptions import ElementNotInteractableException

from custom import basic_custom_actions
from test_cases.web_admin.web_admin_core.pages.general.common.common_page import CommonPage
from test_cases.web_admin.web_admin_core.pages.login.login_page import LoginPage
from test_cases.web_admin.web_admin_core.pages.root.side_menu import SideMenu
from test_cases.web_admin.web_admin_core.pages.users.users.users_page import UsersPage
from test_cases.web_admin.web_admin_core.pages.users.users.users_role_sub_wizard import UsersRoleSubWizard
from test_cases.web_admin.web_admin_core.pages.users.users.users_wizard import UsersWizard
from test_cases.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_5315(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id)
        self.login = "adm02"
        self.password = "adm02"
        self.venue = "KSE"
        self.user_id = "adm05"
        self.perm_role = "Permissions for Head of Location role"

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        time.sleep(2)
        side_menu.open_users_page()
        users_page = UsersPage(self.web_driver_container)
        users_wizard = UsersWizard(self.web_driver_container)
        time.sleep(2)
        users_page.set_user_id(self.user_id)
        time.sleep(2)
        users_page.click_on_more_actions()
        time.sleep(2)
        users_page.click_on_edit_at_more_actions()
        role_sub_wizard = UsersRoleSubWizard(self.web_driver_container)
        time.sleep(1)
        role_sub_wizard.set_perm_role(self.perm_role)
        time.sleep(2)
        users_wizard.click_on_save_changes()
        time.sleep(2)
        common_page = CommonPage(self.web_driver_container)
        common_page.click_on_user_icon()
        time.sleep(2)
        common_page.click_on_logout()
        time.sleep(2)
        login_page.login_to_web_admin("adm05", "adm05")

    def test_context(self):
        try:
            self.precondition()
            side_menu = SideMenu(self.web_driver_container)
            try:
                side_menu.open_institutions_page()
                self.verify("Institution page MUST NOT displayed", False, True)
            except ElementNotInteractableException:
                self.verify("Institution page in not displayed", True, True)
            try:
                side_menu.open_zones_page()
                self.verify("Zones page MUST NOT  displayed", False, True)
            except ElementNotInteractableException:
                self.verify("Zones page in not displayed", True, True)
            try:
                side_menu.open_locations_page()
                self.verify("Location page displayed", True, True)
                side_menu.open_desks_page()
                self.verify("Desks page MUST NOT displayed", False, True)
            except ElementNotInteractableException:
                self.verify("Desks page in not displayed", True, True)






        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            print(traceback.format_exc() + " Search in ->  " + self.__class__.__name__)
