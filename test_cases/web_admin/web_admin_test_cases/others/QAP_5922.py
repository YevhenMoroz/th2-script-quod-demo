import random
import string
import sys
import time
import traceback

from custom import basic_custom_actions
from test_cases.web_admin.web_admin_core.pages.login.login_page import LoginPage
from test_cases.web_admin.web_admin_core.pages.others.routes.routes_page import RoutesPage
from test_cases.web_admin.web_admin_core.pages.others.routes.routes_venues_subwizard import RoutesVenuesSubWizard
from test_cases.web_admin.web_admin_core.pages.others.routes.routes_wizard import RoutesWizard
from test_cases.web_admin.web_admin_core.pages.root.side_menu import SideMenu
from test_cases.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_5922(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id)
        self.login = "adm02"
        self.password = "adm02"
        self.name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.user_id = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.mic = "ALXP"
        self.venue = "ADX"
        self.main_security_id_source = 'Blmbrg'

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        time.sleep(2)
        side_menu.open_routes_page()
        routes_page = RoutesPage(self.web_driver_container)
        routes_page.click_on_new_button()
        time.sleep(1)

    def test_context(self):
        try:
            self.precondition()
            values_sub_wizard = RoutesWizard(self.web_driver_container)
            values_sub_wizard.set_name_at_values_tab(self.name)
            time.sleep(1)
            routes_venues_sub_wizard = RoutesVenuesSubWizard(self.web_driver_container)
            routes_venues_sub_wizard.click_on_plus_at_venues_tab()
            routes_venues_sub_wizard.set_venue_at_venues_tab(self.venue)
            routes_venues_sub_wizard.set_main_security_id_source_at_venues_tab(self.main_security_id_source)
            routes_venues_sub_wizard.set_mic_at_venues_tab_at_venues_tab(self.mic)
            routes_venues_sub_wizard.click_on_check_mark_at_venues_tab()
            self.verify("Mic at venue created correctly", True, True)
            wizard = RoutesWizard(self.web_driver_container)
            time.sleep(2)
            wizard.click_on_save_changes()
            time.sleep(1)
            page = RoutesPage(self.web_driver_container)
            page.set_name_at_filter(self.name)
            time.sleep(1)
            page.click_on_more_actions()
            time.sleep(1)
            page.click_on_edit_at_more_actions()
            time.sleep(1)
            venues_sub_wizard = RoutesVenuesSubWizard(self.web_driver_container)
            venues_sub_wizard.click_on_edit_at_venues_tab()
            time.sleep(2)
            expected_data_result = [self.mic, self.main_security_id_source]
            actual_data_result = [venues_sub_wizard.get_mic_at_venues_tab_at_venues_tab(),
                                  venues_sub_wizard.get_main_security_id_source_at_venues_tab()]

            self.verify("Is venue saved correctly", expected_data_result, actual_data_result)
        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
