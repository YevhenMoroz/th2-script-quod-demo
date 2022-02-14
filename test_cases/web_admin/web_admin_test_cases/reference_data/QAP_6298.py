import random
import string
import sys
import time
import traceback

from custom import basic_custom_actions
from test_cases.web_admin.web_admin_core.pages.login.login_page import LoginPage
from test_cases.web_admin.web_admin_core.pages.reference_data.venues.venues_page import VenuesPage
from test_cases.web_admin.web_admin_core.pages.reference_data.venues.venues_wizard import VenuesWizard
from test_cases.web_admin.web_admin_core.pages.reference_data.venues.venues_values_sub_wizard import \
    VenuesValuesSubWizard
from test_cases.web_admin.web_admin_core.pages.reference_data.venues.venues_dark_algo_commission_sub_wizard import \
    VenuesDarkAlgoCommissionSubWizard

from test_cases.web_admin.web_admin_core.pages.root.side_menu import SideMenu
from test_cases.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_6298(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id)
        self.login = "adm03"
        self.password = "adm03"

        self.type = "DarkPool"
        self.name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.id = self.name + "1ID"

        self.cost_per_trade = "10.1"
        self.per_unit_comm_amt = "12.2"
        self.comm_basis_point = "13.3"
        self.spread_discount_proportion = "14.4"

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        time.sleep(2)
        side_menu.open_venues_page()
        time.sleep(2)
        page = VenuesPage(self.web_driver_container)
        page.click_on_new()

        venues_wizard_values = VenuesValuesSubWizard(self.web_driver_container)
        venues_wizard_values.set_name(self.name)
        venues_wizard_values.set_id(self.id)
        venues_wizard_values.set_type(self.type)

        venues_wizard_dark = VenuesDarkAlgoCommissionSubWizard(self.web_driver_container)
        venues_wizard_dark.set_cost_per_trade(self.cost_per_trade)
        venues_wizard_dark.set_per_unit_comm_amt(self.per_unit_comm_amt)
        venues_wizard_dark.set_comm_basis_point(self.comm_basis_point)
        venues_wizard_dark.set_spread_discount_proportion(self.spread_discount_proportion)
        time.sleep(1)
        venues_wizard_dark.click_on_is_comm_per_unit_checkbox()

        venues_wizard = VenuesWizard(self.web_driver_container)
        venues_wizard.click_on_save_changes()

    def test_context(self):
        try:
            self.precondition()

            page = VenuesPage(self.web_driver_container)
            page.set_name_filter(self.name)
            time.sleep(2)
            page.click_on_more_actions()

            time.sleep(2)
            page.click_on_edit()
            time.sleep(2)
            venues_wizard_dark = VenuesDarkAlgoCommissionSubWizard(self.web_driver_container)
            expected_values_after_saved = [self.cost_per_trade, self.per_unit_comm_amt, self.comm_basis_point,
                                           self.spread_discount_proportion]
            actual_result = [venues_wizard_dark.get_cost_per_trade(), venues_wizard_dark.get_per_unit_comm_amt(),
                             venues_wizard_dark.get_comm_basis_point(),
                             venues_wizard_dark.get_spread_discount_proportion()]

            self.verify("Values saved correctly", expected_values_after_saved, actual_result)

            time.sleep(2)
            self.verify("Check-box \"Is Comm Per Unit\" is enable", True,
                        venues_wizard_dark.is_comm_per_unit_checkbox_selected())


        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
