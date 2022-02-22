import random
import string
import sys
import time
import traceback

from selenium.common.exceptions import TimeoutException

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.market_making.client_tier.client_tier_instrument_sweepable_quantities_sub_wizard import \
    ClientTiersInstrumentSweepableQuantitiesSubWizard
from test_framework.web_admin_core.pages.market_making.client_tier.client_tier_instrument_tenors_sub_wizard import \
    ClientTiersInstrumentTenorsSubWizard
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


class QAP_2649(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.core_spot_price_strategy = "Direct"
        self.tenor = "Spot"
        self.bid_margin = 555
        self.offer_margin = 444


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
    time.sleep(1)
    client_tiers_values_sub_wizard.set_core_spot_price_strategy(self.core_spot_price_strategy)
    client_tiers_wizard = ClientTiersWizard(self.web_driver_container)
    client_tiers_wizard.click_on_save_changes()
    time.sleep(2)


def test_context(self):
    try:
        self.precondition()
        client_tiers_main_page = ClientTiersPage(self.web_driver_container)
        try:
            client_tiers_main_page.set_name(self.name)
            self.verify("Is client tier created correctly? ", True, True)
        except Exception as e:
            self.verify("Is client  created INCORRECTLY !!!", True, e.__class__.__name__)
        time.sleep(2)
        client_tiers_main_page.click_on_more_actions()
        time.sleep(3)
        client_tier_instrument_main_page = ClientTierInstrumentsPage(self.web_driver_container)
        client_tier_instrument_main_page.click_on_new()
        time.sleep(2)
        client_tier_instrument_sweepable_quantities = ClientTiersInstrumentSweepableQuantitiesSubWizard(
            self.web_driver_container)
        client_tier_instrument_sweepable_quantities.click_on_plus()
        client_tier_instrument_sweepable_quantities.set_quantity(100000)
        client_tier_instrument_sweepable_quantities.click_on_published_checkbox()
        client_tier_instrument_sweepable_quantities.click_on_checkmark()
        client_tier_instrument_sweepable_quantities.click_on_plus()
        client_tier_instrument_sweepable_quantities.set_quantity(200000)
        client_tier_instrument_sweepable_quantities.click_on_published_checkbox()
        client_tier_instrument_sweepable_quantities.click_on_checkmark()
        client_tier_instrument_tenors_sub_wizard = ClientTiersInstrumentTenorsSubWizard(self.web_driver_container)
        client_tier_instrument_tenors_sub_wizard.click_on_plus()
        client_tier_instrument_tenors_sub_wizard.set_tenor(self.tenor)
        client_tier_instrument_tenors_sub_wizard.click_on_edit_at_base_margins_tab()
        client_tier_instrument_tenors_sub_wizard.set_bid_margin_at_base_margins_tab(self.bid_margin)
        client_tier_instrument_tenors_sub_wizard.set_offer_margin_at_base_margins_tab(self.offer_margin)
        client_tier_instrument_tenors_sub_wizard.click_on_checkmark_at_base_margins_tab()
        client_tier_instrument_tenors_sub_wizard.click_on_checkmark()
        client_tier_instrument_sweepable_quantities.set_quantity_filter(200000)
        time.sleep(2)
        client_tier_instrument_sweepable_quantities.click_on_delete()
        time.sleep(2)
        client_tier_instrument_tenors_sub_wizard.click_on_edit()
        client_tier_instrument_tenors_sub_wizard.set_quantity_filter_at_base_margins_tab(200000)
        time.sleep(2)
        try:
            client_tier_instrument_tenors_sub_wizard.click_on_edit_at_base_margins_tab()
            time.sleep(2)
            self.verify("Erorr, quantity does not deleted !!!", True, False)

        except TimeoutException as e:
            error_name = e.__class__.__name__
            self.verify("Quantity is not displayed and deleted successful", "TimeoutException", error_name)
    except Exception:
        basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                          status='FAILED')
        exc_type, exc_value, exc_traceback = sys.exc_info()
        traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
        print(" Search in ->  " + self.__class__.__name__)
