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


class QAP_T3590(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)

        self.login = 'adm_inst'
        self.password = 'adm_inst'

        self.institution_name = 'QUOD FINANCIAL'
        self.new_ctm_bic = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.zone_name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.location_name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.desk_name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.desk_mode = 'Hierarchical'

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)

    def test_context(self):
        try:
            self.precondition()

            side_menu = SideMenu(self.web_driver_container)
            side_menu.open_institutions_page()
            institution_page = InstitutionsPage(self.web_driver_container)
            self.verify("Displayed only one Institution", 1, institution_page.count_displayed_institutions())
        ###
            institution_page.click_on_more_actions()
            institution_page.click_on_edit()
            institution_values_tab = InstitutionsValuesSubWizard(self.web_driver_container)
            institution_values_tab.set_ctm_bic(self.new_ctm_bic)
            institution_wizard = InstitutionsWizard(self.web_driver_container)
            institution_wizard.click_on_save_changes()
            self.verify("Institutions saved with new CTM BIC", True,
                        institution_page.is_searched_institution_found(self.new_ctm_bic))
        ###
            side_menu.open_zones_page()
            zone_page = ZonesPage(self.web_driver_container)
            all_displayed_institutions_of_zones = zone_page.get_list_of_all_institutions()
            actual_result = ''
            for i in all_displayed_institutions_of_zones:
                if i != self.institution_name:
                    actual_result = False
                    break
                else:
                    actual_result = True
            self.verify(f"Only Zones with {self.institution_name} institution are displayed", True, actual_result)
            zone_page.click_on_new()
            zone_values_tab = ZonesValuesSubWizard(self.web_driver_container)
            zone_values_tab.set_name(self.zone_name)
            zone_assignment_tab = ZonesAssignmentsSubWizard(self.web_driver_container)
            displayed_institutions_in_wizard = zone_assignment_tab.get_all_institutions_from_drop_menu()
            actual_result = ''
            for i in displayed_institutions_in_wizard:
                if i != self.institution_name:
                    actual_result = False
                    break
                else:
                    actual_result = True
            self.verify(f"Only {self.institution_name} institution are displayed at crete wizard", True, actual_result)
            zone_assignment_tab.set_institution(self.institution_name)
            zone_wizard = ZonesWizard(self.web_driver_container)
            zone_wizard.click_on_save_changes()
            zone_page.set_name(self.zone_name)
            time.sleep(1)
            self.verify("New Zone is created and displayed", True, zone_page.is_searched_zone_found(self.zone_name))
            zone_page.click_on_more_actions()
            zone_page.click_on_edit()
            actual_result = ''
            for i in displayed_institutions_in_wizard:
                if i != self.institution_name:
                    actual_result = False
                    break
                else:
                    actual_result = True
            self.verify(f"Only {self.institution_name} institution are displayed at edit wizard", True, actual_result)
            zone_wizard.click_on_save_changes()
            displayed_zones_at_zones_page = zone_page.get_list_of_all_zones()
        ###
            side_menu.open_locations_page()
            location_page = LocationsPage(self.web_driver_container)
            displayed_zones_at_location_page = location_page.get_list_of_all_zones()
            actual_result = ''
            for i in displayed_zones_at_location_page:
                if i in displayed_zones_at_zones_page:
                    actual_result = True
                else:
                    actual_result = False
                    break
            self.verify(f"Locations page displays only Location with Zones from {self.institution_name} institution",
                        True, actual_result)
            location_page.click_on_new()
            location_values_tab = LocationsValuesSubWizard(self.web_driver_container)
            location_values_tab.set_name(self.location_name)
            location_assignment_tab = LocationsAssignmentsSubWizard(self.web_driver_container)
            displayed_zones_in_create_wizard = location_assignment_tab.get_all_zones_from_drop_menu()
            self.verify("Zones field dropdown displays only Zones the current User has access to",
                        displayed_zones_at_zones_page, displayed_zones_in_create_wizard)
            location_assignment_tab.set_zone(self.zone_name)
            location_wizard = LocationsWizard(self.web_driver_container)
            location_wizard.click_on_save_changes()
            location_page.set_name(self.location_name)
            time.sleep(1)
            self.verify("New Location create and displayed at main page", True,
                        location_page.is_searched_location_found(self.location_name))
            location_page.click_on_more_actions()
            location_page.click_on_edit()
            displayed_zones_in_edit_wizard = location_assignment_tab.get_all_zones_from_drop_menu()
            self.verify("Zones field dropdown displays only Zones the current User has access to",
                        displayed_zones_at_zones_page, displayed_zones_in_edit_wizard)
            location_assignment_tab.set_zone(self.zone_name)
            location_wizard.click_on_save_changes()
            displayed_locations_at_location_page = location_page.get_list_of_all_locations_name()
        ###
            side_menu.open_desks_page()
            desk_page = DesksPage(self.web_driver_container)
            displayed_locations_at_desk_page = desk_page.get_list_of_all_locations()
            actual_result = ''
            for i in displayed_locations_at_desk_page:
                if i in displayed_locations_at_location_page:
                    actual_result = True
                else:
                    actual_result = False
                    break
            self.verify(f"Desks page displays only Desk with Locations from {self.institution_name} institution",
                        True, actual_result)
            desk_page.click_on_new()
            desk_values_tab = DesksValuesSubWizard(self.web_driver_container)
            desk_values_tab.set_name(self.desk_name)
            desk_values_tab.set_desk_mode(self.desk_mode)
            desk_assignments_tab = DesksAssignmentsSubWizard(self.web_driver_container)
            displayed_locations_in_create_wizard = desk_assignments_tab.get_all_locations_from_drop_menu()
            self.verify("Locations field dropdown displays only Locations the current User has access to",
                        displayed_locations_at_location_page, displayed_locations_in_create_wizard)
            desk_assignments_tab.set_location_at_description_tab(self.location_name)
            desk_wizard = DesksWizard(self.web_driver_container)
            desk_wizard.click_on_save_changes()
            desk_page.set_name_filter(self.desk_name)
            time.sleep(1)
            self.verify("New Desk create and displayed at main page", True,
                        desk_page.is_searched_desk_found(self.desk_name))
            desk_page.click_on_more_actions()
            desk_page.click_on_edit()
            displayed_locations_in_edit_wizard = desk_assignments_tab.get_all_locations_from_drop_menu()
            self.verify("Locations field dropdown displays only Locations the current User has access to",
                        displayed_locations_at_location_page, displayed_locations_in_edit_wizard)
            desk_assignments_tab.set_location_at_description_tab(self.location_name)
            desk_wizard.click_on_save_changes()

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
