import random
import string
import sys
import time
import traceback

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.markets.listings.listings_page import ListingsPage
from test_framework.web_admin_core.pages.markets.listings.listings_wizard import ListingsWizard
from test_framework.web_admin_core.pages.markets.listings.listings_values_sub_wizard \
    import ListingsValuesSubWizard
from test_framework.web_admin_core.pages.markets.listings.listings_attachment_sub_wizard \
    import ListingsAttachmentSubWizard
from test_framework.web_admin_core.pages.markets.listings.listings_currency_sub_wizard \
    import ListingsCurrencySubWizard
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T3550(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.listing = 'DUMMY'
        self.symbol = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.lookup_symbol = 'DUMMY'
        self.instr_symbol = 'DUMMYTEST'
        self.instr_type = 'Bond'
        self.security_exchange = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.venue = self.data_set.get_venue_by_name('venue_1')
        self.currency = self.data_set.get_currency_by_name('currency_1')

        self.new_symbol = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.new_lookup_symbol = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.new_instr_symbol = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.new_security_exchange = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        time.sleep(2)
        side_menu = SideMenu(self.web_driver_container)
        side_menu.open_listings_page()
        main_page = ListingsPage(self.web_driver_container)
        main_page.load_listing_from_global_filter(self.listing)

        if not main_page.is_searched_listing_found(self.instr_symbol):
            main_page.click_on_new()
            time.sleep(2)
            values_tab = ListingsValuesSubWizard(self.web_driver_container)
            values_tab.set_symbol(self.symbol)
            values_tab.set_lookup_symbol(self.lookup_symbol)
            values_tab.set_instr_symbol(self.instr_symbol)
            values_tab.set_instr_type(self.instr_type)
            values_tab.set_security_exchange(self.security_exchange)
            values_tab.click_on_dummy()
            attachment_tab = ListingsAttachmentSubWizard(self.web_driver_container)
            attachment_tab.set_venue(self.venue)
            currency_tab = ListingsCurrencySubWizard(self.web_driver_container)
            currency_tab.set_currency(self.currency)
            wizard = ListingsWizard(self.web_driver_container)
            wizard.click_on_save_changes()
            time.sleep(2)
            main_page.load_listing_from_global_filter(self.listing)
            time.sleep(2)

        main_page.click_on_more_actions()
        time.sleep(1)
        main_page.click_on_clone()
        time.sleep(2)

    def test_context(self):
        try:
            self.precondition()

            values_tab = ListingsValuesSubWizard(self.web_driver_container)
            values_tab.set_symbol(self.new_symbol)
            values_tab.set_lookup_symbol(self.new_lookup_symbol)
            values_tab.set_instr_symbol(self.new_instr_symbol)
            values_tab.set_instr_type(self.instr_type)
            values_tab.set_security_exchange(self.new_security_exchange)
            attachment_tab = ListingsAttachmentSubWizard(self.web_driver_container)
            attachment_tab.set_venue(self.venue)
            currency_tab = ListingsCurrencySubWizard(self.web_driver_container)
            currency_tab.set_currency(self.currency)
            wizard = ListingsWizard(self.web_driver_container)
            wizard.click_on_save_changes()
            time.sleep(2)

            self.verify("Second DUMMY client is not saving", True,
                        wizard.is_request_failed_message_displayed())

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
