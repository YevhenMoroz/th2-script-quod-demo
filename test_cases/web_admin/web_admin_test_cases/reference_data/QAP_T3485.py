import random
import string
import sys
import time
import traceback

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.reference_data.venues.venues_page import VenuesPage
from test_framework.web_admin_core.pages.reference_data.venues.venues_wizard import VenuesWizard
from test_framework.web_admin_core.pages.reference_data.venues.venues_values_sub_wizard import \
    VenuesValuesSubWizard
from test_framework.web_admin_core.pages.reference_data.venues.venues_dark_algo_commission_sub_wizard import \
    VenuesDarkAlgoCommissionSubWizard

from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T3485(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.type = self.data_set.get_venue_type("venue_type_1")
        self.name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.client_venue_id = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.id = self.name + "1ID"
        self.cost_per_trade = round(random.uniform(0.1, 20), 2)
        self.per_unit_comm_amt = round(random.uniform(0.1, 20), 2)
        self.comm_basis_point = round(random.uniform(0.1, 20), 2)
        self.spread_discount_proportion = round(random.uniform(0.1, 20), 2)

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        time.sleep(2)
        side_menu.open_venues_page()
        time.sleep(2)
        page = VenuesPage(self.web_driver_container)
        page.click_on_new()
        time.sleep(2)

        venues_wizard_values = VenuesValuesSubWizard(self.web_driver_container)
        venues_wizard_values.set_name(self.name)
        venues_wizard_values.set_client_venue_id(self.client_venue_id)
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
        time.sleep(2)

    def test_context(self):
        try:
            self.precondition()

            page = VenuesPage(self.web_driver_container)
            page.set_name_filter(self.name)
            time.sleep(1)
            page.click_on_more_actions()
            time.sleep(1)
            page.click_on_edit()
            time.sleep(2)
            venues_wizard_dark = VenuesDarkAlgoCommissionSubWizard(self.web_driver_container)
            expected_values_after_saved = [str(self.cost_per_trade), str(self.per_unit_comm_amt),
                                           str(self.comm_basis_point), str(self.spread_discount_proportion)]
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
