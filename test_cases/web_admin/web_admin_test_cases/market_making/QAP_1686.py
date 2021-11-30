import sys
import time
import traceback

from custom import basic_custom_actions
from test_cases.web_admin.web_admin_core.pages.market_making.client_tier.client_tier_instrument_values_sub_wizard import \
    ClientTierInstrumentValuesSubWizard
from test_cases.web_admin.web_admin_core.pages.market_making.client_tier.client_tier_instruments_page import \
    ClientTierInstrumentsPage
from test_cases.web_admin.web_admin_core.pages.market_making.client_tier.client_tiers_page import ClientTiersPage
from test_cases.web_admin.web_admin_core.pages.market_making.client_tier.client_tiers_wizard import ClientTiersWizard
from test_cases.web_admin.web_admin_core.pages.login.login_page import LoginPage
from test_cases.web_admin.web_admin_core.pages.root.side_menu import SideMenu
from test_cases.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_1686(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id)
        self.login = "adm03"
        self.password = "adm03"
        self.symbol = "EUR/USD"


    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        time.sleep(2)
        side_menu.open_client_tier_page()
        client_tiers_main_page = ClientTiersPage(self.web_driver_container)
        client_tier_instrument_main_page = ClientTierInstrumentsPage(self.web_driver_container)
        time.sleep(2)
        client_tier_instrument_main_page.click_on_new()
        time.sleep(2)
        client_tiers_wizard = ClientTiersWizard(self.web_driver_container)
        client_tier_instrument_values_sub_wizard = ClientTierInstrumentValuesSubWizard(self.web_driver_container)
        client_tier_instrument_values_sub_wizard.set_symbol(self.symbol)
        client_tiers_wizard.click_on_save_changes()
        time.sleep(2)
        client_tiers_main_page.click_on_more_actions()
        time.sleep(2)
        client_tier_instrument_main_page.set_symbol(self.symbol)
        time.sleep(2)
        client_tier_instrument_main_page.click_on_enable_disable()
        client_tiers_wizard.click_on_ok_button()
        time.sleep(2)
        client_tier_instrument_main_page.click_on_new()
        time.sleep(2)

    def test_context(self):

        try:
            self.precondition()
            client_tier_instrument_values_sub_wizard = ClientTierInstrumentValuesSubWizard(self.web_driver_container)
            client_tiers_wizard = ClientTiersWizard(self.web_driver_container)
            client_tier_instrument_values_sub_wizard.set_symbol(self.symbol)
            client_tiers_wizard.click_on_save_changes()
            time.sleep(2)
            self.verify("Same client tier created", True, True)

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
