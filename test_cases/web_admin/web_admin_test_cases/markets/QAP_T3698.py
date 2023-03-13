import random
import string
import sys
import time
import traceback

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.markets.listings.listings_page import ListingsPage
from test_framework.web_admin_core.pages.markets.listings.listings_wizard import ListingsWizard
from test_framework.web_admin_core.pages.markets.listings.listings_values_sub_wizard import \
    ListingsValuesSubWizard
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T3698(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.instr_type = [
            self.data_set.get_instr_type("instr_type_3"),
            self.data_set.get_instr_type("instr_type_4"),
            self.data_set.get_instr_type("instr_type_5"),
            self.data_set.get_instr_type("instr_type_6"),
            self.data_set.get_instr_type("instr_type_7")
        ]

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        time.sleep(2)
        side_menu.open_listings_page()
        time.sleep(2)
        listing_page = ListingsPage(self.web_driver_container)
        listing_page.click_on_new()

    def test_context(self):
        listing_wizard = ListingsWizard(self.web_driver_container)
        listing_values_sub_wizard = ListingsValuesSubWizard(self.web_driver_container)

        try:
            self.precondition()
            time.sleep(2)
            listing_wizard.click_on_save_changes()

            self.verify("Error after click on [SAVE CHANGES] button", "Incorrect or missing values",
                        listing_wizard.get_error_message_inside_listing_wizard())

            listing_values_sub_wizard.set_instr_type(self.instr_type[0])
            time.sleep(1)
            self.verify(f"Is tenor required for {self.instr_type[0]}", True,
                        listing_values_sub_wizard.is_tenor_field_required())

            time.sleep(1)
            listing_values_sub_wizard.set_instr_type(self.instr_type[1])
            self.verify(f"Is tenor required for {self.instr_type[1]}", True,
                        listing_values_sub_wizard.is_tenor_field_required())
            time.sleep(1)
            listing_values_sub_wizard.set_instr_type(self.instr_type[2])
            self.verify(f"Is tenor required for {self.instr_type[2]}", True,
                        listing_values_sub_wizard.is_tenor_field_required())
            time.sleep(1)
            listing_values_sub_wizard.set_instr_type(self.instr_type[3])
            self.verify(f"Is maturity month year required for {self.instr_type[3]}", True,
                        listing_values_sub_wizard.is_maturity_month_year_field_required())
            time.sleep(1)
            listing_values_sub_wizard.set_instr_type(self.instr_type[4])
            self.verify(f"Is maturity month year required for {self.instr_type[4]}", True,
                        listing_values_sub_wizard.is_maturity_month_year_field_required())
            time.sleep(1)
            listing_values_sub_wizard.set_instr_type(self.instr_type[5])
            self.verify(f"Is strike price required required for {self.instr_type[5]}", True,
                        listing_values_sub_wizard.is_strike_price_field_required())
            time.sleep(1)
            self.verify(f"Is call put  required for {self.instr_type[5]}", True,
                        listing_values_sub_wizard.is_call_put_field_required())
            time.sleep(1)
            self.verify(f"Is maturity month year required for {self.instr_type[5]}", True,
                        listing_values_sub_wizard.is_maturity_month_year_field_required())

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
