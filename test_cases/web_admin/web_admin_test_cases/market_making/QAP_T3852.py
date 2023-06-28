import random
import string
import sys
import time
import traceback
from pathlib import Path

from custom import basic_custom_actions
from test_framework.core.try_exept_decorator import try_except
from test_framework.web_admin_core.pages.market_making.client_tier.client_tier_instrument_tenors_sub_wizard import \
    ClientTiersInstrumentTenorsSubWizard
from test_framework.web_admin_core.pages.market_making.client_tier.client_tier_instrument_values_sub_wizard import \
    ClientTierInstrumentValuesSubWizard
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


class QAP_T3852(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.position_book = self.data_set.get_client("client_1")
        self.position_eur = "11"
        self.tenor = "2W"
        self.symbol = self.data_set.get_symbol_by_name("symbol_1")
        self.core_spot_price_strategy = self.data_set.get_core_spot_price_strategy("core_spot_price_strategy_3")
        self.tod_end_time = "01:00:00"

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        time.sleep(2)
        side_menu.open_client_tier_page()
        client_tiers_main_page = ClientTiersPage(self.web_driver_container)
        client_tiers_main_page.click_on_new()
        time.sleep(2)
        client_tiers_values_sub_wizard = ClientTiersValuesSubWizard(self.web_driver_container)
        client_tiers_values_sub_wizard.set_name(self.name)
        client_tiers_values_sub_wizard.set_core_spot_price_strategy(self.core_spot_price_strategy)
        client_tiers_values_sub_wizard.set_tod_end_time(self.tod_end_time)
        client_tiers_wizard = ClientTiersWizard(self.web_driver_container)
        client_tiers_wizard.click_on_save_changes()
        time.sleep(2)

    @try_except(test_id=Path(__file__).name[:-3])
    def test_context(self):
        self.precondition()
        client_tier_instrument_wizard = ClientTiersWizard(self.web_driver_container)
        client_tiers_main_page = ClientTiersPage(self.web_driver_container)
        time.sleep(2)
        client_tiers_main_page.set_name(self.name)
        time.sleep(2)
        client_tiers_main_page.click_on_more_actions()
        time.sleep(3)
        client_tier_instrument_main_page = ClientTierInstrumentsPage(self.web_driver_container)
        client_tier_instrument_main_page.click_on_new()
        time.sleep(2)
        client_tiers_instrument_values_sub_wizard = ClientTierInstrumentValuesSubWizard(self.web_driver_container)
        client_tiers_instrument_values_sub_wizard.set_symbol(self.symbol)
        client_tiers_instrument_values_sub_wizard.set_tod_end_time(self.tod_end_time)
        client_tier_instrument_wizard.click_on_save_changes()
        ########
        client_tiers_main_page.set_name(self.name)
        time.sleep(2)
        client_tiers_main_page.click_on_more_actions()
        time.sleep(12)
        client_tier_instrument_main_page = ClientTierInstrumentsPage(self.web_driver_container)
        client_tier_instrument_main_page.click_on_more_actions()
        time.sleep(2)
        client_tier_instrument_main_page.click_on_edit()
        time.sleep(2)
        client_tier_instrument_tenors_sub_wizard = ClientTiersInstrumentTenorsSubWizard(self.web_driver_container)
        client_tier_instrument_tenors_sub_wizard.click_on_plus()
        client_tier_instrument_tenors_sub_wizard.set_tenor(self.tenor)
        time.sleep(1)
        client_tier_instrument_tenors_sub_wizard.click_on_automated_margin_strategies_enabled_checkbox()
        time.sleep(1)
        client_tier_instrument_tenors_sub_wizard.click_on_position_based_margins()
        time.sleep(1)
        client_tier_instrument_tenors_sub_wizard.set_position_book(self.position_book)
        time.sleep(1)
        client_tier_instrument_tenors_sub_wizard.click_on_plus_button_at_position_levels_tab()
        time.sleep(1)
        client_tier_instrument_tenors_sub_wizard.set_position_at_position_levels_tab(self.position_eur)
        time.sleep(1)
        client_tier_instrument_tenors_sub_wizard.click_on_checkmark_at_position_levels_tab()
        time.sleep(1)
        client_tier_instrument_tenors_sub_wizard.click_on_checkmark()
        time.sleep(2)
        self.verify("Is Tenor contains correctly values in PDF", True,
                    client_tier_instrument_wizard.click_download_pdf_entity_button_and_check_pdf(self.tenor))
        time.sleep(2)
        client_tier_instrument_wizard.click_on_save_changes()
        time.sleep(2)
        client_tiers_main_page.set_name(self.name)
        time.sleep(2)
        client_tiers_main_page.click_on_more_actions()
        time.sleep(12)
        client_tier_instrument_main_page.click_on_more_actions()
        time.sleep(2)

        self.verify("Is Tenor saved correctly", True,
                    client_tier_instrument_main_page.click_download_pdf_entity_button_and_check_pdf(
                        self.tenor))

