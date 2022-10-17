import sys
import time
import traceback

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.others.routes.routes_page import RoutesPage
from test_framework.web_admin_core.pages.others.routes.routes_venues_subwizard import RoutesVenuesSubWizard
from test_framework.web_admin_core.pages.others.routes.routes_wizard import RoutesWizard
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T3838(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.name = 'QAP_T3838'
        self.venue = self.data_set.get_venue_by_name("venue_6")
        self.max_ord_amt = "10000"
        self.max_ord_amt_currency = "EUR"
        self.currency_different_than = "EUR"
        self.max_ord_qty = "500"
        self.display_qty_max_pct_of_ord_qty = "5"

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        side_menu.open_routes_page()
        routes_page = RoutesPage(self.web_driver_container)
        routes_page.set_name_at_filter(self.name)
        time.sleep(1)
        if not routes_page.is_searched_route_found(self.name):
            routes_page.click_on_new_button()
            values_sub_wizard = RoutesWizard(self.web_driver_container)
            values_sub_wizard.set_name_at_values_tab(self.name)
            wizard = RoutesWizard(self.web_driver_container)
            wizard.click_on_save_changes()

    def test_context(self):
        try:
            self.precondition()

            routes_page = RoutesPage(self.web_driver_container)
            routes_page.set_name_at_filter(self.name)
            time.sleep(1)
            routes_page.click_on_more_actions()
            routes_page.click_on_edit_at_more_actions()
            routes_venues_sub_wizard = RoutesVenuesSubWizard(self.web_driver_container)
            routes_venues_sub_wizard.click_on_plus_at_venues_tab()
            routes_venues_sub_wizard.set_venue_at_venues_tab(self.venue)
            routes_venues_sub_wizard.set_ord_amt_less_than_std_mkt_size_checkbox_at_venues_tab()
            routes_venues_sub_wizard.set_max_ord_amt_at_venues_tab(self.max_ord_amt)
            routes_venues_sub_wizard.set_max_ord_amt_currency_at_venues_tab(self.max_ord_amt_currency)
            routes_venues_sub_wizard.set_currency_different_than_at_venues_tab(self.currency_different_than)
            routes_venues_sub_wizard.set_max_ord_qty_at_venues_tab(self.max_ord_qty)
            routes_venues_sub_wizard.set_display_qty_max_pct_of_ord_qty_at_venues_tab(self.display_qty_max_pct_of_ord_qty)
            routes_venues_sub_wizard.click_on_check_mark_at_venues_tab()
            wizard = RoutesWizard(self.web_driver_container)
            wizard.click_on_save_changes()

            routes_page.set_name_at_filter(self.name)
            time.sleep(1)
            routes_page.click_on_more_actions()
            routes_page.click_on_edit_at_more_actions()
            routes_venues_sub_wizard.set_venue_filter_at_venues_tab(self.venue)
            time.sleep(1)
            routes_venues_sub_wizard.click_on_edit_at_venues_tab()

            expected_result = ["True", self.max_ord_amt, self.max_ord_amt_currency, self.currency_different_than,
                               self.max_ord_qty, self.display_qty_max_pct_of_ord_qty]

            actual_result = [f"{routes_venues_sub_wizard.get_ord_amt_less_than_std_mkt_size_checkbox_at_venues_tab()}",
                             routes_venues_sub_wizard.get_max_ord_amt_at_venues_tab(),
                             routes_venues_sub_wizard.get_max_ord_amt_currency_at_venues_tab(),
                             routes_venues_sub_wizard.get_currency_different_than_at_venues_tab(),
                             routes_venues_sub_wizard.get_max_ord_qty_at_venues_tab(),
                             routes_venues_sub_wizard.get_display_qty_max_pct_of_ord_qty_at_venues_tab()]

            self.verify("Parameters are restored", expected_result, actual_result)

            routes_venues_sub_wizard.click_on_check_mark_at_venues_tab()
            routes_venues_sub_wizard.click_on_delete_at_venues_tab()
            wizard.click_on_save_changes()

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
