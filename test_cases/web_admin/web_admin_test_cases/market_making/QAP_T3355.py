import sys
import time
import traceback
from pathlib import Path

from custom import basic_custom_actions
from test_framework.core.try_exept_decorator import try_except
from test_framework.web_admin_core.pages.market_making.client_tier.client_tier_instrument_values_sub_wizard import \
    ClientTierInstrumentValuesSubWizard
from test_framework.web_admin_core.pages.market_making.client_tier.client_tier_instrument_tenors_sub_wizard import \
    ClientTiersInstrumentTenorsSubWizard
from test_framework.web_admin_core.pages.market_making.client_tier.client_tier_instrument_tiered_quantities_sub_wizard \
    import ClientTiersInstrumentTieredQuantitiesSubWizard
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


class QAP_T3355(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.name = 'QAP_T3355'
        self.core_spot_price_strategy = self.data_set.get_core_spot_price_strategy("core_spot_price_strategy_3")
        self.symbol = self.data_set.get_symbol_by_name("symbol_1")
        self.tod_end_time = "23:59:59"
        self.tenor = 'Spot'
        self.tiered_quantity = "1000"

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        time.sleep(2)
        side_menu = SideMenu(self.web_driver_container)
        side_menu.open_client_tier_page()
        client_tiers_frame = ClientTiersPage(self.web_driver_container)
        client_tiers_frame.set_name(self.name)
        time.sleep(1)
        if not client_tiers_frame.is_searched_client_tiers_found(self.name):
            client_tiers_frame.click_on_new()
            client_tiers_values_tab = ClientTiersValuesSubWizard(self.web_driver_container)
            client_tiers_values_tab.set_name(self.name)
            client_tiers_values_tab.set_tod_end_time(self.tod_end_time)
            client_tiers_values_tab.set_core_spot_price_strategy(self.core_spot_price_strategy)
            client_tiers_wizard = ClientTiersWizard(self.web_driver_container)
            client_tiers_wizard.click_on_save_changes()
            client_tiers_frame.set_name(self.name)
            client_tiers_frame.select_client_tier_by_name(self.name)

            client_tier_instrument_frame = ClientTierInstrumentsPage(self.web_driver_container)
            client_tier_instrument_frame.click_on_new()
            instrument_values_tab = ClientTierInstrumentValuesSubWizard(self.web_driver_container)
            instrument_values_tab.set_symbol(self.symbol)
            instrument_values_tab.set_tod_end_time(self.tod_end_time)
            tenors_tab = ClientTiersInstrumentTenorsSubWizard(self.web_driver_container)
            tenors_tab.click_on_plus()
            tenors_tab.set_tenor(self.tenor)
            tenors_tab.click_on_checkmark()
            client_tiers_instrument_wizard = ClientTierInstrumentWizard(self.web_driver_container)
            client_tiers_instrument_wizard.click_on_save_changes()

    @try_except(test_id=Path(__file__).name[:-3])
    def test_context(self):
        self.precondition()

        client_tiers_frame = ClientTiersPage(self.web_driver_container)
        client_tiers_frame.set_name(self.name)
        client_tiers_frame.select_client_tier_by_name(self.name)
        client_tier_instrument_frame = ClientTierInstrumentsPage(self.web_driver_container)
        client_tier_instrument_frame.set_symbol(self.symbol)
        time.sleep(1)
        client_tier_instrument_frame.click_on_more_actions()
        client_tier_instrument_frame.click_on_edit()
        tiered_tab = ClientTiersInstrumentTieredQuantitiesSubWizard(self.web_driver_container)
        tiered_tab.click_on_plus()
        tiered_tab.set_quantity(self.tiered_quantity)
        tiered_tab.click_on_checkmark()
        tiered_tab.click_on_plus()
        tiered_tab.set_quantity(self.tiered_quantity)
        tiered_tab.click_on_checkmark()

        client_tiers_instrument_wizard = ClientTierInstrumentWizard(self.web_driver_container)
        self.verify("Such record is already exist displayed ", True,
                    client_tiers_instrument_wizard.is_such_record_exists_massage_displayed())


