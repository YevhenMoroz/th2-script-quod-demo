import sys
import time
import traceback

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.risk_limits.trading_limits.trading_limits_page import TradingLimitsPage
from test_framework.web_admin_core.pages.risk_limits.trading_limits.trading_limits_dimensions_sub_wizard \
    import TradingLimitsDimensionsSubWizardPage
from test_framework.web_admin_core.pages.risk_limits.cum_trading_limits.cum_trading_limits_page \
    import CumTradingLimitsPage
from test_framework.web_admin_core.pages.risk_limits.cum_trading_limits.cum_trading_limits_dimensions_sub_wizard \
    import CumTradingLimitsDimensionsSubWizard
from test_framework.web_admin_core.pages.risk_limits.position_limits.position_limits_page import PositionLimitsPage
from test_framework.web_admin_core.pages.risk_limits.position_limits.position_limits_dimensions_sub_wizard \
    import PositionLimitsDimensionsSubWizard
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T3230(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        time.sleep(2)

    def test_context(self):
        try:
            self.precondition()

            side_menu = SideMenu(self.web_driver_container)
            side_menu.open_trading_limits_page()
            time.sleep(2)
            trading_limits_page = TradingLimitsPage(self.web_driver_container)
            trading_limits_page.click_on_new()
            time.sleep(2)
            trading_limits_dimensions_tab = TradingLimitsDimensionsSubWizardPage(self.web_driver_container)
            expected_displayed_fields = ['Venue', 'SubVenue', 'ListingGroup', 'User', 'Client',
                                                'Client Group', 'Desk', 'Route', 'Instrument Type',
                                                'InstrSybmol', 'Execution Policy', 'Phase']
            displayed_fields = [
                            trading_limits_dimensions_tab.is_venue_field_displayed(),
                            trading_limits_dimensions_tab.is_sub_venue_field_displayed(),
                            trading_limits_dimensions_tab.is_listing_group_field_displayed(),
                            trading_limits_dimensions_tab.is_user_field_displayed(),
                            trading_limits_dimensions_tab.is_client_field_displayed(),
                            trading_limits_dimensions_tab.is_client_group_field_displayed(),
                            trading_limits_dimensions_tab.is_desk_field_displayed(),
                            trading_limits_dimensions_tab.is_route_field_displayed(),
                            trading_limits_dimensions_tab.is_instrument_type_field_displayed(),
                            trading_limits_dimensions_tab.is_instr_symbol_field_displayed(),
                            trading_limits_dimensions_tab.is_execution_policy_field_displayed(),
                            trading_limits_dimensions_tab.is_phase_field_displayed()
                        ]
            self.verify("The Dimension section is present with fields:",
                        [i + ": True" for i in expected_displayed_fields],
                        [expected_displayed_fields[i] + f": {displayed_fields[i]}" for i in
                         range(len(displayed_fields))])

            side_menu.open_cum_trading_limits_page()
            time.sleep(2)

            cum_trading_limits_page = CumTradingLimitsPage(self.web_driver_container)
            cum_trading_limits_page.click_on_new()
            time.sleep(2)
            cum_trading_limits_dimensions_tab = CumTradingLimitsDimensionsSubWizard(self.web_driver_container)
            expected_displayed_fields = ['Venue', 'SubVenue', 'ListingGroup', 'Listing', 'User',
                                         'Desk', 'Route', 'Instrument Type',
                                         'Client', 'Client Group', 'InstrSybmol', 'Account']
            displayed_fields = [
                cum_trading_limits_dimensions_tab.is_venue_field_displayed(),
                cum_trading_limits_dimensions_tab.is_sub_venue_field_displayed(),
                cum_trading_limits_dimensions_tab.is_listing_group_field_displayed(),
                cum_trading_limits_dimensions_tab.is_listing_field_displayed(),
                cum_trading_limits_dimensions_tab.is_user_field_displayed(),
                cum_trading_limits_dimensions_tab.is_desk_field_displayed(),
                cum_trading_limits_dimensions_tab.is_route_field_displayed(),
                cum_trading_limits_dimensions_tab.is_instrument_type_field_displayed(),
                cum_trading_limits_dimensions_tab.is_client_field_displayed(),
                cum_trading_limits_dimensions_tab.is_client_group_field_displayed(),
                cum_trading_limits_dimensions_tab.is_instr_symbol_field_displayed(),
                cum_trading_limits_dimensions_tab.is_account_field_displayed()
            ]
            self.verify("The Dimension section is present with fields:",
                        [i + ": True" for i in expected_displayed_fields],
                        [expected_displayed_fields[i] + f": {displayed_fields[i]}" for i in
                         range(len(displayed_fields))])

            side_menu.open_positions_limits_page()
            time.sleep(2)
            position_limits_page = PositionLimitsPage(self.web_driver_container)
            position_limits_page.click_on_new()
            time.sleep(2)
            position_limits_dimensions_tab = PositionLimitsDimensionsSubWizard(self.web_driver_container)
            expected_displayed_fields = ['Instrument', 'Instrument Group', 'Instrument Type', 'Account']
            displayed_fields = [position_limits_dimensions_tab.is_instrument_field_displayed(),
                                position_limits_dimensions_tab.is_instrument_group_field_displayed(),
                                position_limits_dimensions_tab.is_instrument_type_field_displayed(),
                                position_limits_dimensions_tab.is_account_type_field_displayed()]
            self.verify("The Dimension section is present with fields:",
                        [i + ": True" for i in expected_displayed_fields],
                        [expected_displayed_fields[i] + f": {displayed_fields[i]}" for i in
                         range(len(displayed_fields))])


        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
