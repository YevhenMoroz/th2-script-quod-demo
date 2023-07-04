import random
import string
import time

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

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None,
                 db_manager=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.db_manager = db_manager
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

        self.new_linting = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.new_symbol = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.new_lookup_symbol = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.new_instr_symbol = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.new_security_exchange = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        main_page = ListingsPage(self.web_driver_container)
        side_menu = SideMenu(self.web_driver_container)
        attachment_tab = ListingsAttachmentSubWizard(self.web_driver_container)
        currency_tab = ListingsCurrencySubWizard(self.web_driver_container)
        values_tab = ListingsValuesSubWizard(self.web_driver_container)
        wizard = ListingsWizard(self.web_driver_container)

        login_page.login_to_web_admin(self.login, self.password)
        side_menu.open_listings_page()

        self.db_manager.my_db.execute("SELECT INSTRSYMBOL FROM INSTRUMENT WHERE DUMMY = 'Y'")
        dummy_listing = [_[0] for _ in self.db_manager.my_db]
        if len(dummy_listing) == 0:
            main_page.click_on_new()
            values_tab.set_symbol(self.symbol)
            values_tab.set_lookup_symbol(self.lookup_symbol)
            values_tab.set_instr_symbol(self.instr_symbol)
            values_tab.set_instr_type(self.instr_type)
            values_tab.set_security_exchange(self.security_exchange)
            values_tab.click_on_dummy()
            attachment_tab.set_venue(self.venue)
            currency_tab.set_currency(self.currency)
            wizard.click_on_save_changes()
            time.sleep(1)

    def test_context(self):
        values_tab = ListingsValuesSubWizard(self.web_driver_container)
        attachment_tab = ListingsAttachmentSubWizard(self.web_driver_container)
        currency_tab = ListingsCurrencySubWizard(self.web_driver_container)
        main_page = ListingsPage(self.web_driver_container)
        wizard = ListingsWizard(self.web_driver_container)

        self.precondition()

        main_page.click_on_new()
        values_tab.set_symbol(self.new_symbol)
        values_tab.set_lookup_symbol(self.new_lookup_symbol)
        values_tab.set_instr_symbol(self.new_instr_symbol)
        values_tab.set_instr_type(self.instr_type)
        values_tab.set_security_exchange(self.new_security_exchange)
        values_tab.click_on_dummy()
        attachment_tab.set_venue(self.venue)
        currency_tab.set_currency(self.currency)
        wizard.click_on_save_changes()
        time.sleep(2)

        self.verify("Second DUMMY Listing is not saving", True, wizard.is_request_failed_message_displayed())
