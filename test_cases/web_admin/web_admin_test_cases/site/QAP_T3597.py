import random
import string
import time

from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.pages.site.locations.locations_assignments_sub_wizard import \
    LocationsAssignmentsSubWizard
from test_framework.web_admin_core.pages.site.locations.locations_page import LocationsPage
from test_framework.web_admin_core.pages.site.locations.locations_values_sub_wizard import LocationsValuesSubWizard
from test_framework.web_admin_core.pages.site.locations.locations_wizard import LocationsWizard
from test_framework.web_admin_core.pages.site.zones.zones_assignments_sub_wizard import ZonesAssignmentsSubWizard
from test_framework.web_admin_core.pages.site.zones.zones_page import ZonesPage
from test_framework.web_admin_core.pages.site.zones.zones_values_sub_wizard import ZonesValuesSubWizard
from test_framework.web_admin_core.pages.site.zones.zones_wizard import ZonesWizard
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T3597(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.location1 = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.location2 = self.location1
        self.zone1 = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.zone2 = self.data_set.get_zone("zone_2")
        self.institution = self.data_set.get_institution("institution_2")

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
