import random
import string
import sys
import time
import traceback

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.market_making.client_tier.client_tier_instrument_values_sub_wizard import \
    ClientTierInstrumentValuesSubWizard
from test_framework.web_admin_core.pages.market_making.client_tier.client_tier_instrument_wizard import \
    ClientTierInstrumentWizard
from test_framework.web_admin_core.pages.market_making.client_tier.client_tier_instruments_page import \
    ClientTierInstrumentsPage
from test_framework.web_admin_core.pages.market_making.client_tier.client_tiers_page import ClientTiersPage
from test_framework.web_admin_core.pages.market_making.client_tier.client_tiers_values_sub_wizard import \
    ClientTiersValuesSubWizard
from test_framework.web_admin_core.pages.market_making.client_tier.client_tiers_wizard import ClientTiersWizard
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T3957(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.core_spot_price_strategy = self.data_set.get_core_spot_price_strategy("core_spot_price_strategy_3")
        self.symbol = self.data_set.get_symbol_by_name("symbol_1")
        self.tod_end_time = "01:00:00"

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        side_menu.open_client_tier_page()
        client_tiers_main_page = ClientTiersPage(self.web_driver_container)
        client_tiers_main_page.click_on_new()
        client_tiers_values_sub_wizard = ClientTiersValuesSubWizard(self.web_driver_container)
        client_tiers_values_sub_wizard.set_name(self.name)
        client_tiers_values_sub_wizard.set_tod_end_time(self.tod_end_time)
        client_tiers_values_sub_wizard.set_core_spot_price_strategy(self.core_spot_price_strategy)
        client_tiers_wizard = ClientTiersWizard(self.web_driver_container)
        client_tiers_wizard.click_on_save_changes()

    def test_context(self):
        try:
            self.precondition()
            client_tiers_main_page = ClientTiersPage(self.web_driver_container)
            client_tiers_instrument_wizard = ClientTierInstrumentWizard(self.web_driver_container)
            client_tiers_instrument_values_sub_wizard = ClientTierInstrumentValuesSubWizard(self.web_driver_container)
            try:
                client_tiers_main_page.set_name(self.name)
                self.verify("Is client tier created correctly? ", True, True)
                time.sleep(1)
            except Exception as e:
                self.verify("Is client  created INCORRECTLY !!!", True, e.__class__.__name__)
            client_tiers_main_page.select_client_tier_by_name(self.name)
            time.sleep(1)
            client_tier_instrument_main_page = ClientTierInstrumentsPage(self.web_driver_container)
            client_tier_instrument_main_page.click_on_new()
            client_tiers_instrument_values_sub_wizard.set_symbol(self.symbol)
            client_tiers_instrument_values_sub_wizard.set_tod_end_time(self.tod_end_time)
            client_tiers_instrument_values_sub_wizard.set_rfq_response_stream_ttl(22)
            client_tiers_instrument_wizard.click_on_save_changes()
            client_tiers_main_page.set_name(self.name)
            time.sleep(1)
            client_tiers_main_page.select_client_tier_by_name(self.name)
            time.sleep(1)
            client_tier_instrument_main_page.click_on_more_actions()
            time.sleep(1)
            client_tier_instrument_main_page.click_on_edit()
            client_tiers_instrument_values_sub_wizard.set_rfq_response_stream_ttl(55)
            client_tiers_instrument_wizard.click_on_save_changes()
            client_tiers_main_page.set_name(self.name)
            time.sleep(1)
            client_tiers_main_page.select_client_tier_by_name(self.name)
            time.sleep(1)
            client_tier_instrument_main_page.click_on_more_actions()
            time.sleep(1)
            client_tier_instrument_main_page.click_on_edit()
            self.verify("TTL changed correctly", 55,
                        client_tiers_instrument_values_sub_wizard.get_rfq_response_stream_ttl())


        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
