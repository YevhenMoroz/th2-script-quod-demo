import time

from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.pages.site.zones.zones_assignments_sub_wizard import ZonesAssignmentsSubWizard
from test_framework.web_admin_core.pages.site.zones.zones_page import ZonesPage
from test_framework.web_admin_core.pages.site.zones.zones_wizard import ZonesWizard
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T3695(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.zone_name = self.data_set.get_zone("zone_2")
        self.institution = self.data_set.get_institution("institution_1")

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        wizard = ZonesWizard(self.web_driver_container)
        side_menu.open_zones_page()
        zone_page = ZonesPage(self.web_driver_container)
        zone_page.set_name(self.zone_name)
        time.sleep(1)
        zone_page.click_on_more_actions()
        zone_page.click_on_edit()

        assignments_tab = ZonesAssignmentsSubWizard(self.web_driver_container)
        assignments_tab.set_institution(self.institution)
        wizard.click_on_save_changes()

    def test_context(self):
        zone_page = ZonesPage(self.web_driver_container)
        assignments_tab = ZonesAssignmentsSubWizard(self.web_driver_container)

        self.precondition()
        zone_page.set_name(self.zone_name)
        time.sleep(1)
        zone_page.click_on_more_actions()
        zone_page.click_on_edit()
        locations = assignments_tab.get_all_locations()
        users = assignments_tab.get_all_users()

        expected_result = [True for _ in range(3)]
        actual_result = [assignments_tab.get_institution() == self.institution,
                         True if len(locations) >= 1 else False,
                         True if len(users) >= 1 else False]

        self.verify("Zone contains assigned Institution, Locations, Users", expected_result, actual_result)
