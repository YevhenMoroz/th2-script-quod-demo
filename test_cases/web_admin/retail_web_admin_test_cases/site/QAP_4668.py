import time
import traceback

from custom import basic_custom_actions
from test_cases.web_admin.web_admin_core.pages.login.login_page import LoginPage
from test_cases.web_admin.web_admin_core.pages.root.side_menu import SideMenu
from test_cases.web_admin.web_admin_core.pages.site.locations.locations_assignments_sub_wizard import \
    LocationsAssignmentsSubWizard
from test_cases.web_admin.web_admin_core.pages.site.locations.locations_page import LocationsPage
from test_cases.web_admin.web_admin_core.pages.site.locations.locations_wizard import LocationsWizard
from test_cases.web_admin.web_admin_core.pages.site.zones.zones_values_sub_wizard import ZonesValuesSubWizard
from test_cases.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_4668(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id)
        self.login = "adm02"
        self.password = "adm02"
        self.zone = "NORTH-ZONE"

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        time.sleep(2)
        side_menu.open_locations_page()
        time.sleep(2)
        main_page = LocationsPage(self.web_driver_container)
        main_page.set_enabled("true")
        time.sleep(2)
        main_page.click_on_more_actions()
        time.sleep(2)
        main_page.click_on_edit()
        time.sleep(2)
        assignments_sub_wizard = LocationsAssignmentsSubWizard(self.web_driver_container)
        assignments_sub_wizard.clear_zone_field()
        time.sleep(1)
        wizard = LocationsWizard(self.web_driver_container)
        wizard.click_on_save_changes()

    def test_context(self):
        try:
            self.precondition()
            wizard = LocationsWizard(self.web_driver_container)
            assignments_sub_wizard = LocationsAssignmentsSubWizard(self.web_driver_container)
            self.verify("Incorrect or missing values message displayed", True,
                        wizard.is_incorrect_or_missing_value_message_displayed())
            time.sleep(2)
            assignments_sub_wizard.set_zone(self.zone)
            time.sleep(2)
            assignments_sub_wizard.click_on_zone(self.zone)
            time.sleep(2)
            zone_values_sub_wizard = ZonesValuesSubWizard(self.web_driver_container)
            self.verify(
                "Is zone menu displayed after click on hyperlink", True, zone_values_sub_wizard.get_name() == self.zone)

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            print(traceback.format_exc() + " Search in ->  " + self.__class__.__name__)
