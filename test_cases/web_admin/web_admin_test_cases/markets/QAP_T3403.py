import sys
import time
import traceback
import random
import string

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.markets.listings.listings_page import ListingsPage
from test_framework.web_admin_core.pages.markets.listings.listings_wizard import ListingsWizard
from test_framework.web_admin_core.pages.markets.listings.listings_feature_sub_wizard import ListingsFeatureSubWizard
from test_framework.web_admin_core.pages.markets.listings.listings_values_sub_wizard import ListingsValuesSubWizard
from test_framework.web_admin_core.pages.markets.listings.listings_attachment_sub_wizard import ListingsAttachmentSubWizard
from test_framework.web_admin_core.pages.markets.listings.listings_currency_sub_wizard import ListingsCurrencySubWizard

from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T3403(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.contract_multiplier_value = random.randint(0, 100)
        self.symbol = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.lookup_symbol = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.insrt_symbol = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.instr_type = self.data_set.get_instr_type("instr_type_1")
        self.security_exchange = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.venue = self.data_set.get_venue_by_name("venue_1")
        self.currency = self.data_set.get_currency_by_name("currency_1")

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        time.sleep(1)
        side_menu = SideMenu(self.web_driver_container)
        side_menu.open_listings_page()
        time.sleep(1)
        listing_page = ListingsPage(self.web_driver_container)
        listing_page.click_on_new()
        time.sleep(1)
        listing_wizard_value_tab = ListingsValuesSubWizard(self.web_driver_container)
        listing_wizard_value_tab.set_symbol(self.symbol)
        listing_wizard_value_tab.set_lookup_symbol(self.lookup_symbol)
        listing_wizard_value_tab.set_instr_symbol(self.insrt_symbol)
        listing_wizard_value_tab.set_instr_type(self.instr_type)
        listing_wizard_value_tab.set_security_exchange(self.security_exchange)
        listing_wizard_attachment_tab = ListingsAttachmentSubWizard(self.web_driver_container)
        listing_wizard_attachment_tab.set_venue(self.venue)
        listing_wizard_currency_tab = ListingsCurrencySubWizard(self.web_driver_container)
        listing_wizard_currency_tab.set_currency(self.currency)
        listing_wizard = ListingsWizard(self.web_driver_container)
        listing_wizard.click_on_save_changes()

    def test_context(self):
        try:
            self.precondition()

            listing_page = ListingsPage(self.web_driver_container)
            listing_page.search_listing_and_click_edit_btn(self.lookup_symbol)
            time.sleep(2)
            listing_wizard_features_tab = ListingsFeatureSubWizard(self.web_driver_container)
            listing_wizard_features_tab.set_contract_multiplier(self.contract_multiplier_value)
            time.sleep(1)
            listing_wizard = ListingsWizard(self.web_driver_container)
            listing_wizard.click_on_save_changes()
            time.sleep(2)
            listing_page.search_listing_and_click_edit_btn(self.lookup_symbol)
            time.sleep(2)
            self.verify("Contract Multiplier field is set correctly",
                        self.contract_multiplier_value, listing_wizard_features_tab.get_contract_multiplier())

            time.sleep(1)
            listing_wizard_features_tab.set_contract_multiplier(" ")
            time.sleep(1)
            listing_wizard.click_on_save_changes()
            time.sleep(2)
            listing_page.search_listing_and_click_edit_btn(self.lookup_symbol)
            time.sleep(2)
            self.verify("Contract Multiplier field is empty",
                        True, listing_wizard_features_tab.is_contract_multiplier_empty())

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
