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
from test_framework.web_admin_core.pages.markets.listings.listings_status_sub_wizard \
    import ListingsStatusSubWizard
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T3525(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")

        self.symbol = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.new_symbol = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.lookup_symbol = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.instr_symbol = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.instr_type = self.data_set.get_instr_type("instr_type_1")

        self.venue = self.data_set.get_venue_by_name("venue_3")
        self.currency = self.data_set.get_currency_by_name("currency_1")

        self.trading_phase = '200'
        self.trading_status = 'Trading'
        self.trading_session = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.external_trading_status = 'Trading'

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        side_menu.open_listings_page()

        main_page = ListingsPage(self.web_driver_container)
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
        wizard = ListingsWizard(self.web_driver_container)
        wizard.click_on_save_changes()

    def test_context(self):

        try:
            self.precondition()

            main_page = ListingsPage(self.web_driver_container)
            main_page.load_listing_from_global_filter(self.lookup_symbol)
            time.sleep(1)
            main_page.click_on_more_actions()
            main_page.click_on_edit()

            status_tab = ListingsStatusSubWizard(self.web_driver_container)
            status_tab.set_trading_phase(self.trading_phase)
            status_tab.set_trading_status(self.trading_status)
            status_tab.set_trading_session(self.trading_session)
            status_tab.set_external_trading_status(self.external_trading_status)
            wizard = ListingsWizard(self.web_driver_container)
            wizard.click_on_save_changes()

            main_page.load_listing_from_global_filter(self.lookup_symbol)
            time.sleep(1)
            main_page.click_on_more_actions()
            main_page.click_on_edit()

            expected_result = [self.trading_phase, self.trading_status, self.trading_session,
                               self.external_trading_status]
            actual_result = [status_tab.get_trading_phase(), status_tab.get_trading_status(),
                             status_tab.get_trading_session(), status_tab.get_external_trading_status()]
            self.verify("Status tab displayed saved data after save", expected_result, actual_result)

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
