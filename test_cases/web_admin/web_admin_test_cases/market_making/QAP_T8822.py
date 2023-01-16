import random
import string
import sys
import time
import traceback

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.market_making.client_tier.client_tiers_wizard import ClientTiersWizard
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase
from test_framework.web_admin_core.pages.market_making.client_tier.client_tiers_page import ClientTiersPage
from test_framework.web_admin_core.pages.market_making.client_tier.client_tiers_values_sub_wizard import \
    ClientTiersValuesSubWizard
from test_framework.web_admin_core.pages.market_making.client_tier.client_tier_instrument_values_sub_wizard import \
    ClientTierInstrumentValuesSubWizard
from test_framework.web_admin_core.pages.market_making.client_tier.client_tier_instruments_page import \
    ClientTierInstrumentsPage
from test_framework.web_admin_core.pages.market_making.client_tier.client_tier_instrument_client_tier_sub_wizard import \
    ClientTiersInstrumentClientTierSubWizard
from test_framework.web_admin_core.pages.market_making.client_tier.client_tier_instrument_wizard import \
    ClientTierInstrumentWizard


class QAP_T8822(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.core_spot_price_strategy = self.data_set.get_core_spot_price_strategy("core_spot_price_strategy_3")
        self.symbol = self.data_set.get_symbol_by_name("symbol_4")
        self.tod_end_time = "23:59:00"
        self.instrument_client_tier = "Gold"
        self.default_weight = str(random.randint(1, 50))

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

    def postcondition(self):
        side_menu = SideMenu(self.web_driver_container)
        side_menu.open_client_tier_page()
        client_tiers_main_page = ClientTiersPage(self.web_driver_container)
        client_tiers_main_page.set_name(self.name)
        time.sleep(1)
        client_tiers_main_page.click_on_more_actions()
        client_tiers_main_page.click_on_delete_and_confirmation(True)

    def test_context(self):
        try:
            self.precondition()

            client_tiers_main_page = ClientTiersPage(self.web_driver_container)
            client_tiers_main_page.set_name(self.name)
            time.sleep(1)
            client_tiers_main_page.select_client_tier_by_name(self.name)

            instrument_main_page = ClientTierInstrumentsPage(self.web_driver_container)
            instrument_main_page.click_on_new()
            instrument_values_tab = ClientTierInstrumentValuesSubWizard(self.web_driver_container)
            instrument_values_tab.set_symbol(self.symbol)
            instrument_values_tab.set_tod_end_time(self.tod_end_time)
            instrument_client_tiers_tab = ClientTiersInstrumentClientTierSubWizard(self.web_driver_container)
            instrument_client_tiers_tab.click_on_plus()
            instrument_client_tiers_tab.set_client_tiers(self.instrument_client_tier)
            instrument_client_tiers_tab.select_critical_checkbox()
            instrument_client_tiers_tab.set_default_weight(self.default_weight)
            instrument_client_tiers_tab.click_on_checkmark()

            instrument_wizard = ClientTierInstrumentWizard(self.web_driver_container)
            instrument_wizard.click_on_save_changes()

            client_tiers_main_page.set_name(self.name)
            time.sleep(1)
            client_tiers_main_page.select_client_tier_by_name(self.name)
            instrument_main_page.set_symbol(self.symbol)
            time.sleep(1)
            instrument_main_page.click_on_more_actions()
            instrument_main_page.click_on_edit()

            instrument_client_tiers_tab.set_client_tiers_filter(self.instrument_client_tier)
            instrument_client_tiers_tab.click_on_edit()

            expected_result = [self.instrument_client_tier, True, self.default_weight]
            actual_result = [instrument_client_tiers_tab.get_client_tiers(),
                             instrument_client_tiers_tab.is_critical_checkbox_selected(),
                             instrument_client_tiers_tab.get_default_weight()]

            self.verify("Instrument Client Tiers entity displayed saved data", expected_result, actual_result)

            self.postcondition()

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
