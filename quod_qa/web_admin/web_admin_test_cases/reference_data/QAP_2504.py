import random
import string
import sys
import time
import traceback

from custom import basic_custom_actions
from quod_qa.web_admin.web_admin_core.pages.login.login_page import LoginPage
from quod_qa.web_admin.web_admin_core.pages.reference_data.listings.listings_attachment_sub_wizard import \
    ListingsAttachmentSubWizard
from quod_qa.web_admin.web_admin_core.pages.reference_data.listings.listings_currency_sub_wizard import \
    ListingsCurrencySubWizard
from quod_qa.web_admin.web_admin_core.pages.reference_data.listings.listings_page import ListingsPage
from quod_qa.web_admin.web_admin_core.pages.reference_data.listings.listings_values_sub_wizard import \
    ListingsValuesSubWizard
from quod_qa.web_admin.web_admin_core.pages.reference_data.listings.listings_wizard import ListingsWizard
from quod_qa.web_admin.web_admin_core.pages.root.side_menu import SideMenu
from quod_qa.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer
from quod_qa.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_2504(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id)
        self.login = "adm02"
        self.password = "adm02"
        self.symbol = "EUR/USD"
        self.lookup_symbol = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.instr_symbol = "EUR/USD"
        self.venue = "AMSTERDAM"
        self.preferred_venue = "BATS"
        self.new_preferred_venue = "ADX"
        self.currency = "AED"

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        time.sleep(2)
        side_menu.open_listings_page()
        time.sleep(2)
        page = ListingsPage(self.web_driver_container)
        page.click_on_new()
        time.sleep(2)
        values_sub_wizard = ListingsValuesSubWizard(self.web_driver_container)
        values_sub_wizard.set_symbol(self.symbol)
        values_sub_wizard.set_lookup_symbol(self.lookup_symbol)
        values_sub_wizard.set_instr_symbol(self.instr_symbol)
        attachment_sub_wizard = ListingsAttachmentSubWizard(self.web_driver_container)
        attachment_sub_wizard.set_venue(self.venue)
        attachment_sub_wizard.set_preferred_venue(self.preferred_venue)
        currency_sub_wizard = ListingsCurrencySubWizard(self.web_driver_container)
        currency_sub_wizard.set_currency(self.currency)
        time.sleep(2)
        wizard = ListingsWizard(self.web_driver_container)
        wizard.click_on_save_changes()
        time.sleep(2)
        page.set_listing_in_global_filter(self.lookup_symbol)
        time.sleep(1)
        page.click_on_load()
        time.sleep(2)
        page.click_on_more_actions()
        time.sleep(2)

    def test_context(self):

        try:
            self.precondition()
            page = ListingsPage(self.web_driver_container)
            wizard = ListingsWizard(self.web_driver_container)
            attachment_sub_wizard = ListingsAttachmentSubWizard(self.web_driver_container)
            expected_pdf_values_after_saved = [self.lookup_symbol,
                                               self.instr_symbol,
                                               self.venue,
                                               self.preferred_venue]

            self.verify("Listing saved with correctly values", True,
                        page.click_download_pdf_entity_button_and_check_pdf(expected_pdf_values_after_saved))
            #########
            time.sleep(3)
            page.click_on_more_actions()
            time.sleep(2)
            page.click_on_edit()
            time.sleep(2)
            attachment_sub_wizard.set_preferred_venue(self.new_preferred_venue)
            time.sleep(2)
            wizard.click_on_save_changes()
            time.sleep(2)
            page.set_listing_in_global_filter(self.lookup_symbol)
            time.sleep(1)
            page.click_on_load()
            time.sleep(2)
            page.click_on_more_actions()
            time.sleep(2)
            expected_pdf_values_after_edited = [self.lookup_symbol,
                                                self.instr_symbol,
                                                self.venue,
                                                self.new_preferred_venue]
            self.verify("Listing edited with correctly values", True,
                        page.click_download_pdf_entity_button_and_check_pdf(expected_pdf_values_after_edited))


        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
