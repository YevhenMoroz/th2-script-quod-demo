import random
import string
import sys
import time
import traceback

from custom import basic_custom_actions
from quod_qa.web_admin.web_admin_core.pages.login.login_page import LoginPage
from quod_qa.web_admin.web_admin_core.pages.root.side_menu import SideMenu
from quod_qa.web_admin.web_admin_core.pages.site.locations.locations_assignments_sub_wizard import \
    LocationsAssignmentsSubWizard
from quod_qa.web_admin.web_admin_core.pages.site.locations.locations_page import LocationsPage
from quod_qa.web_admin.web_admin_core.pages.site.locations.locations_values_sub_wizard import LocationsValuesSubWizard
from quod_qa.web_admin.web_admin_core.pages.site.locations.locations_wizard import LocationsWizard
from quod_qa.web_admin.web_admin_core.pages.site.zones.zones_assignments_sub_wizard import ZonesAssignmentsSubWizard
from quod_qa.web_admin.web_admin_core.pages.site.zones.zones_page import ZonesPage
from quod_qa.web_admin.web_admin_core.pages.site.zones.zones_values_sub_wizard import ZonesValuesSubWizard
from quod_qa.web_admin.web_admin_core.pages.site.zones.zones_wizard import ZonesWizard
from quod_qa.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer
from quod_qa.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_5580(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id)
        self.login = "adm02"
        self.password = "adm02"
        self.location1 = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.location2 = self.location1
        self.zone1 = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.zone2 = "EAST-ZONE"
        self.institution = "LOAD"

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        time.sleep(2)
        side_menu.open_zones_page()
        time.sleep(2)
        zone_page = ZonesPage(self.web_driver_container)
        zone_page.click_on_new()
        time.sleep(1)
        values_tab = ZonesValuesSubWizard(self.web_driver_container)
        values_tab.set_name(self.zone1)
        assignments_tab = ZonesAssignmentsSubWizard(self.web_driver_container)
        assignments_tab.set_institution(self.institution)
        wizard_zone = ZonesWizard(self.web_driver_container)
        wizard_zone.click_on_save_changes()
        time.sleep(2)
        side_menu.open_locations_page()
        time.sleep(2)
        location_page = LocationsPage(self.web_driver_container)
        location_page.click_on_new()
        time.sleep(2)
        values_sub_wizard = LocationsValuesSubWizard(self.web_driver_container)
        values_sub_wizard.set_name(self.location1)
        assignments_sub_wizard = LocationsAssignmentsSubWizard(self.web_driver_container)
        assignments_sub_wizard.set_zone(self.zone1)
        time.sleep(1)
        wizard = LocationsWizard(self.web_driver_container)
        wizard.click_on_save_changes()
        time.sleep(2)
        location_page.click_on_new()
        values_sub_wizard.set_name(self.location2)
        assignments_sub_wizard = LocationsAssignmentsSubWizard(self.web_driver_container)
        assignments_sub_wizard.set_zone(self.zone2)
        time.sleep(1)


    def test_context(self):
        try:
            self.precondition()
            location_page = LocationsPage(self.web_driver_container)
            wizard = LocationsWizard(self.web_driver_container)
            try:
                wizard.click_on_save_changes()
                time.sleep(2)
                location_page.set_name(self.location2)
                time.sleep(2)
                location_page.click_on_more_actions()
                self.verify("New same Location with another institution created correctly", True, True)
            except Exception as e:
                self.verify("Same Location not created", True, e.__class__.__name__)
        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
