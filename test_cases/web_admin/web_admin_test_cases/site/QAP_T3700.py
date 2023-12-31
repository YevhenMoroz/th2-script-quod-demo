import time

from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.pages.site.locations.locations_assignments_sub_wizard import \
    LocationsAssignmentsSubWizard
from test_framework.web_admin_core.pages.site.locations.locations_page import LocationsPage
from test_framework.web_admin_core.pages.site.locations.locations_wizard import LocationsWizard
from test_framework.web_admin_core.pages.site.zones.zones_values_sub_wizard import ZonesValuesSubWizard
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T3700(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)

        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.zone = self.data_set.get_zone("zone_3")

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        side_menu.open_locations_page()
        main_page = LocationsPage(self.web_driver_container)
        main_page.set_enabled("true")
        time.sleep(1)

    def test_context(self):
        main_page = LocationsPage(self.web_driver_container)
        wizard = LocationsWizard(self.web_driver_container)
        assignments_sub_wizard = LocationsAssignmentsSubWizard(self.web_driver_container)
        zone_values_sub_wizard = ZonesValuesSubWizard(self.web_driver_container)

        self.precondition()

        main_page.click_on_more_actions()
        main_page.click_on_edit()
        assignments_sub_wizard.clear_zone_field()
        time.sleep(1)
        wizard.click_on_save_changes()

        self.verify("Incorrect or missing values message displayed", True,
                    wizard.is_incorrect_or_missing_value_message_displayed())

        assignments_sub_wizard.set_zone(self.zone)
        assignments_sub_wizard.click_on_zone(self.zone)
        time.sleep(2)
        self.verify("Zone page opens", True, zone_values_sub_wizard.get_name() == self.zone)
