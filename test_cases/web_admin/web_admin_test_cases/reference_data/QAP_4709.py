import random
import string
import time
import traceback

from custom import basic_custom_actions
from test_cases.web_admin.web_admin_core.pages.login.login_page import LoginPage
from test_cases.web_admin.web_admin_core.pages.reference_data.listings.listings_page import ListingsPage
from test_cases.web_admin.web_admin_core.pages.reference_data.listings.listings_values_sub_wizard import \
    ListingsValuesSubWizard
from test_cases.web_admin.web_admin_core.pages.root.side_menu import SideMenu
from test_cases.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_4709(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id)
        self.login = "adm02"
        self.password = "adm02"
        self.name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        time.sleep(2)
        side_menu.open_listings_page()
        time.sleep(2)
        listing_page = ListingsPage(self.web_driver_container)
        listing_page.click_on_new()
        time.sleep(2)
        listing_values_sub_wizard = ListingsValuesSubWizard(self.web_driver_container)
        listing_values_sub_wizard.set_instr_type("FXNDF")
        time.sleep(1)
        self.verify("Is tenor required for FXNDF", True, listing_values_sub_wizard.is_tenor_field_required())
        time.sleep(1)
        listing_values_sub_wizard.set_instr_type("FXForward")
        self.verify("Is tenor required for FXForward", True, listing_values_sub_wizard.is_tenor_field_required())
        time.sleep(1)
        listing_values_sub_wizard.set_instr_type("DepositLoanLeg")
        self.verify("Is tenor required for DepositLoanLeg", True, listing_values_sub_wizard.is_tenor_field_required())
        time.sleep(1)
        listing_values_sub_wizard.set_instr_type("Option")
        self.verify("Is maturity month year required for Option", True,
                    listing_values_sub_wizard.is_maturity_month_year_field_required())
        time.sleep(1)
        self.verify("Is strike price required required for Option", True,
                    listing_values_sub_wizard.is_strike_price_field_required())
        self.verify("Is call put  required for Option", True,
                    listing_values_sub_wizard.is_call_put_field_required())

    def test_context(self):

        try:
            self.precondition()


        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            print(traceback.format_exc() + " Search in ->  " + self.__class__.__name__)
