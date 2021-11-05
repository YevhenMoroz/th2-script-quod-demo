import random
import string
import time
import traceback

from custom import basic_custom_actions
from quod_qa.web_admin.web_admin_core.pages.fx_market_making.client_tier.client_tier_instrument_external_clients_sub_wizard import \
    ClientTiersInstrumentExternalClientsSubWizard
from quod_qa.web_admin.web_admin_core.pages.fx_market_making.client_tier.client_tier_instrument_forward_venues_sub_wizard import \
    ClientTiersInstrumentForwardVenuesSubWizard
from quod_qa.web_admin.web_admin_core.pages.fx_market_making.client_tier.client_tier_instrument_internal_clients_sub_wizard import \
    ClientTiersInstrumentInternalClientsSubWizard
from quod_qa.web_admin.web_admin_core.pages.fx_market_making.client_tier.client_tier_instrument_spot_venues_sub_wizard import \
    ClientTiersInstrumentSpotVenuesSubWizard
from quod_qa.web_admin.web_admin_core.pages.fx_market_making.client_tier.client_tier_instrument_sweepable_quantities_sub_wizard import \
    ClientTiersInstrumentSweepableQuantitiesSubWizard
from quod_qa.web_admin.web_admin_core.pages.fx_market_making.client_tier.client_tier_instrument_tenors_sub_wizard import \
    ClientTiersInstrumentTenorsSubWizard
from quod_qa.web_admin.web_admin_core.pages.fx_market_making.client_tier.client_tier_instrument_values_sub_wizard import \
    ClientTierInstrumentValuesSubWizard
from quod_qa.web_admin.web_admin_core.pages.fx_market_making.client_tier.client_tier_instruments_page import \
    ClientTierInstrumentsPage
from quod_qa.web_admin.web_admin_core.pages.fx_market_making.client_tier.client_tiers_page import ClientTiersPage
from quod_qa.web_admin.web_admin_core.pages.fx_market_making.client_tier.client_tiers_values_sub_wizard import \
    ClientTiersValuesSubWizard
