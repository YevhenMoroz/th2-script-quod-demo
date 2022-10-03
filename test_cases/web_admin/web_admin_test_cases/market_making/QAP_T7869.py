import sys
import traceback

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.market_making.client_tier.client_tier_instruments_page \
    import ClientTierInstrumentsPage
from test_framework.web_admin_core.pages.market_making.client_tier.client_tier_instrument_values_sub_wizard import \
    ClientTierInstrumentValuesSubWizard
from test_framework.web_admin_core.pages.market_making.client_tier.client_tier_instrument_wizard import \
    ClientTierInstrumentWizard

from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T7869(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.core_spot_price_strategy = 'Direct'
        self.tod_end_time = "15:00:00"

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        side_menu.open_client_tier_page()

    def test_context(self):
        try:
            instrument_page = ClientTierInstrumentsPage(self.web_driver_container)
            wizard = ClientTierInstrumentWizard(self.web_driver_container)
            values_tab = ClientTierInstrumentValuesSubWizard(self.web_driver_container)

            self.precondition()

            instrument_page.click_on_new()
            self.verify("'Symbol' field contains '*' symbol", True,
                        values_tab.is_symbol_filed_contains_asterisk_symbol())

            values_tab.set_core_spot_price_strategy(self.core_spot_price_strategy)
            values_tab.set_tod_end_time(self.tod_end_time)
            wizard.click_on_save_changes()

            self.verify("Error message appears in footer", True,
                        wizard.is_incorrect_or_missing_value_massage_displayed())


        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
