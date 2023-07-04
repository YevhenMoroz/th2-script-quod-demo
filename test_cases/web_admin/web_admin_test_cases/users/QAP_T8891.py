import time

from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.pages.users.users.users_page import UsersPage
from test_framework.web_admin_core.pages.users.users.users_assignments_sub_wizard import UsersAssignmentsSubWizard
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T8891(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.desk = self.data_set.get_desk("desk_1")
        self.location = self.data_set.get_location("location_1")
        self.zone = self.data_set.get_zone("zone_1")
        self.institution = self.data_set.get_institution("institution_1")
        self.clear_option = 'Not found'

    def test_context(self):
        login_page = LoginPage(self.web_driver_container)
        side_menu = SideMenu(self.web_driver_container)
        users_page = UsersPage(self.web_driver_container)
        assignments_tab = UsersAssignmentsSubWizard(self.web_driver_container)

        login_page.login_to_web_admin(self.login, self.password)
        side_menu.open_users_page()
        users_page.click_on_new_button()
        assignments_tab.set_desks(self.desk)
        time.sleep(1)
        self.verify('The fields "Location", "Zone", "Institution" became read-only',
                    [False for _ in range(3)],
                    [assignments_tab.is_location_field_enabled(), assignments_tab.is_zone_field_enabled(),
                     assignments_tab.is_institution_field_enabled()])
        assignments_tab.set_desks(self.desk)
        assignments_tab.set_location(self.location)
        time.sleep(1)
        self.verify('The fields "Desks", "Zone", "Institution" became read-only',
                    [False for _ in range(3)],
                    [assignments_tab.is_desks_field_enabled(),
                     assignments_tab.is_zone_field_enabled(),
                     assignments_tab.is_institution_field_enabled()])
        assignments_tab.set_location(self.clear_option)
        time.sleep(1)
        assignments_tab.set_zone(self.zone)
        time.sleep(1)
        self.verify('The fields "Desks", "Location", "Institution" became read-only',
                    [False for _ in range(3)],
                    [assignments_tab.is_location_field_enabled(), assignments_tab.is_location_field_enabled(),
                     assignments_tab.is_institution_field_enabled()])
        assignments_tab.set_zone(self.clear_option)
        time.sleep(1)
        assignments_tab.set_institution(self.institution)
        time.sleep(1)
        self.verify('The fields "Desks", "Location", "Zone" became read-only',
                    [False for _ in range(3)],
                    [assignments_tab.is_location_field_enabled(), assignments_tab.is_location_field_enabled(),
                     assignments_tab.is_zone_field_enabled()])
