import sys
import time
import traceback

from custom import basic_custom_actions
from test_cases.web_admin.web_admin_core.pages.login.login_page import LoginPage
from test_cases.web_admin.web_admin_core.pages.root.side_menu import SideMenu
from test_cases.web_admin.web_admin_core.pages.site.locations.locations_assignments_sub_wizard import \
    LocationsAssignmentsSubWizard
from test_cases.web_admin.web_admin_core.pages.site.locations.locations_page import LocationsPage
from test_cases.web_admin.web_admin_core.pages.site.locations.locations_values_sub_wizard import LocationsValuesSubWizard
from test_cases.web_admin.web_admin_core.pages.site.locations.locations_wizard import LocationsWizard
from test_cases.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_5579(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id)
        self.login = "adm03"
        self.password = "adm03"
        self.name = "EAST-LOCATION-A"

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        time.sleep(2)
        side_menu.open_locations_page()
        time.sleep(2)
        location_page = LocationsPage(self.web_driver_container)
        location_page.set_name(self.name)
        time.sleep(2)
        location_page.click_on_enable_disable_button()
        time.sleep(1)


    def test_context(self):
        try:
            self.precondition()
            location_page = LocationsPage(self.web_driver_container)
            try:
                location_page.click_on_enable_disable_button()
                self.verify("Location enabled", True, True)

            except Exception as e:
                self.verify("Location not enabled", True, e.__class__.__name__)

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
