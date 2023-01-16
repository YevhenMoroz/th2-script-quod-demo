import sys
import time
import traceback

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.pages.site.institution.institution_assignments_sub_wizard import \
    InstitutionAssignmentsSubWizard
from test_framework.web_admin_core.pages.site.institution.institutions_page import InstitutionsPage
from test_framework.web_admin_core.pages.site.locations.locations_assignments_sub_wizard import \
    LocationsAssignmentsSubWizard
from test_framework.web_admin_core.pages.site.zones.zones_assignments_sub_wizard import ZonesAssignmentsSubWizard
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T3599(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.institution_name = self.data_set.get_institution("institution_1")
        self.zone = self.data_set.get_zone("zone_1")
        self.location = self.data_set.get_location("location_2")
        self.desk = self.data_set.get_desk("desk_2")

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        side_menu.open_institutions_page()

    def test_context(self):
        try:
            self.precondition()
            try:
                institution_page = InstitutionsPage(self.web_driver_container)
                institution_page.set_institution_name(self.institution_name)
                time.sleep(1)
                institution_page.click_on_more_actions()
                institution_page.click_on_edit()
                location_assignments_sub_wizard = InstitutionAssignmentsSubWizard(self.web_driver_container)
                location_assignments_sub_wizard.click_on_zones(self.zone)
                zone_assignments_sub_wizard = ZonesAssignmentsSubWizard(self.web_driver_container)
                zone_assignments_sub_wizard.click_on_locations(self.location)
                time.sleep(2)
                locations_assignments_sub_wizard = LocationsAssignmentsSubWizard(self.web_driver_container)
                locations_assignments_sub_wizard.click_on_desks(self.desk)
                self.verify("All links works correctly", True, True)
            except Exception as e:
                self.verify("Some link not active", True, e.__class__.__name__)

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
