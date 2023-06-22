import time

from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.pages.users.users.users_page import UsersPage
from test_framework.web_admin_core.pages.users.users.users_assignments_sub_wizard import UsersAssignmentsSubWizard
from test_framework.web_admin_core.pages.site.zones.zones_wizard import ZonesWizard
from test_framework.web_admin_core.pages.users.users.users_wizard import UsersWizard
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T3693(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.user = self.data_set.get_user("user_4")

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        time.sleep(2)
        side_menu = SideMenu(self.web_driver_container)
        side_menu.open_users_page()
        time.sleep(2)

    def test_context(self):
        self.precondition()

        main_page = UsersPage(self.web_driver_container)
        main_page.set_user_id(self.user)
        time.sleep(1)
        main_page.click_on_more_actions()
        time.sleep(1)
        main_page.click_on_edit_at_more_actions()
        time.sleep(2)
        assignments_tab = UsersAssignmentsSubWizard(self.web_driver_container)
        assignments_tab.click_on_zone_link()
        wizard = UsersWizard(self.web_driver_container)
        if wizard.is_confirmation_pop_displayed():
            wizard.accept_or_cancel_confirmation(True)
        time.sleep(2)
        zone_wizard = ZonesWizard(self.web_driver_container)
        self.verify("Is Zones wizard open?", True, zone_wizard.is_wizard_open())