import random
import string
import sys
import time
import traceback

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.markets.venues.nested_wizards.venues_tick_size_profile_sub_wizard import \
    VenuesTickSizeProfileSubWizard
from test_framework.web_admin_core.pages.markets.venues.venues_page import VenuesPage
from test_framework.web_admin_core.pages.markets.venues.venues_profiles_sub_wizard import \
    VenuesProfilesSubWizard
from test_framework.web_admin_core.pages.markets.venues.venues_wizard import VenuesWizard
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T3979(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.external_id = [''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6)) for _ in range(2)]
        self.tick_size_xaxis_type = 'Price'
        self.tick_size_refprice_type = 'ClosingPrice'
        self.tick = ['1', '3']
        self.upper_limit = '20'

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        wizard = VenuesWizard(self.web_driver_container)
        side_menu.open_venues_page()
        page = VenuesPage(self.web_driver_container)
        page.click_on_new()
        profiles_sub_wizard = VenuesProfilesSubWizard(self.web_driver_container)
        profiles_sub_wizard.click_on_tick_size_profile_manage_button()
        tick_size_profile = VenuesTickSizeProfileSubWizard(self.web_driver_container)
        tick_size_profile.click_on_plus_button()
        tick_size_profile.set_external_id(self.external_id[0])
        tick_size_points = VenuesTickSizeProfileSubWizard(self.web_driver_container)
        tick_size_points.click_on_plus_button_at_tick_size_points()
        tick_size_points.set_tick(self.tick[0])
        tick_size_points.click_on_checkmark_at_tick_size_points()
        tick_size_profile.click_on_checkmark()
        side_menu.click_on_venues_tab()
        wizard.click_on_no_button()

    def test_context(self):
        try:
            self.precondition()

            page = VenuesPage(self.web_driver_container)
            page.click_on_new()
            profiles_sub_wizard = VenuesProfilesSubWizard(self.web_driver_container)
            profiles_sub_wizard.click_on_tick_size_profile_manage_button()

            tick_size_profile = VenuesTickSizeProfileSubWizard(self.web_driver_container)
            if tick_size_profile.is_tick_size_profile_lookup_displayed():
                tick_size_profile.load_tick_size_profile_by_lookup(self.external_id[0])
                time.sleep(0.5)
            else:
                tick_size_profile.set_external_id_filter(self.external_id[0])
                time.sleep(0.5)
            tick_size_profile.click_on_edit()
            tick_size_profile.set_external_id(self.external_id[1])
            tick_size_profile.set_tick_size_xaxis_type(self.tick_size_xaxis_type)
            tick_size_profile.set_tick_size_refprice_type(self.tick_size_refprice_type)
            tick_size_profile.click_on_edit_at_tick_size_points()
            tick_size_profile.set_tick(self.tick[1])
            tick_size_profile.set_upper_limit(self.upper_limit)
            tick_size_profile.click_on_checkmark_at_tick_size_points()
            tick_size_profile.click_on_checkmark()
            wizard = VenuesWizard(self.web_driver_container)
            wizard.click_on_go_back_button()

            profiles_sub_wizard.set_tick_size_profile(self.external_id[1])
            profiles_sub_wizard.click_on_tick_size_profile_manage_button()
            if tick_size_profile.is_tick_size_profile_lookup_displayed():
                tick_size_profile.load_tick_size_profile_by_lookup(self.external_id[1])
                time.sleep(0.5)
            else:
                tick_size_profile.set_external_id_filter(self.external_id[1])
                time.sleep(0.5)
            tick_size_profile.click_on_edit()
            tick_size_profile.click_on_edit_at_tick_size_points()

            expected_result = [self.external_id[1], self.tick_size_xaxis_type, self.tick_size_refprice_type,
                               self.tick[1], self.upper_limit]
            actual_result = [tick_size_profile.get_external_id(), tick_size_profile.get_tick_size_xaxis_type(),
                             tick_size_profile.get_tick_size_refprice_type(), tick_size_profile.get_tick(),
                             tick_size_profile.get_upper_limit()]

            self.verify("Tick Size Profile has been change", expected_result, actual_result)

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
