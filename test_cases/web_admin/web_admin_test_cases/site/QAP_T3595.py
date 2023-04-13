import random
import string
import sys
import time
import traceback

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.site.institution.institutions_page import InstitutionsPage
from test_framework.web_admin_core.pages.site.institution.institutions_wizard import InstitutionsWizard
from test_framework.web_admin_core.pages.site.institution.institution_values_sub_wizard \
    import InstitutionsValuesSubWizard

from test_framework.web_admin_core.pages.site.zones.zones_page import ZonesPage
from test_framework.web_admin_core.pages.site.zones.zones_wizard import ZonesWizard
from test_framework.web_admin_core.pages.site.zones.zones_values_sub_wizard import ZonesValuesSubWizard
from test_framework.web_admin_core.pages.site.zones.zones_assignments_sub_wizard import ZonesAssignmentsSubWizard

from test_framework.web_admin_core.pages.site.locations.locations_page import LocationsPage
from test_framework.web_admin_core.pages.site.locations.locations_wizard import LocationsWizard
from test_framework.web_admin_core.pages.site.locations.locations_values_sub_wizard import LocationsValuesSubWizard
from test_framework.web_admin_core.pages.site.locations.locations_assignments_sub_wizard \
    import LocationsAssignmentsSubWizard

from test_framework.web_admin_core.pages.site.desks.desks_page import DesksPage
from test_framework.web_admin_core.pages.site.desks.desks_wizard import DesksWizard
from test_framework.web_admin_core.pages.site.desks.desks_values_sub_wizard import DesksValuesSubWizard
from test_framework.web_admin_core.pages.site.desks.desks_assignments_sub_wizard import DesksAssignmentsSubWizard

from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T3595(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)

        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")

        self.institution_name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.ctm_bic = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.zone_name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.base_institution = self.data_set.get_institution("institution_1")
        self.location_name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.base_zone = data_set.get_zone("zone_2")
        self.desk_name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.desk_mode = 'Hierarchical'
        self.base_location = data_set.get_location("location_3")

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        time.sleep(2)

    def test_context(self):
        try:
            self.precondition()

            side_menu = SideMenu(self.web_driver_container)
            side_menu.open_institutions_page()
            time.sleep(2)
            institution_page = InstitutionsPage(self.web_driver_container)
            institution_page.click_on_new()
            time.sleep(2)
            institution_values_tab = InstitutionsValuesSubWizard(self.web_driver_container)
            institution_values_tab.set_institution_name(self.institution_name)
            institution_wizard = InstitutionsWizard(self.web_driver_container)
            institution_wizard.click_on_save_changes()
            time.sleep(2)
            institution_page.set_institution_name(self.institution_name)
            time.sleep(1)
            self.verify("New Institution is created and displayed at main page", True,
                        institution_page.is_searched_institution_found(self.institution_name))
            institution_page.click_on_more_actions()
            time.sleep(1)
            institution_page.click_on_edit()
            time.sleep(2)
            institution_values_tab.set_ctm_bic(self.ctm_bic)
            institution_wizard.click_on_save_changes()
            time.sleep(2)
            institution_page.set_institution_name(self.institution_name)
            time.sleep(1)
            self.verify("Saved CTM BIC is displayed", True,
                        institution_page.is_searched_institution_found(self.ctm_bic))

            side_menu.open_zones_page()
            time.sleep(2)
            zone_page = ZonesPage(self.web_driver_container)
            zone_page.click_on_new()
            time.sleep(2)
            zone_value_tab = ZonesValuesSubWizard(self.web_driver_container)
            zone_value_tab.set_name(self.zone_name)
            zone_assignment_tab = ZonesAssignmentsSubWizard(self.web_driver_container)
            zone_assignment_tab.set_institution(self.base_institution)
            zone_wizard = ZonesWizard(self.web_driver_container)
            zone_wizard.click_on_save_changes()
            time.sleep(2)
            zone_page.set_name(self.zone_name)
            time.sleep(1)
            self.verify("New Zone is created and displayed at main page", True,
                        zone_page.is_searched_zone_found(self.zone_name))
            zone_page.click_on_more_actions()
            time.sleep(1)
            zone_page.click_on_edit()
            time.sleep(2)
            zone_assignment_tab.set_institution(self.institution_name)
            zone_wizard.click_on_save_changes()
            time.sleep(2)
            zone_page.set_name(self.zone_name)
            time.sleep(1)
            self.verify("New institution for zone is displayed at main page", True,
                        zone_page.is_searched_zone_found(self.institution_name))

            side_menu.open_locations_page()
            time.sleep(2)
            location_page = LocationsPage(self.web_driver_container)
            location_page.click_on_new()
            time.sleep(2)
            location_values_tab = LocationsValuesSubWizard(self.web_driver_container)
            location_values_tab.set_name(self.location_name)
            location_assignment_tab = LocationsAssignmentsSubWizard(self.web_driver_container)
            location_assignment_tab.set_zone(self.base_zone)
            location_wizard = LocationsWizard(self.web_driver_container)
            location_wizard.click_on_save_changes()
            time.sleep(2)
            location_page.set_name(self.location_name)
            time.sleep(1)
            self.verify("New Location is created and displayed at main page", True,
                        location_page.is_searched_location_found(self.location_name))
            location_page.click_on_more_actions()
            time.sleep(1)
            location_page.click_on_edit()
            time.sleep(2)
            location_assignment_tab.set_zone(self.zone_name)
            location_wizard.click_on_save_changes()
            time.sleep(2)
            location_page.set_name(self.location_name)
            time.sleep(1)
            self.verify("New zone for Location is displayed at main page", True,
                        location_page.is_searched_location_found(self.zone_name))

            side_menu.open_desks_page()
            time.sleep(2)
            desk_page = DesksPage(self.web_driver_container)
            desk_page.click_on_new()
            time.sleep(2)
            desk_values_tab = DesksValuesSubWizard(self.web_driver_container)
            desk_values_tab.set_name(self.desk_name)
            desk_values_tab.set_desk_mode(self.desk_mode)
            desk_assignments_tab = DesksAssignmentsSubWizard(self.web_driver_container)
            desk_assignments_tab.set_location(self.base_location)
            desk_wizard = DesksWizard(self.web_driver_container)
            desk_wizard.click_on_save_changes()
            time.sleep(2)
            desk_page.set_name_filter(self.desk_name)
            time.sleep(1)
            self.verify("New Desk is created and displayed at main page", True,
                        desk_page.is_searched_desk_found(self.desk_name))
            desk_page.click_on_more_actions()
            time.sleep(1)
            desk_page.click_on_edit()
            time.sleep(2)
            desk_assignments_tab.set_location(self.location_name)
            desk_wizard.click_on_save_changes()
            time.sleep(2)
            desk_page.set_name_filter(self.desk_name)
            time.sleep(1)
            self.verify("New location for desk displayed at main page", True,
                        desk_page.is_searched_desk_found(self.location_name))

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
