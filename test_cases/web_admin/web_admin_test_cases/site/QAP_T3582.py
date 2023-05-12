import random
import string
import sys
import time
import traceback

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.site.locations.locations_page import LocationsPage
from test_framework.web_admin_core.pages.site.locations.locations_wizard import LocationsWizard
from test_framework.web_admin_core.pages.site.locations.locations_values_sub_wizard import LocationsValuesSubWizard
from test_framework.web_admin_core.pages.site.locations.locations_assignments_sub_wizard import LocationsAssignmentsSubWizard

from test_framework.web_admin_core.pages.site.desks.desks_page import DesksPage
from test_framework.web_admin_core.pages.site.desks.desks_values_sub_wizard import DesksValuesSubWizard
from test_framework.web_admin_core.pages.site.desks.desks_assignments_sub_wizard import DesksAssignmentsSubWizard
from test_framework.web_admin_core.pages.site.desks.desks_wizard import DesksWizard

from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T3582(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)

        self.login = self.data_set.get_user("user_4")
        self.password = self.data_set.get_password("password_4")
        self.zone = self.data_set.get_zone("zone_2")
        self.location_name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.desk_name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.desk_mode = 'Hierarchical'

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        time.sleep(2)

    def test_context(self):
        try:
            self.precondition()

            side_menu = SideMenu(self.web_driver_container)
            side_menu.open_locations_page()
            time.sleep(2)
            self.verify("Only Locations and Desks tab displayed",
                        [False, False, True, True],
                        [side_menu.is_institutions_page_tab_displayed(),
                         side_menu.is_zones_page_tab_displayed(),
                         side_menu.is_locations_page_tab_displayed(),
                         side_menu.is_desks_page_tab_displayed()])

            location_page = LocationsPage(self.web_driver_container)
            main_page_displayed_locations = location_page.get_list_of_all_zones()
            actual_result = bool
            for i in main_page_displayed_locations:
                if i != self.zone:
                    actual_result = False
                    break
                else:
                    actual_result = True
            self.verify(f"Only {self.zone} entity displayed", True, actual_result)

            location_page.click_on_new()
            time.sleep(2)
            location_value_tab = LocationsValuesSubWizard(self.web_driver_container)
            location_value_tab.set_name(self.location_name)
            location_assignments_tab = LocationsAssignmentsSubWizard(self.web_driver_container)
            wizard_displayed_zones = location_assignments_tab.get_all_zones_from_drop_menu()
            for i in wizard_displayed_zones:
                if i != self.zone:
                    actual_result = False
                    break
                else:
                    actual_result = True
            self.verify(f"Zone field contains only {self.zone} entity", True, actual_result)
            location_assignments_tab.set_zone(self.zone)
            location_wizard = LocationsWizard(self.web_driver_container)
            location_wizard.click_on_save_changes()
            time.sleep(2)
            location_page.set_name(self.location_name)
            time.sleep(1)
            self.verify("New Locations has been create", True,
                        location_page.is_searched_location_found(self.location_name))
            location_page.set_name("")
            time.sleep(1)
            main_page_displayed_locations = location_page.get_list_of_all_locations_name()

            side_menu.open_desks_page()
            time.sleep(2)
            actual_result = bool
            desks_page = DesksPage(self.web_driver_container)
            displayed_desks = desks_page.get_list_of_all_locations()
            for i in displayed_desks:
                if i not in main_page_displayed_locations:
                    actual_result = False
                    break
                else:
                    actual_result = True

            self.verify(f"Desks page displays only Desks, assigned to Locations assigned to {self.zone} zone",
                        True, actual_result)
            desks_page.click_on_new()
            time.sleep(2)
            desk_value_tab = DesksValuesSubWizard(self.web_driver_container)
            desk_value_tab.set_name(self.desk_name)
            desk_value_tab.set_desk_mode(self.desk_mode)
            desk_assignment_tab = DesksAssignmentsSubWizard(self.web_driver_container)
            desk_assignment_tab.set_location(self.location_name)
            desk_wizard = DesksWizard(self.web_driver_container)
            desk_wizard.click_on_save_changes()
            time.sleep(2)
            desks_page.set_name_filter(self.desk_name)
            time.sleep(2)
            self.verify("New Desk has been create", True, desks_page.is_searched_desk_found(self.desk_name))

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
