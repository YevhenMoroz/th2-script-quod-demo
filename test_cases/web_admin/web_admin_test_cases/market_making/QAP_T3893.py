import random
import string
import sys
import time
import traceback

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.market_making.client_tier.client_tier_instrument_sweepable_quantities_sub_wizard \
    import ClientTiersInstrumentSweepableQuantitiesSubWizard
from test_framework.web_admin_core.pages.market_making.client_tier.client_tier_instrument_tenors_sub_wizard \
    import ClientTiersInstrumentTenorsSubWizard
from test_framework.web_admin_core.pages.market_making.client_tier.client_tier_instruments_page \
    import ClientTierInstrumentsPage
from test_framework.web_admin_core.pages.market_making.client_tier.client_tiers_page import ClientTiersPage
from test_framework.web_admin_core.pages.market_making.client_tier.client_tiers_values_sub_wizard \
    import ClientTiersValuesSubWizard
from test_framework.web_admin_core.pages.market_making.client_tier.client_tiers_wizard import ClientTiersWizard
from test_framework.web_admin_core.pages.market_making.client_tier.client_tier_instrument_values_sub_wizard \
    import ClientTierInstrumentValuesSubWizard
from test_framework.web_admin_core.pages.market_making.client_tier.client_tier_instrument_wizard \
    import ClientTierInstrumentWizard

from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T3893(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.core_spot_price_strategy = self.data_set.get_core_spot_price_strategy("core_spot_price_strategy_3")
        self.tenor_2 = self.data_set.get_tenor_by_name("tenor_2")
        self.symbol = self.data_set.get_symbol_by_name("symbol_1")
        self.position = -2
        self.quantity = 5000
        self.bid_margin = 5
        self.offer_margin = 4
        self.sweepable_quantities = 1000000
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
        self.verify(f"Client tier {self.name} has been created", True, True)
        time.sleep(2)
        client_tiers_main_page = ClientTiersPage(self.web_driver_container)
        client_tiers_main_page.set_name(self.name)
        time.sleep(1)
        client_tiers_main_page.click_on_more_actions()
        time.sleep(1)
        client_tier_instrument_main_page = ClientTierInstrumentsPage(self.web_driver_container)
        client_tier_instrument_main_page.click_on_new()
        time.sleep(2)

        client_tier_instrument_values_tab = ClientTierInstrumentValuesSubWizard(self.web_driver_container)
        client_tier_instrument_values_tab.set_symbol(self.symbol)
        client_tier_instrument_values_tab.set_tod_end_time(self.tod_end_time)

        time.sleep(2)
        client_tier_instrument_sweepable_quantities = ClientTiersInstrumentSweepableQuantitiesSubWizard(
            self.web_driver_container)
        client_tier_instrument_sweepable_quantities.click_on_plus()
        client_tier_instrument_sweepable_quantities.set_quantity(self.sweepable_quantities)
        client_tier_instrument_sweepable_quantities.click_on_checkmark()
        time.sleep(1)

        client_tier_instrument_wizard = ClientTierInstrumentWizard(self.web_driver_container)
        client_tier_instrument_wizard.click_on_save_changes()
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

    def test_context(self):
        try:
            self.precondition()

            client_tier_instrument_tenors_sub_wizard = ClientTiersInstrumentTenorsSubWizard(self.web_driver_container)
            client_tier_instrument_tenors_sub_wizard.click_on_plus()
            time.sleep(1)

            self.verify("Client PriceSlippageRange is not active", False,
                        client_tier_instrument_tenors_sub_wizard.is_client_price_slippage_range_field_enabled())

            client_tier_instrument_tenors_sub_wizard.click_on_client_price_slippage_range_checkbox()

            self.verify("Client PriceSlippageRange become active", True,
                        client_tier_instrument_tenors_sub_wizard.is_client_price_slippage_range_field_enabled())

            client_tier_instrument_tenors_sub_wizard.click_on_plus_button_at_base_margin_tab()
            time.sleep(1)

            client_tier_instrument_tenors_sub_wizard.click_on_plus_button_at_base_margin_tab()
            client_tier_instrument_tenors_sub_wizard.set_tenor(self.tenor_2)
            client_tier_instrument_tenors_sub_wizard.click_on_plus_button_at_base_margin_tab()
            client_tier_instrument_tenors_sub_wizard.set_quantity_at_base_margin_tab(self.quantity)
            client_tier_instrument_tenors_sub_wizard.set_bid_margin_at_base_margins_tab(self.bid_margin)
            client_tier_instrument_tenors_sub_wizard.set_offer_margin_at_base_margins_tab(self.offer_margin)
            client_tier_instrument_tenors_sub_wizard.click_on_checkmark_at_base_margins_tab()

            time.sleep(1)
            client_tier_instrument_tenors_sub_wizard.click_on_plus_button_at_position_levels_tab()
            client_tier_instrument_tenors_sub_wizard.set_position_at_position_levels_tab(self.position)
            client_tier_instrument_tenors_sub_wizard.set_bid_margin_at_position_levels_tab(self.position)
            client_tier_instrument_tenors_sub_wizard.set_offer_margin_at_position_levels_tab(self.offer_margin)
            client_tier_instrument_tenors_sub_wizard.click_on_checkmark_at_position_levels_tab()

            time.sleep(1)
            client_tier_instrument_tenors_sub_wizard.click_on_checkmark()

            time.sleep(1)
            client_tier_instrument_sweepable_quantities = ClientTiersInstrumentSweepableQuantitiesSubWizard(
                self.web_driver_container)
            client_tier_instrument_sweepable_quantities.click_on_delete_by_value(self.sweepable_quantities)

            client_tier_instrument_tenors_sub_wizard.click_on_edit()
            time.sleep(2)
            all_quantity_at_base_margin = client_tier_instrument_tenors_sub_wizard.\
                get_all_list_quantity_at_base_margin_tab()

            actual_result = False if str(self.sweepable_quantities) in all_quantity_at_base_margin else True

            self.verify("Deleted Quantity is not displayed ", True, actual_result)


        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
