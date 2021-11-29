import sys
import time
import traceback

from custom import basic_custom_actions
from quod_qa.web_admin.web_admin_core.pages.market_making.client_tier.client_tier_instrument_tenors_sub_wizard import \
    ClientTiersInstrumentTenorsSubWizard
from quod_qa.web_admin.web_admin_core.pages.market_making.client_tier.client_tier_instrument_wizard import \
    ClientTierInstrumentWizard
from quod_qa.web_admin.web_admin_core.pages.market_making.client_tier.client_tier_instruments_page import \
    ClientTierInstrumentsPage
from quod_qa.web_admin.web_admin_core.pages.market_making.client_tier.client_tiers_page import ClientTiersPage
from quod_qa.web_admin.web_admin_core.pages.login.login_page import LoginPage
from quod_qa.web_admin.web_admin_core.pages.root.side_menu import SideMenu
from quod_qa.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer
from quod_qa.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_2557(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id)
        self.login = "adm03"
        self.password = "adm03"
        self.name = "Silver"
        self.symbol = "EUR/USD"
        self.tenor_filter = "Spot"
        self.position = "1"
        self.bid_margin = "2"
        self.offer_margin = "2"

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        time.sleep(2)
        side_menu.open_client_tier_page()
        client_tiers_main_page = ClientTiersPage(self.web_driver_container)
        client_tiers_main_page.set_name(self.name)
        time.sleep(2)
        client_tiers_main_page.click_on_more_actions()
        client_tiers_instruments_page = ClientTierInstrumentsPage(self.web_driver_container)
        client_tiers_instruments_page.set_symbol(self.symbol)
        time.sleep(2)
        client_tiers_instruments_page.click_on_more_actions()
        time.sleep(2)
        client_tiers_instruments_page.click_on_edit()
        time.sleep(2)
        tenor_sub_wizard = ClientTiersInstrumentTenorsSubWizard(self.web_driver_container)
        # tenor_sub_wizard.set_tenor_filter(self.tenor_filter)
        time.sleep(2)
        tenor_sub_wizard.click_on_edit()
        time.sleep(2)

    def test_context(self):

        try:
            self.precondition()
            client_tiers_main_page = ClientTiersPage(self.web_driver_container)
            client_tiers_instrument_wizard = ClientTierInstrumentWizard(self.web_driver_container)
            tenor_sub_wizard = ClientTiersInstrumentTenorsSubWizard(self.web_driver_container)

            # if tenor_sub_wizard.get_automated_margin_strategies_enabled():
            #    self.verify("Automated margin strategies enabled", True, True)

            # else:
            tenor_sub_wizard.click_on_automated_margin_strategies_enabled_checkbox()
              # self.verify("Automated margin strategies enabled", True, True)

            # if tenor_sub_wizard.get_position_based_margins():
            #     self.verify("Position based margins enabled", True, True)

            # else:
            tenor_sub_wizard.click_on_position_based_margins()
             # self.verify("Position based margins enabled", True, True)

            tenor_sub_wizard.click_on_plus_button_at_position_levels_tab()
            tenor_sub_wizard.set_position_at_position_levels_tab(self.position)
            tenor_sub_wizard.set_bid_margin_at_position_levels_tab(self.bid_margin)
            tenor_sub_wizard.set_offer_margin_at_base_margins_tab(self.offer_margin)
            tenor_sub_wizard.click_on_checkmark_at_position_levels_tab()
            time.sleep(1)
            tenor_sub_wizard.click_on_checkmark()

            expected_pdf_result = [self.symbol,
                                   self.tenor_filter,
                                   self.position,
                                   self.bid_margin,
                                   self.offer_margin]

            self.verify("Is pdf contains correctly values", True,
                        client_tiers_instrument_wizard.click_download_pdf_entity_button_and_check_pdf(
                            expected_pdf_result))
            time.sleep(2)
            try:
                client_tiers_instrument_wizard.click_on_save_changes()
                self.verify("Entity saved correctly", True, True)

            except Exception as e:
                self.verify("Entity Not saved !!!", True, e.__class__.__name__)
            client_tiers_main_page.set_name(self.name)
            time.sleep(2)
            client_tiers_main_page.click_on_more_actions()
            client_tiers_instruments_page = ClientTierInstrumentsPage(self.web_driver_container)
            client_tiers_instruments_page.set_symbol(self.symbol)
            time.sleep(2)
            client_tiers_instruments_page.click_on_more_actions()
            time.sleep(3)
            client_tiers_instruments_page.click_on_edit()
            time.sleep(3)
            tenor_sub_wizard.click_on_edit()
            time.sleep(2)
            tenor_sub_wizard.click_on_automated_margin_strategies_enabled_checkbox()
            tenor_sub_wizard.click_on_position_based_margins()
            client_tiers_instrument_wizard.click_on_save_changes()

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
