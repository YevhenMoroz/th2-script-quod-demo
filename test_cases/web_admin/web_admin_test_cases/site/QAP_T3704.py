import sys
import time
import traceback

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.pages.site.desks.desks_assignments_sub_wizard import DesksAssignmentsSubWizard
from test_framework.web_admin_core.pages.site.desks.desks_page import DesksPage
from test_framework.web_admin_core.pages.site.desks.desks_values_sub_wizard import DesksValuesSubWizard
from test_framework.web_admin_core.pages.site.locations.locations_values_sub_wizard import LocationsValuesSubWizard
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T3704(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = "adm03"
        self.password = "adm03"
        self.desk_name = "Quod Desk"
        self.location = "EAST-LOCATION-B"
        self.user = "adm_desk"

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        main_page = DesksPage(self.web_driver_container)
        side_menu.open_desks_page()
        main_page.set_name_filter(self.desk_name)
        main_page.set_location_filter(self.location)
        time.sleep(1)
        main_page.click_on_more_actions()
        main_page.click_on_edit()

    def test_context(self):
        values_sub_wizard = DesksValuesSubWizard(self.web_driver_container)
        assignments_sub_wizard = DesksAssignmentsSubWizard(self.web_driver_container)
        location_values_sub_wizard = LocationsValuesSubWizard(self.web_driver_container)

        try:
            self.precondition()

            expected_values = [self.desk_name, "Collaborative"]
            actual_values = [values_sub_wizard.get_name(), values_sub_wizard.get_desk_mode()]
            self.verify("Is required fields have values", expected_values, actual_values)

            self.verify("Is users field has link", True, assignments_sub_wizard.is_user_link_exist(self.user))
            assignments_sub_wizard.click_on_location(self.location)
            self.verify("Is location field has hyperlinked value", self.location, location_values_sub_wizard.get_name())

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
