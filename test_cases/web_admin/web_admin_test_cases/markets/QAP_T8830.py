import random
import string
import sys
import time
import traceback

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.markets.venues.venues_page import VenuesPage
from test_framework.web_admin_core.pages.markets.venues.venues_values_sub_wizard import \
    VenuesValuesSubWizard
from test_framework.web_admin_core.pages.markets.venues.venues_phase_session_sub_wizard import \
    VenuesPhaseSessionSubWizard
from test_framework.web_admin_core.pages.markets.venues.venues_wizard import VenuesWizard
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T8830(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.id = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.type = "DarkPool"
        self.client_venue_id = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))

        self.trading_phase = '210'
        self.trading_session = ''.join(random.sample((string.ascii_uppercase + string.digits) * 4, 4))
        self.time_in_force = 'TradeAtLast'
        self.ord_type = 'NotSpecified'
        self.short_name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        side_menu.open_venues_page()
        page = VenuesPage(self.web_driver_container)
        page.click_on_new()
        values_tab = VenuesValuesSubWizard(self.web_driver_container)
        values_tab.set_name(self.name)
        values_tab.set_id(self.id)
        values_tab.set_type(self.type)
        values_tab.set_client_venue_id(self.client_venue_id)

        phase_session_tab = VenuesPhaseSessionSubWizard(self.web_driver_container)
        phase_session_tab.click_on_plus_button()
        phase_session_tab.set_trading_phase(self.trading_phase)
        phase_session_tab.set_trading_session(self.trading_session)
        phase_session_tab.click_on_plus_button_at_type_tif()
        phase_session_tab.set_time_in_force(self.time_in_force)
        phase_session_tab.set_ord_type(self.ord_type)
        phase_session_tab.click_on_checkmark_at_type_tif()
        phase_session_tab.click_on_checkmark()
        wizard = VenuesWizard(self.web_driver_container)
        wizard.click_on_save_changes()

    def test_context(self):
        try:
            self.precondition()

            page = VenuesPage(self.web_driver_container)
            page.set_name_filter(self.name)
            time.sleep(1)
            page.click_on_more_actions()
            page.click_on_edit()
            values_tab = VenuesValuesSubWizard(self.web_driver_container)
            values_tab.set_short_name(self.short_name)
            wizard = VenuesWizard(self.web_driver_container)
            wizard.click_on_save_changes()

            page.set_name_filter(self.name)
            time.sleep(1)
            page.click_on_more_actions()
            page.click_on_edit()
            self.verify("Modification is accepted, Venue changed saved", self.short_name, values_tab.get_short_name())

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
