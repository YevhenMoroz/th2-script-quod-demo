import random
import string
import sys
import time
import traceback

from custom import basic_custom_actions
from quod_qa.web_admin.web_admin_core.pages.login.login_page import LoginPage
from quod_qa.web_admin.web_admin_core.pages.root.side_menu import SideMenu
from quod_qa.web_admin.web_admin_core.pages.site.locations.locations_assignments_sub_wizard import \
    LocationsAssignmentsSubWizard
from quod_qa.web_admin.web_admin_core.pages.site.locations.locations_page import LocationsPage
from quod_qa.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer
from quod_qa.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_5583(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id)
        self.login = "adm02"
        self.password = "adm02"
        self.name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.location = "EAST-LOCATION-B"
        self.user_name = "adm_loca"

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        time.sleep(2)
        side_menu.open_locations_page()
        time.sleep(2)
        location_page = LocationsPage(self.web_driver_container)
        location_page.set_name(self.location)
        time.sleep(2)
        location_page.click_on_more_actions()
        time.sleep(2)
        location_page.click_on_edit()
        time.sleep(1)

    def test_context(self):
        try:
            self.precondition()
            assignments_sub_wizard = LocationsAssignmentsSubWizard(self.web_driver_container)
            try:

                assignments_sub_wizard.click_on_user(self.user_name)
                self.verify("User link works correctly", True, True)
            except Exception as e:
                self.verify("User link not working", True, e.__class__.__name__)

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)