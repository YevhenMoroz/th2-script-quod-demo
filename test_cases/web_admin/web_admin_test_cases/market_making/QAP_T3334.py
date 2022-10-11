import sys
import time
import traceback

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.market_making.client_tier.client_tier_instrument_values_sub_wizard import \
    ClientTierInstrumentValuesSubWizard
from test_framework.web_admin_core.pages.market_making.client_tier.client_tier_instrument_tenors_sub_wizard import \
    ClientTiersInstrumentTenorsSubWizard
from test_framework.web_admin_core.pages.market_making.client_tier.client_tier_instrument_sweepable_quantities_sub_wizard import \
    ClientTiersInstrumentSweepableQuantitiesSubWizard
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


class QAP_T3334(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.name = 'QAP_T8433'
        self.core_spot_price_strategy = self.data_set.get_core_spot_price_strategy("core_spot_price_strategy_3")
        self.symbol = self.data_set.get_symbol_by_name("symbol_1")
        self.tod_end_time = "01:00:00"
        self.sweepable_qty = "1111111"
        self.tenor = 'Spot'
        self.base_margin_qty = ["2222222", "3333333", "4444444"]

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
            sweepable_quantities_tab = ClientTiersInstrumentSweepableQuantitiesSubWizard(self.web_driver_container)
            sweepable_quantities_tab.click_on_plus()
            sweepable_quantities_tab.set_quantity(self.sweepable_qty)
            sweepable_quantities_tab.click_on_checkmark()
            tenors_tab = ClientTiersInstrumentTenorsSubWizard(self.web_driver_container)
            tenors_tab.click_on_plus()
            tenors_tab.set_tenor(self.tenor)
            tenors_tab.click_on_checkmark()
            client_tiers_instrument_wizard = ClientTierInstrumentWizard(self.web_driver_container)
            client_tiers_instrument_wizard.click_on_save_changes()

    def test_context(self):
        try:
            self.precondition()

            client_tiers_frame = ClientTiersPage(self.web_driver_container)
            client_tiers_frame.set_name(self.name)
            client_tiers_frame.select_client_tier_by_name(self.name)
            client_tiers_frame.click_on_more_actions()
            time.sleep(1)
            client_tier_instrument_frame = ClientTierInstrumentsPage(self.web_driver_container)
            client_tier_instrument_frame.click_on_more_actions()
            client_tier_instrument_frame.click_on_edit()
            tenors_tab = ClientTiersInstrumentTenorsSubWizard(self.web_driver_container)
            tenors_tab.set_tenor_filter(self.tenor)
            tenors_tab.click_on_edit()
            time.sleep(1)
            tenors_tab.click_on_edit_at_base_margins_tab_by_values(self.sweepable_qty)
            time.sleep(1)
            actual_result = tenors_tab.is_quantity_field_enable_at_base_margin_tab()
            self.verify("Quantity field disabled", actual_result, False)

            tenors_tab.click_on_close_at_base_margins_tab()
            time.sleep(1)
            tenors_tab.click_on_plus_button_at_base_margin_tab()
            tenors_tab.set_quantity_at_base_margin_tab(self.base_margin_qty[0])
            tenors_tab.click_on_checkmark_at_base_margins_tab()
            tenors_tab.click_on_plus_button_at_base_margin_tab()
            tenors_tab.set_quantity_at_base_margin_tab(self.base_margin_qty[1])
            tenors_tab.click_on_checkmark_at_base_margins_tab()
            tenors_tab.click_on_checkmark()

            tenors_tab.set_tenor_filter(self.tenor)
            tenors_tab.click_on_edit()
            tenors_tab.click_on_edit_at_base_margins_tab_by_values(self.base_margin_qty[0])
            tenors_tab.set_quantity_at_base_margin_tab(self.base_margin_qty[2])
            tenors_tab.click_on_publish_prices_checkbox_at_base_margins_tab()
            tenors_tab.click_on_checkmark_at_base_margins_tab()
            tenors_tab.click_on_checkmark()

            tenors_tab.set_tenor_filter(self.tenor)
            tenors_tab.click_on_edit()
            tenors_tab.click_on_edit_at_base_margins_tab_by_values(self.base_margin_qty[2])
            self.verify("Changes values found, and Publish Price checkbox unselected", True,
                        tenors_tab.is_publish_prices_checkbox_selected_at_base_margins_tab())
            tenors_tab.click_on_checkmark_at_base_margins_tab()

            tenors_tab.click_on_delete_at_base_margins_tab_by_values(self.base_margin_qty[1])
            tenors_tab.click_on_delete_at_base_margins_tab_by_values(self.base_margin_qty[2])
            tenors_tab.click_on_checkmark()

            tenors_tab.set_tenor_filter(self.tenor)
            tenors_tab.click_on_edit()

            all_quantity_at_base_margin = tenors_tab.get_all_list_quantity_at_base_margin_tab()
            actual_result = False if str(self.base_margin_qty) in all_quantity_at_base_margin else True

            self.verify("Deleted Quantity is not displayed ", True, actual_result)

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
