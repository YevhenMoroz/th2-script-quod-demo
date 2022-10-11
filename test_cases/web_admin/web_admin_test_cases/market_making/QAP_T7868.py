import sys
import time
import traceback

from custom import basic_custom_actions

from test_framework.web_admin_core.pages.market_making.client_tier.client_tier_instrument_tiered_quantities_sub_wizard \
    import ClientTiersInstrumentTieredQuantitiesSubWizard
from test_framework.web_admin_core.pages.market_making.client_tier.client_tier_instrument_sweepable_quantities_sub_wizard \
    import ClientTiersInstrumentSweepableQuantitiesSubWizard
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


class QAP_T7868(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.name = 'QAP_T7868'
        self.core_spot_price_strategy = self.data_set.get_core_spot_price_strategy("core_spot_price_strategy_3")
        self.tod_end_time = "01:00:00"
        self.tiered_quantity = ["101", "1", "99", "100"]
        self.sweepable_quantity = ["100", "150", "50"]

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
        else:
            client_tiers_frame.select_client_tier_by_name(self.name)

    def test_context(self):
        try:
            self.precondition()

            client_tier_instrument_frame = ClientTierInstrumentsPage(self.web_driver_container)
            client_tier_instrument_frame.click_on_new()
            instrument_sweepable_qty_tab = ClientTiersInstrumentSweepableQuantitiesSubWizard(self.web_driver_container)
            instrument_sweepable_qty_tab.click_on_plus()
            instrument_sweepable_qty_tab.set_quantity(self.sweepable_quantity[0])
            instrument_sweepable_qty_tab.click_on_checkmark()

            instrument_tiered_qty_tab = ClientTiersInstrumentTieredQuantitiesSubWizard(self.web_driver_container)
            instrument_tiered_qty_tab.click_on_plus()
            instrument_tiered_qty_tab.set_quantity(self.tiered_quantity[0])
            instrument_tiered_qty_tab.click_on_checkmark()

            self.verify("Is warning displayed", True, instrument_tiered_qty_tab.is_warning_displayed())

            instrument_sweepable_qty_tab.click_on_edit()
            instrument_sweepable_qty_tab.set_quantity(self.sweepable_quantity[1])
            instrument_sweepable_qty_tab.click_on_checkmark()
            instrument_sweepable_qty_tab.click_on_plus()
            instrument_sweepable_qty_tab.set_quantity(self.sweepable_quantity[2])
            instrument_sweepable_qty_tab.click_on_checkmark()

            self.verify("Is warning displayed", False, instrument_tiered_qty_tab.is_warning_displayed())

            instrument_tiered_qty_tab.click_on_plus()
            instrument_tiered_qty_tab.set_quantity(self.tiered_quantity[1])
            instrument_tiered_qty_tab.click_on_checkmark()

            self.verify("Is warning displayed", False, instrument_tiered_qty_tab.is_warning_displayed())

            instrument_tiered_qty_tab.click_on_plus()
            instrument_tiered_qty_tab.set_quantity(self.tiered_quantity[2])
            instrument_tiered_qty_tab.click_on_checkmark()

            self.verify("Is warning displayed", True, instrument_tiered_qty_tab.is_warning_displayed())

            instrument_tiered_qty_tab.click_on_plus()
            instrument_tiered_qty_tab.set_quantity(self.tiered_quantity[3])
            instrument_tiered_qty_tab.click_on_checkmark()

            self.verify("Is warning displayed", True, instrument_tiered_qty_tab.is_warning_displayed())

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