from quod_qa.web_admin.web_admin_core.pages.fx_market_making.client_tier.client_tiers_wizard import ClientTiersWizard
from quod_qa.web_admin.web_admin_core.pages.login.login_page import LoginPage
from quod_qa.web_admin.web_admin_core.pages.root.side_menu import SideMenu
from quod_qa.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer
from quod_qa.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_1647(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id)
        self.login = "adm03"
        self.password = "adm03"
        self.name =''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.core_spot_price_strategy = "Direct"
        self.symbol = "AUD/CAD"
        self.rfq_response_stream_ttl = 2
        self.venue_at_spot_venues_tab = "MS RFQ"
        self.venue_at_forward_venues_tab = "BTMU FA"
        self.client_at_external_clients_tab = "CLIENT1"
        self.client_at_internal_clients_tab = "HouseFill"
        self.quantity = 1000000
        self.tenor = "Spot"
        self.min_spread = 50
        self.max_spread = 70
        self.position = 100
        self.bid_margin = 10
        self.offer_margin = 20

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        time.sleep(2)
        side_menu.open_client_tier_page()
        # step 1
        client_tiers_main_page = ClientTiersPage(self.web_driver_container)
        client_tiers_main_page.click_on_new()
        time.sleep(2)
        # step 2
        client_tiers_values_sub_wizard = ClientTiersValuesSubWizard(self.web_driver_container)
        client_tiers_values_sub_wizard.set_name(self.name)
        time.sleep(1)
        client_tiers_values_sub_wizard.set_core_spot_price_strategy(self.core_spot_price_strategy)
        # step 3
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
            # step 4
            client_tier_instrument_main_page = ClientTierInstrumentsPage(self.web_driver_container)
            client_tier_instrument_main_page.click_on_new()
            # step 5
            time.sleep(2)
            client_tier_instrument_values_sub_wizard = ClientTierInstrumentValuesSubWizard(self.web_driver_container)
            client_tier_instrument_values_sub_wizard.set_symbol(self.symbol)
            time.sleep(1)
            client_tier_instrument_values_sub_wizard.set_rfq_response_stream_ttl(self.rfq_response_stream_ttl)
            time.sleep(1)
            client_tier_instrument_values_sub_wizard.set_core_spot_price_strategy(self.core_spot_price_strategy)
            time.sleep(1)
            # step 6
            client_tier_instrument_spot_venues_sub_wizard = ClientTiersInstrumentSpotVenuesSubWizard(
                self.web_driver_container)
            client_tier_instrument_spot_venues_sub_wizard.click_on_plus()
            time.sleep(2)
            client_tier_instrument_spot_venues_sub_wizard.set_venue(self.venue_at_spot_venues_tab)
            client_tier_instrument_spot_venues_sub_wizard.click_on_checkmark()
            time.sleep(2)
            client_tier_instrument_forward_venues_sub_wizard = ClientTiersInstrumentForwardVenuesSubWizard(
                self.web_driver_container)
            client_tier_instrument_forward_venues_sub_wizard.click_on_plus()
            time.sleep(2)
            client_tier_instrument_forward_venues_sub_wizard.set_venue(self.venue_at_forward_venues_tab)
            client_tier_instrument_forward_venues_sub_wizard.click_on_checkmark()
            time.sleep(2)
            # step 7
            client_tier_instrument_external_clients_sub_wizard = ClientTiersInstrumentExternalClientsSubWizard(
                self.web_driver_container)
            client_tier_instrument_external_clients_sub_wizard.click_on_plus()
            time.sleep(2)
            client_tier_instrument_external_clients_sub_wizard.set_client(self.client_at_external_clients_tab)
            client_tier_instrument_external_clients_sub_wizard.click_on_checkmark()
            time.sleep(1)
            client_tier_instrument_internal_clients_sub_wizard = ClientTiersInstrumentInternalClientsSubWizard(
                self.web_driver_container)
            client_tier_instrument_internal_clients_sub_wizard.click_on_plus()
            time.sleep(2)
            client_tier_instrument_internal_clients_sub_wizard.set_client(self.client_at_internal_clients_tab)
            client_tier_instrument_internal_clients_sub_wizard.click_on_checkmark()
            time.sleep(1)
            # step 9
            client_tier_instrument_sweepable_quantities_sub_wizard = ClientTiersInstrumentSweepableQuantitiesSubWizard(
                self.web_driver_container)
            client_tier_instrument_sweepable_quantities_sub_wizard.click_on_plus()
            client_tier_instrument_sweepable_quantities_sub_wizard.set_quantity(self.quantity)
            client_tier_instrument_sweepable_quantities_sub_wizard.click_on_published_checkbox()
            client_tier_instrument_sweepable_quantities_sub_wizard.click_on_checkmark()
            time.sleep(1)
            # step 8
            client_tier_instrument_tenors_sub_wizard = ClientTiersInstrumentTenorsSubWizard(self.web_driver_container)
            client_tier_instrument_tenors_sub_wizard.click_on_plus()
            time.sleep(2)
            client_tier_instrument_tenors_sub_wizard.set_tenor(self.tenor)
            time.sleep(2)
            client_tier_instrument_tenors_sub_wizard.set_min_spread(self.min_spread)
            time.sleep(2)
            client_tier_instrument_tenors_sub_wizard.set_max_spread(self.max_spread)
            time.sleep(2)

            # step 10
            client_tier_instrument_position_levels_sub_wizard = ClientTiersInstrumentTenorsSubWizard(
                self.web_driver_container)
            client_tier_instrument_position_levels_sub_wizard.click_on_plus_button_at_position_levels_tab()
            time.sleep(2)
            client_tier_instrument_position_levels_sub_wizard.set_position_at_position_levels_tab(self.position)
            time.sleep(2)
            client_tier_instrument_position_levels_sub_wizard.set_bid_margin_at_position_levels_tab(self.bid_margin)
            time.sleep(2)
            client_tier_instrument_position_levels_sub_wizard.set_offer_margin_at_position_levels_tab(self.offer_margin)
            time.sleep(2)
            client_tier_instrument_position_levels_sub_wizard.click_on_checkmark_at_position_levels_tab()
            time.sleep(2)
            client_tier_instrument_tenors_sub_wizard.click_on_checkmark()
            # step 11
            client_tier_instrument_wizard = ClientTiersWizard(self.web_driver_container)
            time.sleep(2)
            client_tier_instrument_wizard.click_on_save_changes()
            time.sleep(2)
            client_tiers_main_page = ClientTiersPage(self.web_driver_container)
            client_tiers_main_page.set_name(self.name)
            time.sleep(2)
            client_tiers_main_page.click_on_more_actions()
            time.sleep(2)
            client_tier_instrument_main_page.set_symbol(self.symbol)
            time.sleep(2)
            try:
                client_tier_instrument_main_page.click_on_more_actions()
                time.sleep(2)
                client_tier_instrument_main_page.click_on_edit()
                self.verify("Check that instrument saved ", True, True)
            except Exception as e:
                self.verify("Instrument saved INCORRECTLY !!!", True, e.__class__.__name__)
        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            print(traceback.format_exc() + " Search in ->  " + self.__class__.__name__)
