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
from test_framework.web_admin_core.pages.markets.listings.listings_page import ListingsPage
from test_framework.web_admin_core.pages.markets.listings.listings_values_sub_wizard import \
    ListingsValuesSubWizard
from test_framework.web_admin_core.pages.markets.listings.listings_wizard import ListingsWizard
from test_framework.web_admin_core.pages.markets.listings.listings_market_identifies_sub_wizard \
    import ListingsMarketIdentifiersSubWizard
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T3247(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")

        self.symbol = 'QAP_T3247'
        self.new_symbol = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.lookup_symbol = 'QAP_T3247'
        self.instr_symbol = 'ASC'
        self.instr_type = self.data_set.get_instr_type("instr_type_1")

        self.venue = self.data_set.get_venue_by_name("venue_3")
        self.currency = self.data_set.get_currency_by_name("currency_1")

        self.security_id = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.security_id_source = 'Belgian'

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        time.sleep(2)
        side_menu = SideMenu(self.web_driver_container)
        side_menu.open_listings_page()
        main_page = ListingsPage(self.web_driver_container)
        main_page.load_listing_from_global_filter(self.lookup_symbol)
        if not main_page.is_searched_listing_found(self.lookup_symbol):
            main_page.click_on_new()
            values_tab = ListingsValuesSubWizard(self.web_driver_container)
            values_tab.set_symbol(self.symbol)
            values_tab.set_lookup_symbol(self.lookup_symbol)
            values_tab.set_instr_symbol(self.instr_symbol)
            values_tab.set_instr_type(self.instr_type)

            attachment_tab = ListingsAttachmentSubWizard(self.web_driver_container)
            attachment_tab.set_venue(self.venue)

            currency_tab = ListingsCurrencySubWizard(self.web_driver_container)
            currency_tab.set_currency(self.currency)

            market_identifiers_tab = ListingsMarketIdentifiersSubWizard(self.web_driver_container)
            market_identifiers_tab.set_security_id(self.security_id)
            market_identifiers_tab.set_security_id_source(self.security_id_source)

            wizard = ListingsWizard(self.web_driver_container)
            wizard.click_on_save_changes()
            main_page.load_listing_from_global_filter(self.lookup_symbol)

        main_page.click_on_more_actions()
        main_page.click_on_edit()

    def test_context(self):

        try:
            self.precondition()

            market_identifiers_tab = ListingsMarketIdentifiersSubWizard(self.web_driver_container)
            market_identifiers_tab.set_security_id("")

            wizard = ListingsWizard(self.web_driver_container)
            wizard.click_on_save_changes()

            self.verify("Listing is not save w/o Security ID", True, wizard.is_error_message_displayed())

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
