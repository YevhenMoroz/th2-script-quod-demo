import time
import traceback

from custom import basic_custom_actions
from quod_qa.web_admin.web_admin_core.pages.login.login_page import LoginPage
from quod_qa.web_admin.web_admin_core.pages.root.side_menu import SideMenu
from quod_qa.web_admin.web_admin_core.pages.site.desks.desks_assignments_sub_wizard import DesksAssignmentsSubWizard
from quod_qa.web_admin.web_admin_core.pages.site.desks.desks_page import DesksPage
from quod_qa.web_admin.web_admin_core.pages.site.desks.desks_values_sub_wizard import DesksValuesSubWizard
from quod_qa.web_admin.web_admin_core.pages.site.locations.locations_values_sub_wizard import LocationsValuesSubWizard
from quod_qa.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer
from quod_qa.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_4662(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id)
        self.login = "adm02"
        self.password = "adm02"
        self.desk_name = "Quod Desk"
        self.location = "EAST-LOCATION-B"
        self.user = "QA1"

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        main_page = DesksPage(self.web_driver_container)
        time.sleep(2)
        side_menu.open_desks_page()
        time.sleep(2)
        main_page.set_location_filter("EAST-LOCATION-B")
        time.sleep(2)
        main_page.click_on_more_actions()
        time.sleep(2)
        main_page.click_on_edit()
        time.sleep(2)

    def test_context(self):
        try:
            self.precondition()
            values_sub_wizard = DesksValuesSubWizard(self.web_driver_container)
            expected_values = [self.desk_name, "Collaborative"]
            actual_values = [values_sub_wizard.get_name(), values_sub_wizard.get_desk_mode()]
            self.verify("Is required fields have values", expected_values, actual_values)
            assignments_sub_wizard = DesksAssignmentsSubWizard(self.web_driver_container)
            self.verify("Is users field has link", True, assignments_sub_wizard.is_user_link_exist(self.user))
            time.sleep(3)
            assignments_sub_wizard.click_on_location(self.location)
            time.sleep(3)
            location_values_sub_wizard = LocationsValuesSubWizard(self.web_driver_container)
            self.verify("Is location field has hyperlinked value", self.location, location_values_sub_wizard.get_name())


        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            print(traceback.format_exc() + " Search in ->  " + self.__class__.__name__)
