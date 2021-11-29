import sys
import time
import traceback

from custom import basic_custom_actions
from test_cases.web_admin.web_admin_core.pages.login.login_page import LoginPage
from test_cases.web_admin.web_admin_core.pages.root.side_menu import SideMenu
from test_cases.web_admin.web_admin_core.pages.site.institution.institution_assignments_sub_wizard import \
    InstitutionAssignmentsSubWizard
from test_cases.web_admin.web_admin_core.pages.site.institution.institutions_page import InstitutionsPage
from test_cases.web_admin.web_admin_core.pages.site.locations.locations_assignments_sub_wizard import \
    LocationsAssignmentsSubWizard
from test_cases.web_admin.web_admin_core.pages.site.locations.locations_wizard import LocationsWizard
from test_cases.web_admin.web_admin_core.pages.site.zones.zones_assignments_sub_wizard import ZonesAssignmentsSubWizard
from test_cases.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_5578(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id)
        self.login = "adm03"
        self.password = "adm03"
        self.institution_name = "QUOD FINANCIAL"
        self.zone = "WEST-ZONE"
        self.location = "WEST-LOCATION-B"
        self.desk = "DESK-C"

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        time.sleep(2)
        side_menu.open_institutions_page()
        time.sleep(2)

    def test_context(self):
        try:
            self.precondition()
            try:
                institution_page = InstitutionsPage(self.web_driver_container)
                institution_page.set_institution_name(self.institution_name)
                location_wizard = LocationsWizard(self.web_driver_container)
                time.sleep(2)
                institution_page.click_on_more_actions()
                time.sleep(2)
                institution_page.click_on_edit()
                location_assignments_sub_wizard = InstitutionAssignmentsSubWizard(self.web_driver_container)
                location_assignments_sub_wizard.click_on_zones(self.zone)
                time.sleep(2)
                location_wizard.click_on_ok_button()
                time.sleep(2)
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
