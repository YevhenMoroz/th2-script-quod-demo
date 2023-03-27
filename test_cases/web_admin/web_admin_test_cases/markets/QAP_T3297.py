import random
import string
import sys
import time
import traceback

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.markets.listings.listings_attachment_sub_wizard import \
    ListingsAttachmentSubWizard
from test_framework.web_admin_core.pages.markets.listings.listings_currency_sub_wizard import \
    ListingsCurrencySubWizard
from test_framework.web_admin_core.pages.markets.listings.listings_translation_sub_wizard import \
    TranslationTab
from test_framework.web_admin_core.pages.markets.listings.listings_page import ListingsPage
from test_framework.web_admin_core.pages.markets.listings.listings_values_sub_wizard import \
    ListingsValuesSubWizard
from test_framework.web_admin_core.pages.markets.listings.listings_wizard import ListingsWizard
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T3297(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.symbol = self.data_set.get_symbol_by_name("symbol_2")
        self.lookup_symbol = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.instr_symbol = self.data_set.get_instr_symbol("instr_symbol_2")
        self.instr_type = self.data_set.get_instr_type("instr_type_1")
        self.security_exchange = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.listing_languages = ['Afar', 'Ukrainian-Ukraine', 'English-US']
        self.listing_description = [''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6)) for _ in
                                    range(3)]
        self.instrument_languages = ['Arabic-Libya.', 'Bihari', 'Spanish-Panama']
        self.instrument_description = [''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6)) for _ in
                                       range(3)]
        self.venue = self.data_set.get_venue_by_name("venue_4")
        self.currency = self.data_set.get_currency_by_name("currency_2")

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        side_menu.open_listings_page()

    def test_context(self):
        try:
            self.precondition()

            page = ListingsPage(self.web_driver_container)
            page.click_on_new()
            values_tab = ListingsValuesSubWizard(self.web_driver_container)
            values_tab.set_symbol(self.symbol)
            values_tab.set_lookup_symbol(self.lookup_symbol)
            values_tab.set_instr_symbol(self.instr_symbol)
            values_tab.set_instr_type(self.instr_type)
            values_tab.set_security_exchange(self.security_exchange)

            translation_tab_listing = TranslationTab.ListingTable(self.web_driver_container)
            for i in range(len(self.listing_languages)):
                translation_tab_listing.click_on_plus()
                translation_tab_listing.set_language(self.listing_languages[i])
                translation_tab_listing.set_description(self.listing_description[i])
                translation_tab_listing.click_on_checkmark()

            translation_tab_instrument = TranslationTab.InstrumentTable(self.web_driver_container)
            for i in range(len(self.instrument_languages)):
                translation_tab_instrument.click_on_plus()
                translation_tab_instrument.set_language(self.instrument_languages[i])
                translation_tab_instrument.set_description(self.instrument_description[i])
                translation_tab_instrument.click_on_checkmark()

            attachment_tab = ListingsAttachmentSubWizard(self.web_driver_container)
            attachment_tab.set_venue(self.venue)
            currency_tab = ListingsCurrencySubWizard(self.web_driver_container)
            currency_tab.set_currency(self.currency)
            wizard = ListingsWizard(self.web_driver_container)
            wizard.click_on_save_changes()
            page.load_listing_from_global_filter(self.lookup_symbol)
            page.click_on_more_actions()
            page.click_on_edit()

            expected_result = [a+": "+b for a, b in zip(self.listing_languages, self.listing_description)]
            saved_listing_languages = []
            saved_listing_description = []
            for i in range(len(self.listing_languages)):
                translation_tab_listing.set_language_filter(self.listing_languages[i])
                time.sleep(0.5)
                translation_tab_listing.click_on_edit()
                saved_listing_languages.append(translation_tab_listing.get_language())
                saved_listing_description.append(translation_tab_listing.get_description())
                translation_tab_listing.click_on_close()

            actual_result = [a+": "+b for a, b in zip(saved_listing_languages, saved_listing_description)]
            self.verify("Listing languages and description save correct", expected_result, actual_result)

            expected_result = [a + ": " + b for a, b in zip(self.instrument_languages, self.instrument_description)]
            saved_instrument_languages = []
            saved_instrument_description = []
            for i in range(len(self.instrument_languages)):
                translation_tab_instrument.set_language_filter(self.instrument_languages[i])
                time.sleep(0.5)
                translation_tab_instrument.click_on_edit()
                saved_instrument_languages.append(translation_tab_instrument.get_language())
                saved_instrument_description.append(translation_tab_instrument.get_description())
                translation_tab_instrument.click_on_close()

            actual_result = [a + ": " + b for a, b in zip(saved_instrument_languages, saved_instrument_description)]
            self.verify("Instrument languages and description save correct", expected_result, actual_result)

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
