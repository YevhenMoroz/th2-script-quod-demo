import random
import string
import time
import traceback

from custom import basic_custom_actions
from quod_qa.web_admin.web_admin_core.pages.login.login_page import LoginPage
from quod_qa.web_admin.web_admin_core.pages.reference_data.listings.listings_attachment_sub_wizard import \
    ListingsAttachmentSubWizard
from quod_qa.web_admin.web_admin_core.pages.reference_data.listings.listings_page import ListingsPage
from quod_qa.web_admin.web_admin_core.pages.reference_data.listings.listings_values_sub_wizard import \
    ListingsValuesSubWizard
from quod_qa.web_admin.web_admin_core.pages.reference_data.listings.listings_wizard import ListingsWizard
from quod_qa.web_admin.web_admin_core.pages.root.side_menu import SideMenu
from quod_qa.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer
from quod_qa.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_1736(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id)
        self.login = "adm02"
        self.password = "adm02"
        self.symbol = "EUR/USD"
        self.lookup_symbol = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.instr_symbol = "EUR/USD"
        self.venue = "AMSTERDAM"

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
        time.sleep(2)
        wizard = ListingsWizard(self.web_driver_container)
        wizard.click_on_save_changes()
        time.sleep(2)
        page.set_listing_in_global_filter(self.lookup_symbol)
        time.sleep(1)

    def test_context(self):
        try:
            self.precondition()
            page = ListingsPage(self.web_driver_container)
            try:
                page.click_on_load()
                time.sleep(2)
                page.click_on_more_actions()
                time.sleep(2)
                self.verify("Listing created correctly", True, True)
            except Exception as e:
                self.verify("Listing NOT created", True, e.__class__.__name__)

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            print(traceback.format_exc() + " Search in ->  " + self.__class__.__name__)
