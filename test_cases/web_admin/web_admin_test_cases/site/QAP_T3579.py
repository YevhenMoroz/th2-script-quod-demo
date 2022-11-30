import random
import string
import sys
import time
import traceback

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.site.desks.desks_page import DesksPage
from test_framework.web_admin_core.pages.site.desks.desks_values_sub_wizard import DesksValuesSubWizard
from test_framework.web_admin_core.pages.site.desks.desks_assignments_sub_wizard import DesksAssignmentsSubWizard
from test_framework.web_admin_core.pages.site.desks.desks_wizard import DesksWizard

from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T3579(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)

        self.login = 'adm_loca'
        self.password = 'adm_loca'
        self.location = 'EAST-LOCATION-B'
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
            side_menu.open_desks_page()
            time.sleep(2)
            self.verify("Only Desks tab displayed",
                        [side_menu.is_institutions_page_tab_displayed(),
                         side_menu.is_zones_page_tab_displayed(),
                         side_menu.is_locations_page_tab_displayed(),
                         side_menu.is_desks_page_tab_displayed()],
                        [False, False, False, True])

            actual_result = bool
            desks_page = DesksPage(self.web_driver_container)
            displayed_desks = desks_page.get_list_of_all_locations()
            for i in displayed_desks:
                if i != self.location:
                    actual_result = False
                    break
                else:
                    actual_result = True
            self.verify(f"Desks page displays only Desks, assigned to {self.location} location",
                        True, actual_result)
            desks_page.click_on_new()
            time.sleep(2)
            desk_value_tab = DesksValuesSubWizard(self.web_driver_container)
            desk_value_tab.set_name(self.desk_name)
            desk_value_tab.set_desk_mode(self.desk_mode)
            desk_assignment_tab = DesksAssignmentsSubWizard(self.web_driver_container)
            available_locations_in_wizard = desk_assignment_tab.get_all_locations_from_drop_menu()
            actual_result = bool
            for i in available_locations_in_wizard:
                if i != self.location:
                    actual_result = False
                    break
                else:
                    actual_result = True
            self.verify(f"Locations field in the create wizard contains only {self.location} entity",
                        True, actual_result)

            desk_assignment_tab.set_location(self.location)
            desk_wizard = DesksWizard(self.web_driver_container)
            desk_wizard.click_on_save_changes()
            time.sleep(2)
            desks_page.set_name_filter(self.desk_name)
            time.sleep(1)
            self.verify("New Desk has been create", True, desks_page.is_searched_desk_found(self.desk_name))
            desks_page.click_on_more_actions()
            time.sleep(1)
            desks_page.click_on_edit()
            time.sleep(2)
            available_locations_in_wizard = desk_assignment_tab.get_all_locations_from_drop_menu()
            actual_result = bool
            for i in available_locations_in_wizard:
                if i != self.location:
                    actual_result = False
                    break
                else:
                    actual_result = True
            self.verify(f"Locations field in the edit wizard contains only {self.location} entity",
                        True, actual_result)
            desk_assignment_tab.set_location(self.location)
            desk_wizard = DesksWizard(self.web_driver_container)
            desk_wizard.click_on_save_changes()
            time.sleep(2)
            desks_page.set_name_filter(self.desk_name)
            time.sleep(1)
            self.verify("Desk displayed after modify", True, desks_page.is_searched_desk_found(self.desk_name))

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
