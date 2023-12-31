import random
import string
import sys
import time
import traceback
from pathlib import Path

from selenium.common.exceptions import TimeoutException

from custom import basic_custom_actions
from test_framework.core.try_exept_decorator import try_except
from test_framework.web_admin_core.pages.market_making.client_tier.client_tier_instrument_sweepable_quantities_sub_wizard import \
    ClientTiersInstrumentSweepableQuantitiesSubWizard
from test_framework.web_admin_core.pages.market_making.client_tier.client_tier_instrument_tenors_sub_wizard import \
    ClientTiersInstrumentTenorsSubWizard
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


class QAP_T3960(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        print(self.name)
        self.core_spot_price_strategy = self.data_set.get_core_spot_price_strategy("core_spot_price_strategy_3")
        self.symbol = self.data_set.get_symbol_by_name("symbol_2")
        self.tenor_1 = self.data_set.get_tenor_by_name("tenor_1")
        self.tenor_2 = self.data_set.get_tenor_by_name("tenor_2")
        self.sweepable_quantities = [111111, 2222222, 33333333]
        self.base_margin_quantity = 4444444
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
        client_tiers_values_sub_wizard.set_tod_end_time(self.tod_end_time)
        time.sleep(1)
        client_tiers_values_sub_wizard.set_core_spot_price_strategy(self.core_spot_price_strategy)
        client_tiers_wizard = ClientTiersWizard(self.web_driver_container)
        client_tiers_wizard.click_on_save_changes()
        time.sleep(2)
        self.verify(f"Client tier {self.name} has been created", True, True)

        client_tiers_main_page = ClientTiersPage(self.web_driver_container)
        client_tiers_instrument_wizard = ClientTierInstrumentWizard(self.web_driver_container)
        client_tier_instrument_main_page = ClientTierInstrumentsPage(self.web_driver_container)
        client_tier_instrument_sweepable_quantities = ClientTiersInstrumentSweepableQuantitiesSubWizard(
            self.web_driver_container)
        client_tier_instrument_values_sub_wizard = ClientTierInstrumentValuesSubWizard(self.web_driver_container)

        time.sleep(2)
        client_tiers_main_page.set_name(self.name)
        time.sleep(1)
        client_tiers_main_page.click_on_more_actions()
        time.sleep(2)
        client_tier_instrument_main_page.click_on_new()
        time.sleep(2)
        client_tier_instrument_values_sub_wizard.set_symbol(self.symbol)
        client_tier_instrument_values_sub_wizard.set_tod_end_time(self.tod_end_time)
        client_tier_instrument_sweepable_quantities.click_on_plus()
        client_tier_instrument_sweepable_quantities.set_quantity(self.sweepable_quantities[0])
        client_tier_instrument_sweepable_quantities.click_on_published_checkbox()
        time.sleep(1)
        client_tier_instrument_sweepable_quantities.click_on_checkmark()
        client_tier_instrument_sweepable_quantities.click_on_plus()
        client_tier_instrument_sweepable_quantities.set_quantity(self.sweepable_quantities[1])
        client_tier_instrument_sweepable_quantities.click_on_published_checkbox()
        time.sleep(1)
        client_tier_instrument_sweepable_quantities.click_on_checkmark()
        client_tier_instrument_sweepable_quantities.click_on_plus()
        client_tier_instrument_sweepable_quantities.set_quantity(self.sweepable_quantities[2])
        client_tier_instrument_sweepable_quantities.click_on_published_checkbox()
        time.sleep(1)
        client_tier_instrument_sweepable_quantities.click_on_checkmark()

        client_tier_instrument_tenors_sub_wizard = ClientTiersInstrumentTenorsSubWizard(self.web_driver_container)
        client_tier_instrument_tenors_sub_wizard.click_on_plus()
        time.sleep(2)
        client_tier_instrument_tenors_sub_wizard.set_tenor(self.tenor_1)
        time.sleep(1)
        client_tier_instrument_tenors_sub_wizard.click_on_plus_button_at_base_margin_tab()
        client_tier_instrument_tenors_sub_wizard.set_quantity_at_base_margin_tab(self.base_margin_quantity)
        client_tier_instrument_tenors_sub_wizard.click_on_checkmark_at_base_margins_tab()
        client_tier_instrument_tenors_sub_wizard.click_on_checkmark()
        time.sleep(1)
        client_tier_instrument_tenors_sub_wizard.click_on_plus()
        time.sleep(1)
        client_tier_instrument_tenors_sub_wizard.set_tenor(self.tenor_2)
        time.sleep(1)
        client_tier_instrument_tenors_sub_wizard.click_on_plus_button_at_base_margin_tab()
        client_tier_instrument_tenors_sub_wizard.set_quantity_at_base_margin_tab(self.base_margin_quantity)
        client_tier_instrument_tenors_sub_wizard.click_on_checkmark_at_base_margins_tab()
        client_tier_instrument_tenors_sub_wizard.click_on_checkmark()
        time.sleep(2)
        client_tiers_instrument_wizard.click_on_save_changes()
        time.sleep(2)

        client_tiers_main_page.set_name(self.name)
        time.sleep(1)
        client_tiers_main_page.click_on_more_actions()

        time.sleep(2)
        client_tier_instrument_main_page.set_symbol(self.symbol)
        time.sleep(1)
        client_tier_instrument_main_page.click_on_more_actions()
        time.sleep(1)
        client_tier_instrument_main_page.click_on_edit()

    @try_except(test_id=Path(__file__).name[:-3])
    def test_context(self):
        self.precondition()

        client_tier_instrument_sweepable_quantities = ClientTiersInstrumentSweepableQuantitiesSubWizard(
            self.web_driver_container)

        client_tier_instrument_sweepable_quantities.click_on_delete_by_value(self.sweepable_quantities[1])
        time.sleep(2)

        client_tier_instrument_tenors_sub_wizard = ClientTiersInstrumentTenorsSubWizard(self.web_driver_container)
        client_tier_instrument_tenors_sub_wizard.click_on_created_tenor(self.tenor_1)
        time.sleep(2)
        all_quantity_at_base_margin = client_tier_instrument_tenors_sub_wizard. \
            get_all_list_quantity_at_base_margin_tab()

        actual_result = False if str(self.sweepable_quantities[1]) in all_quantity_at_base_margin else True

        self.verify(f"Deleted Quantity is not displayed inside {self.tenor_1}", True, actual_result)

        time.sleep(2)
        client_tier_instrument_tenors_sub_wizard.click_on_created_tenor(self.tenor_2)
        time.sleep(2)
        all_quantity_at_base_margin = client_tier_instrument_tenors_sub_wizard. \
            get_all_list_quantity_at_base_margin_tab()

        actual_result = False if str(self.sweepable_quantities[1]) in all_quantity_at_base_margin else True

        self.verify(f"Deleted Quantity is not displayed inside {self.tenor_2}", True, actual_result)

