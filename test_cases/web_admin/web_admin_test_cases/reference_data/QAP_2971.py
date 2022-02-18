import random
import string
import sys
import time
import traceback

from custom import basic_custom_actions
from test_cases.web_admin.web_admin_core.pages.login.login_page import LoginPage
from test_cases.web_admin.web_admin_core.pages.reference_data.venues.nested_wizards.venues_trading_phase_profile_sub_wizard import \
    VenuesTradingPhaseProfileSubWizard
from test_cases.web_admin.web_admin_core.pages.reference_data.venues.venues_values_sub_wizard import \
    VenuesValuesSubWizard
from test_cases.web_admin.web_admin_core.pages.reference_data.venues.venues_page import VenuesPage
from test_cases.web_admin.web_admin_core.pages.reference_data.venues.venues_profiles_sub_wizard import \
    VenuesProfilesSubWizard
from test_cases.web_admin.web_admin_core.pages.reference_data.venues.venues_wizard import VenuesWizard
from test_cases.web_admin.web_admin_core.pages.root.side_menu import SideMenu
from test_cases.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_2971(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id)
        self.login = "adm02"
        self.password = "Qwerty123!"
        self.name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.id = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.type = "DarkPool"
        self.trading_phase_profile_desc = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.trading_phase = "Auction"

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
        time.sleep(1)
        description_sub_wizard.set_id(self.id)
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
            profiles.click_on_trading_phase_profile_mange_button()
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
