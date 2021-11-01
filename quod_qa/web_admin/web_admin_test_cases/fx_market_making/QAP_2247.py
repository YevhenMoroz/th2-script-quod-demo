import random
import string
import time
import traceback

from custom import basic_custom_actions
from quod_qa.web_admin.web_admin_core.pages.fx_market_making.client_tier.client_tier_instrument_tiered_quantities_sub_wizard import \
    ClientTiersInstrumentTieredQuantitiesSubWizard
from quod_qa.web_admin.web_admin_core.pages.fx_market_making.client_tier.client_tier_instrument_wizard import \
    ClientTierInstrumentWizard
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


class QAP_2247(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id)
        self.login = "adm03"
        self.password = "adm03"
        self.name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.core_spot_price_strategy = "Direct"

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
            client_tiers_instrument_wizard = ClientTierInstrumentWizard(self.web_driver_container)
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
            client_tier_instrument_tiered_quantities_sub_wizard = ClientTiersInstrumentTieredQuantitiesSubWizard(
                self.web_driver_container)
            client_tier_instrument_tiered_quantities_sub_wizard.click_on_plus()
            client_tier_instrument_tiered_quantities_sub_wizard.set_quantity(1000000)
            client_tier_instrument_tiered_quantities_sub_wizard.click_on_checkmark()
            client_tier_instrument_tiered_quantities_sub_wizard.click_on_plus()
            client_tier_instrument_tiered_quantities_sub_wizard.set_quantity(5000000)
            client_tier_instrument_tiered_quantities_sub_wizard.click_on_checkmark()
            client_tier_instrument_tiered_quantities_sub_wizard.click_on_plus()
            client_tier_instrument_tiered_quantities_sub_wizard.set_quantity(10000000)
            client_tier_instrument_tiered_quantities_sub_wizard.click_on_checkmark()
            client_tier_instrument_tiered_quantities_sub_wizard.click_on_plus()
            client_tier_instrument_tiered_quantities_sub_wizard.set_quantity(17000000)
            client_tier_instrument_tiered_quantities_sub_wizard.click_on_checkmark()
            client_tier_instrument_tiered_quantities_sub_wizard.click_on_plus()
            client_tier_instrument_tiered_quantities_sub_wizard.set_quantity(17000000)
            client_tier_instrument_tiered_quantities_sub_wizard.click_on_checkmark()
            self.verify("Message displayed This tiered quantity is already exists", True,
                        client_tiers_instrument_wizard.is_such_record_exists_massage_displayed())

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            print(traceback.format_exc() + " Search in ->  " + self.__class__.__name__)
