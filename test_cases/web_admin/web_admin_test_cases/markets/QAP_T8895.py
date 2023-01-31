import random
import string
import sys
import time
import traceback

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.login.login_page import LoginPage

from test_framework.web_admin_core.pages.markets.venues.venues_page import VenuesPage
from test_framework.web_admin_core.pages.markets.venues.venues_wizard import VenuesWizard
from test_framework.web_admin_core.pages.markets.venues.venues_profiles_sub_wizard import VenuesProfilesSubWizard
from test_framework.web_admin_core.pages.markets.venues.nested_wizards.venues_trading_phase_profile_sub_wizard \
    import VenuesTradingPhaseProfileSubWizard

from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T8895(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.id = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.type = self.data_set.get_venue_type("venue_type_1")
        self.client_venue_id = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))

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
            profiles_tab = VenuesProfilesSubWizard(self.web_driver_container)
            profiles_tab.click_on_trading_phase_profile_manage_button()
            trading_phase_profile_wizard = VenuesTradingPhaseProfileSubWizard(self.web_driver_container)
            trading_phase_profile_wizard.click_on_edit()
            name = trading_phase_profile_wizard.get_trading_phase_profile_desc()

            trading_phase_profile_wizard.click_on_close()
            trading_phase_profile_wizard.set_trading_phase_profile_desc_filter(name)
            time.sleep(1)
            trading_phase_profile_wizard.click_on_delete()
            wizard = VenuesWizard(self.web_driver_container)
            wizard.click_on_ok_button()
            trading_phase_profile_wizard.set_trading_phase_profile_desc_filter(name)
            time.sleep(1)
            self.verify('Trading Phase Profile not displaying after delete', False,
                        trading_phase_profile_wizard.is_searched_trading_phase_profile_found(name))

            wizard.click_on_go_back_button()
            try:
                profiles_tab.set_trading_phase_profile(name)
                self.verify('Delete Trading Phase Profile can be selected in the Venue wizard', True, False)
            except:
                self.verify('Trading Phase Profile not displaying  in the Venue wizard after delete', True, True)

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
