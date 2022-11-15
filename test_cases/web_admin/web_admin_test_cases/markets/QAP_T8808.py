import random
import string
import sys
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


class QAP_T8808(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.opt_attr = '1'
        self.listing = 'ALDAR'

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        side_menu.open_listings_page()

    def test_context(self):
        wizard = ListingsWizard(self.web_driver_container)
        values_tab = ListingsValuesSubWizard(self.web_driver_container)
        main_page = ListingsPage(self.web_driver_container)

        try:
            self.precondition()

            main_page.load_listing_from_global_filter(self.listing)
            main_page.click_on_more_actions()
            main_page.click_on_edit()

            values_tab.set_opt_attr(self.opt_attr)
            wizard.click_on_save_changes()

            main_page.load_listing_from_global_filter(self.listing)
            main_page.click_on_more_actions()
            main_page.click_on_edit()

            self.verify("The Opt Attr field saved", self.opt_attr, values_tab.get_opt_attr())

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
