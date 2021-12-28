import random
import string
import sys
import time
import traceback

from custom import basic_custom_actions
from test_cases.web_admin.web_admin_core.pages.login.login_page import LoginPage
from test_cases.web_admin.web_admin_core.pages.reference_data.venues.nested_wizards.venues_tick_size_profile_sub_wizard import \
    VenuesTickSizeProfileSubWizard
from test_cases.web_admin.web_admin_core.pages.reference_data.venues.venues_page import VenuesPage
from test_cases.web_admin.web_admin_core.pages.reference_data.venues.venues_profiles_sub_wizard import \
    VenuesProfilesSubWizard
from test_cases.web_admin.web_admin_core.pages.reference_data.venues.venues_wizard import VenuesWizard
from test_cases.web_admin.web_admin_core.pages.root.side_menu import SideMenu
from test_cases.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_1729(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id)
        self.login = "adm02"
        self.password = "adm02"
        self.external_id = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.tick_size_xaxis_type = "Price"
        self.tick = "12"

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        wizard = VenuesWizard(self.web_driver_container)
        time.sleep(2)
        side_menu.open_venues_page()
        time.sleep(2)
        page = VenuesPage(self.web_driver_container)
        page.click_on_new()
        time.sleep(2)
        profiles_sub_wizard = VenuesProfilesSubWizard(self.web_driver_container)
        profiles_sub_wizard.click_on_tick_size_profile_manage_button()
        time.sleep(2)
        tick_size_profile = VenuesTickSizeProfileSubWizard(self.web_driver_container)
        tick_size_profile.click_on_plus_button()
        time.sleep(1)
        tick_size_profile.set_external_id(self.external_id)
        time.sleep(1)
        tick_size_profile.set_tick_size_xaxis_type(self.tick_size_xaxis_type)
        time.sleep(1)
        tick_size_points = VenuesTickSizeProfileSubWizard(self.web_driver_container)
        tick_size_points.click_on_plus_button_at_tick_size_points()
        time.sleep(1)
        tick_size_points.set_tick(self.tick)
        time.sleep(1)
        tick_size_points.click_on_checkmark_at_tick_size_points()
        time.sleep(1)
        tick_size_profile.click_on_checkmark()
        time.sleep(1)
        wizard.click_on_go_back_button()
        time.sleep(2)

    def test_context(self):

        try:
            self.precondition()
            profiles_sub_wizard = VenuesProfilesSubWizard(self.web_driver_container)
            try:
                profiles_sub_wizard.set_tick_size_profile(self.external_id)
                self.verify("Tick size profile selected correctly", True, True)
            except Exception as e:
                self.verify("Tick size profile selected incorrectly, ERROR !!!", True, e.__class__.__name__)

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
