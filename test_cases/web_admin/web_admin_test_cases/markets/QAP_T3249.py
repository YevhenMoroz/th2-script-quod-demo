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
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T3249(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")

        self.lookup_symbol = 'a'

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        side_menu.open_listings_page()

    def test_context(self):

        try:
            self.precondition()

            main_page = ListingsPage(self.web_driver_container)
            main_page.load_listing_from_global_filter(self.lookup_symbol)
            time.sleep(1)
            main_page.click_on_more_actions()
            main_page.click_on_edit()
            time.sleep(1)

            values_tab = ListingsValuesSubWizard(self.web_driver_container)
            attachment_tab = ListingsAttachmentSubWizard(self.web_driver_container)
            currency_tab = ListingsCurrencySubWizard(self.web_driver_container)

            fields = ['InstrSymbol', 'InstrType', 'SecurityExchange', 'Venue', 'Currency']
            expected_result = [False for _ in range(5)]
            actual_result = [values_tab.is_instr_symbol_field_enabled(), values_tab.is_instr_type_field_enabled(),
                             values_tab.is_security_exchange_field_enabled(), attachment_tab.is_venue_field_enabled(),
                             currency_tab.is_currency_field_enabled()]

            self.verify("Required fields disable", [a+": "+str(b) for a, b in zip(fields, expected_result)],
                        [a+": "+str(b) for a, b in zip(fields, actual_result)])

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
