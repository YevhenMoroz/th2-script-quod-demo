import random
import string
import sys
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
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T3295(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.symbol = self.data_set.get_symbol_by_name("symbol_2")
        self.lookup_symbol = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.instr_symbol = self.data_set.get_instr_symbol("instr_symbol_2")
        self.instr_type = self.data_set.get_instr_type("instr_type_1")
        self.inst_subtype = 'Bull'
        self.cfi = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.security_exchange = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.preferred_security_exchange = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.settle_type = 'BrokenDate'
        self.strike_price = str(random.randint(1, 50))
        self.tenor = 'BrokenDate'
        self.cull_put = 'Put'
        self.industry = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.sub_industry = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.industry_group = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.sector = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
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
            values_tab.set_instr_sub_type(self.inst_subtype)
            values_tab.set_cfi(self.cfi)
            values_tab.set_security_exchange(self.security_exchange)
            values_tab.set_preferred_security_exchange(self.preferred_security_exchange)
            values_tab.set_settl_type(self.settle_type)
            values_tab.set_strike_price(self.strike_price)
            values_tab.set_tenor(self.tenor)
            values_tab.set_call_put(self.cull_put)
            values_tab.set_industry(self.industry)
            values_tab.set_sub_industry(self.sub_industry)
            values_tab.set_industry_group(self.industry_group)
            values_tab.set_sector(self.sector)
            attachment_tab = ListingsAttachmentSubWizard(self.web_driver_container)
            attachment_tab.set_venue(self.venue)
            currency_tab = ListingsCurrencySubWizard(self.web_driver_container)
            currency_tab.set_currency(self.currency)
            wizard = ListingsWizard(self.web_driver_container)
            wizard.click_on_save_changes()
            page.load_listing_from_global_filter(self.lookup_symbol)
            page.click_on_more_actions()
            page.click_on_clone()

            expected_result = [self.symbol, self.lookup_symbol, self.instr_type, self.inst_subtype, self.cfi,
                               self.security_exchange, self.preferred_security_exchange, self.settle_type,
                               self.strike_price, self.tenor, self.cull_put, self.industry, self.sub_industry,
                               self.industry_group, self.sector]
            actual_result = [values_tab.get_symbol(), values_tab.get_lookup_symbol(), values_tab.get_instr_type(),
                             values_tab.get_instr_sub_type(), values_tab.get_cfi(), values_tab.get_security_exchange(),
                             values_tab.get_preferred_security_exchange(), values_tab.get_settl_type(),
                             values_tab.get_strike_price(), values_tab.get_tenor(), values_tab.get_call_put(),
                             values_tab.get_industry(), values_tab.get_sub_industry(), values_tab.get_industry_group(),
                             values_tab.get_sector()]
            self.verify("Not required fields displayed after cloning", expected_result, actual_result)

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
