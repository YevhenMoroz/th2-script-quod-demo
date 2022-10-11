import sys
import time
import traceback
import random
import string

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.market_making.client_tier.client_tier_instrument_external_clients_sub_wizard\
    import ClientTiersInstrumentExternalClientsSubWizard
from test_framework.web_admin_core.pages.market_making.client_tier.client_tier_instrument_forward_venues_sub_wizard\
    import ClientTiersInstrumentForwardVenuesSubWizard
from test_framework.web_admin_core.pages.market_making.client_tier.client_tier_instrument_internal_clients_sub_wizard\
    import ClientTiersInstrumentInternalClientsSubWizard
from test_framework.web_admin_core.pages.market_making.client_tier.client_tier_instrument_spot_venues_sub_wizard\
    import ClientTiersInstrumentSpotVenuesSubWizard
from test_framework.web_admin_core.pages.market_making.client_tier.client_tier_instrument_sweepable_quantities_sub_wizard\
    import ClientTiersInstrumentSweepableQuantitiesSubWizard
from test_framework.web_admin_core.pages.market_making.client_tier.client_tier_instrument_tiered_quantities_sub_wizard\
    import ClientTiersInstrumentTieredQuantitiesSubWizard
from test_framework.web_admin_core.pages.market_making.client_tier.client_tier_instrument_tenors_sub_wizard\
    import ClientTiersInstrumentTenorsSubWizard
from test_framework.web_admin_core.pages.market_making.client_tier.client_tier_instrument_values_sub_wizard\
    import ClientTierInstrumentValuesSubWizard
from test_framework.web_admin_core.pages.market_making.client_tier.client_tier_instruments_page\
    import ClientTierInstrumentsPage
from test_framework.web_admin_core.pages.market_making.client_tier.client_tiers_page import ClientTiersPage
from test_framework.web_admin_core.pages.market_making.client_tier.client_tiers_values_sub_wizard import \
    ClientTiersValuesSubWizard
