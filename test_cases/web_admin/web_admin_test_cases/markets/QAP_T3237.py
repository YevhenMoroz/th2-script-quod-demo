import sys
import traceback

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.markets.venues.nested_wizards.venues_trading_phase_profile_sub_wizard \
    import VenuesTradingPhaseProfileSubWizard
from test_framework.web_admin_core.pages.markets.venues.venues_page import VenuesPage
from test_framework.web_admin_core.pages.markets.venues.venues_profiles_sub_wizard import \
    VenuesProfilesSubWizard
from test_framework.web_admin_core.pages.markets.venues.venues_wizard import VenuesWizard
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T3237(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")

        self.trading_phase = self.data_set.get_trading_phase("trading_phase_3")
        self.begin_time = '13:45:43'
        self.end_time = '13:45:00'

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        side_menu.open_venues_page()

    def test_context(self):
        try:
            self.precondition()

            page = VenuesPage(self.web_driver_container)
            page.click_on_new()

            profiles = VenuesProfilesSubWizard(self.web_driver_container)
            profiles.click_on_trading_phase_profile_mange_button()

            trading_phase_profile_sub_wizard = VenuesTradingPhaseProfileSubWizard(self.web_driver_container)
            trading_phase_profile_sub_wizard.click_on_plus_button()
            trading_phase_profile_sub_wizard.click_on_plus_button_at_trading_phase_profile_sequences()
            trading_phase_profile_sub_wizard.set_trading_phase(self.trading_phase)
            trading_phase_profile_sub_wizard.set_end_time(self.end_time)
            trading_phase_profile_sub_wizard.set_begin_time(self.begin_time)
            trading_phase_profile_sub_wizard.click_on_checkmark_at_trading_phase_profile_sequences()

            wizard = VenuesWizard(self.web_driver_container)
            expected_result = 'The start time cannot be earlier than end time'
            actual_result = wizard.get_footer_error_text()

            self.verify("Footer error appears", expected_result, actual_result)

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
