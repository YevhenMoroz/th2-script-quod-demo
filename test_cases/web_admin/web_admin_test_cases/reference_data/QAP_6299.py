import random
import string
import sys
import time
import traceback

from custom import basic_custom_actions
from test_cases.web_admin.web_admin_core.pages.login.login_page import LoginPage
from test_cases.web_admin.web_admin_core.pages.reference_data.listings.listings_page import ListingsPage
from test_cases.web_admin.web_admin_core.pages.reference_data.listings.listings_wizard import ListingsWizard
from test_cases.web_admin.web_admin_core.pages.reference_data.listings.listings_dark_algo_comission_sub_wizard import \
    ListingsDarkAlgoCommissionSubWizard
from test_cases.web_admin.web_admin_core.pages.reference_data.listings.listings_values_sub_wizard import \
    ListingsValuesSubWizard
from test_cases.web_admin.web_admin_core.pages.reference_data.listings.listings_attachment_sub_wizard import \
    ListingsAttachmentSubWizard

from test_cases.web_admin.web_admin_core.pages.root.side_menu import SideMenu
from test_cases.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_6299(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id)
        self.login = "adm03"
        self.password = "adm03"

        self.venue = "ASE"
        self.symbol = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.lookup_symbol = self.symbol + "1LS"
        self.inst_symbol = self.symbol + "2IS"

        self.cost_per_trade = "10.1"
        self.per_unit_comm_amt = "12.2"
        self.comm_basis_point = "13.3"
        self.spread_discount_proportion = "14.4"

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        time.sleep(2)
        side_menu.open_listings_page()
        time.sleep(2)
        page = ListingsPage(self.web_driver_container)
        page.click_on_new()

        listing_wizard_value = ListingsValuesSubWizard(self.web_driver_container)
        listing_wizard_value.set_symbol(self.symbol)
        listing_wizard_value.set_lookup_symbol(self.lookup_symbol)
        listing_wizard_value.set_instr_symbol(self.inst_symbol)

        listing_wizard_attachment = ListingsAttachmentSubWizard(self.web_driver_container)
        listing_wizard_attachment.set_venue(self.venue)

        listing_wizard_dark = ListingsDarkAlgoCommissionSubWizard(self.web_driver_container)
        listing_wizard_dark.set_cost_per_trade(self.cost_per_trade)
        listing_wizard_dark.set_per_unit_comm_amt(self.per_unit_comm_amt)
        listing_wizard_dark.set_comm_basis_point(self.comm_basis_point)
        listing_wizard_dark.set_spread_discount_proportion(self.spread_discount_proportion)
        time.sleep(1)
        listing_wizard_dark.click_on_is_comm_per_unit_checkbox()

        listing_wizard = ListingsWizard(self.web_driver_container)
        listing_wizard.click_on_save_changes()

    def test_context(self):
        try:
            self.precondition()

            page = ListingsPage(self.web_driver_container)
            page.load_client_from_global_filter(self.symbol)
            page.click_on_more_actions()

            time.sleep(2)
            page.click_on_edit()
            time.sleep(2)
            listing_wizard_dark = ListingsDarkAlgoCommissionSubWizard(self.web_driver_container)
            expected_values_after_saved = [self.cost_per_trade, self.per_unit_comm_amt, self.comm_basis_point,
                                           self.spread_discount_proportion]
            actual_result = [listing_wizard_dark.get_cost_per_trade(), listing_wizard_dark.get_per_unit_comm_amt(),
                             listing_wizard_dark.get_comm_basis_point(),
                             listing_wizard_dark.get_spread_discount_proportion()]

            self.verify("Values saved correctly", expected_values_after_saved, actual_result)

            time.sleep(2)
            self.verify("Check-box \"Is Comm Per Unit\" is enable", True,
                        listing_wizard_dark.is_comm_per_unit_checkbox_selected())


        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