from test_framework.web_admin_core.pages.market_making.client_tier.client_tiers_wizard import ClientTiersWizard
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T3989(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")

        self.name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.core_spot_price_strategy = "Direct"
        self.symbol = self.data_set.get_instr_symbol("instr_symbol_3")
        self.venue_at_spot_venues_tab = self.data_set.get_venue_by_name("venue_6")
        self.venue_at_forward_venues_tab = self.data_set.get_venue_by_name("venue_5")
        self.client_at_external_clients_tab = self.data_set.get_client("client_1")
        self.client_at_internal_clients_tab = "HouseFill"
        self.sweepable_quantity = "1000000"
        self.tired_quantity = "9999"
        self.tenor = self.data_set.get_tenor_by_name("tenor_1")

        self.tod_end_time = "01:00:00"

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        time.sleep(2)
        side_menu = SideMenu(self.web_driver_container)
        side_menu.open_client_tier_page()
        client_tiers_frame = ClientTiersPage(self.web_driver_container)

        client_tiers_frame.click_on_new()
        client_tiers_values_tab = ClientTiersValuesSubWizard(self.web_driver_container)
        client_tiers_values_tab.set_name(self.name)
        client_tiers_values_tab.set_core_spot_price_strategy(self.core_spot_price_strategy)
        client_tiers_values_tab.set_tod_end_time(self.tod_end_time)
        client_tiers_wizard = ClientTiersWizard(self.web_driver_container)
        client_tiers_wizard.click_on_save_changes()

    def post_conditions(self):
        client_tiers_frame = ClientTiersPage(self.web_driver_container)
        client_tiers_frame.set_name(self.name)
        time.sleep(1)
        client_tiers_frame.select_client_tier_by_name(self.name)
        client_tiers_frame.click_on_more_actions()
        client_tiers_frame.click_on_delete_and_confirmation(True)

    def test_context(self):
        try:
            self.precondition()

            client_tiers_frame = ClientTiersPage(self.web_driver_container)
            client_tiers_frame.set_name(self.name)
            time.sleep(1)
            client_tiers_frame.select_client_tier_by_name(self.name)

            instrument_frame = ClientTierInstrumentsPage(self.web_driver_container)
            instrument_frame.click_on_new()
            instrument_values_tab = ClientTierInstrumentValuesSubWizard(self.web_driver_container)
            instrument_values_tab.set_symbol(self.symbol)
            instrument_values_tab.set_tod_end_time(self.tod_end_time)

            instrument_spot_venues_tab = ClientTiersInstrumentSpotVenuesSubWizard(self.web_driver_container)
            instrument_spot_venues_tab.click_on_plus()
            instrument_spot_venues_tab.set_venue(self.venue_at_spot_venues_tab)
            instrument_spot_venues_tab.click_on_checkmark()

            instrument_forward_venues_tab = ClientTiersInstrumentForwardVenuesSubWizard(self.web_driver_container)
            instrument_forward_venues_tab.click_on_plus()
            instrument_forward_venues_tab.set_venue(self.venue_at_forward_venues_tab)
            instrument_forward_venues_tab.click_on_checkmark()

            instrument_external_clients_tab = ClientTiersInstrumentExternalClientsSubWizard(self.web_driver_container)
            instrument_external_clients_tab.click_on_plus()
            instrument_external_clients_tab.set_client(self.client_at_external_clients_tab)
            instrument_external_clients_tab.click_on_checkmark()

            instrument_internal_clients_tab = ClientTiersInstrumentInternalClientsSubWizard(self.web_driver_container)
            instrument_internal_clients_tab.click_on_plus()
            instrument_internal_clients_tab.set_client(self.client_at_internal_clients_tab)
            instrument_internal_clients_tab.click_on_checkmark()

            instrument_sweepable_quantities_tab = ClientTiersInstrumentSweepableQuantitiesSubWizard(self.web_driver_container)
            instrument_sweepable_quantities_tab.click_on_plus()
            instrument_sweepable_quantities_tab.set_quantity(self.sweepable_quantity)
            instrument_sweepable_quantities_tab.click_on_checkmark()

            instrument_tiered_quantity = ClientTiersInstrumentTieredQuantitiesSubWizard(self.web_driver_container)
            instrument_tiered_quantity.click_on_plus()
            instrument_tiered_quantity.set_quantity(self.tired_quantity)
            instrument_tiered_quantity.click_on_checkmark()

            instrument_tenors_sub_wizard = ClientTiersInstrumentTenorsSubWizard(self.web_driver_container)
            instrument_tenors_sub_wizard.click_on_plus()
            instrument_tenors_sub_wizard.set_tenor(self.tenor)
            instrument_tenors_sub_wizard.click_on_checkmark()

            instrument_wizard = ClientTiersWizard(self.web_driver_container)
            instrument_wizard.click_on_save_changes()

            client_tiers_frame.set_name(self.name)
            time.sleep(1)
            client_tiers_frame.select_client_tier_by_name(self.name)
            instrument_frame.set_symbol(self.symbol)
            time.sleep(1)
            instrument_frame.click_on_more_actions()
            instrument_frame.click_on_edit()

            actual_result = []
            instrument_spot_venues_tab.click_on_edit()
            actual_result.append(instrument_spot_venues_tab.get_venue())
            instrument_forward_venues_tab.click_on_edit()
            actual_result.append(instrument_forward_venues_tab.get_venue())
            instrument_external_clients_tab.click_on_edit()
            actual_result.append(instrument_external_clients_tab.get_client())
            instrument_internal_clients_tab.click_on_edit()
            actual_result.append(instrument_internal_clients_tab.get_client())
            instrument_sweepable_quantities_tab.click_on_edit()
            actual_result.append(instrument_sweepable_quantities_tab.get_quantity())
            instrument_tiered_quantity.click_on_edit()
            actual_result.append(instrument_tiered_quantity.get_quantity())
            instrument_tenors_sub_wizard.click_on_edit()
            actual_result.append(instrument_tenors_sub_wizard.get_tenor())

            expected_result = [self.venue_at_spot_venues_tab, self.venue_at_forward_venues_tab,
                               self.client_at_external_clients_tab, self.client_at_internal_clients_tab,
                               self.sweepable_quantity, self.tired_quantity, self.tenor]

            self.verify("New Client Tiers Instrument contains all saved data", expected_result, actual_result)

            instrument_wizard.click_on_save_changes()

            self.post_conditions()

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
