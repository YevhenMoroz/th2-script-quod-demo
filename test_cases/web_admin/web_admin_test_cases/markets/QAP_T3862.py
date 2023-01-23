import random
import string
import sys
import time
import traceback

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.markets.venues.nested_wizards.venues_trading_phase_profile_sub_wizard import \
    VenuesTradingPhaseProfileSubWizard
from test_framework.web_admin_core.pages.markets.venues.venues_values_sub_wizard import \
    VenuesValuesSubWizard
from test_framework.web_admin_core.pages.markets.venues.venues_page import VenuesPage
from test_framework.web_admin_core.pages.markets.venues.venues_profiles_sub_wizard import \
    VenuesProfilesSubWizard
from test_framework.web_admin_core.pages.markets.venues.venues_wizard import VenuesWizard
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T3862(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.id = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.client_venue_id = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.type = "DarkPool"
        self.trading_phase_profile_desc = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.trading_phase = self.data_set.get_trading_phase("trading_phase_3")

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
        description_sub_wizard = VenuesValuesSubWizard(self.web_driver_container)
        description_sub_wizard.set_name(self.name)
        description_sub_wizard.set_id(self.id)
        description_sub_wizard.set_client_venue_id(self.client_venue_id)
        time.sleep(1)
        description_sub_wizard.set_type(self.type)
        wizard.click_on_save_changes()
        time.sleep(2)
        page.set_name_filter(self.name)
        time.sleep(2)
        page.click_on_more_actions()
        time.sleep(2)
        page.click_on_edit()
        time.sleep(2)

    def test_context(self):
        wizard = VenuesWizard(self.web_driver_container)
        page = VenuesPage(self.web_driver_container)
        profiles = VenuesProfilesSubWizard(self.web_driver_container)
        try:
            self.precondition()

            trading_phase_profile_sub_wizard = VenuesTradingPhaseProfileSubWizard(self.web_driver_container)
            profiles.click_on_trading_phase_profile_manage_button()
            time.sleep(2)
            trading_phase_profile_sub_wizard.click_on_plus_button()
            try:
                self.verify("TradingPhaseProfile Desc field is required", True,
                            trading_phase_profile_sub_wizard.is_field_trading_phase_profile_desc_required())
            except Exception as e:
                self.verify("TradingPhaseProfile Desc field is not required", True, e.__class__.__name__)

            trading_phase_profile_sub_wizard.set_trading_phase_profile_desc(self.trading_phase_profile_desc)
            trading_phase_profile_sub_wizard.click_on_plus_button_at_trading_phase_profile_sequences()
            time.sleep(1)
            try:
                self.verify("Trading Phase Sequences field is required", True,
                            trading_phase_profile_sub_wizard.is_field_trading_phase_profile_desc_required())
            except Exception as e:
                self.verify("Trading Phase Sequences field is not required", True, e.__class__.__name__)

            trading_phase_profile_sub_wizard.set_trading_phase(self.trading_phase)
            trading_phase_profile_sub_wizard.click_on_checkmark_at_trading_phase_profile_sequences()
            time.sleep(1)
            trading_phase_profile_sub_wizard.click_on_checkmark()
            time.sleep(1)
            wizard.click_on_go_back_button()
            time.sleep(2)
            profiles.set_trading_phase_profile(self.trading_phase_profile_desc)
            wizard.click_on_save_changes()
            time.sleep(2)
            page.set_name_filter(self.name)
            time.sleep(2)
            page.click_on_more_actions()
            time.sleep(2)
            page.click_on_edit()
            time.sleep(2)
            profiles = VenuesProfilesSubWizard(self.web_driver_container)

            try:
                self.verify("Is entity contains valid value after edited ", self.trading_phase_profile_desc,
                            profiles.get_trading_phase_profile())
            except Exception as e:
                self.verify("Entity contains invalid value after edited", True, e.__class__.__name__)

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
