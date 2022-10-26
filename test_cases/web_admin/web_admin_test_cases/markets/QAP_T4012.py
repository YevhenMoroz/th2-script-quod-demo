import random
import string
import sys
import time
import traceback

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.markets.market_data_sources.main_page import \
    MarketDataSourcesPage
from test_framework.web_admin_core.pages.markets.market_data_sources.wizard import \
    MarketDataSourcesWizard
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T4012(CommonTestCase):
    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.symbol = self.data_set.get_symbol_by_name("symbol_6")
        self.user = self.data_set.get_user("user_5")
        self.venue = self.data_set.get_venue_by_name("venue_1")
        self.md_source = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.md_source_edited = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        time.sleep(2)
        side_menu.open_market_data_source_page()
        main_page = MarketDataSourcesPage(self.web_driver_container)
        main_page.click_on_more_actions()
        time.sleep(2)
        main_page.click_on_edit_at_more_actions()
        time.sleep(2)

    def test_context(self):
        try:
            self.precondition()
            wizard = MarketDataSourcesWizard(self.web_driver_container)
            main_page = MarketDataSourcesPage(self.web_driver_container)
            headers = ["Symbol", "User", "Venue"]
            is_actual_fields_enabled = [wizard.is_symbol_field_enabled(), wizard.is_user_field_enabled(),
                                        wizard.is_venue_field_enabled()]
            expected_result = [False, False, False]
            self.verify_arrays_of_data_objects("Is fields enabled", headers, expected_result, is_actual_fields_enabled)
            time.sleep(2)
            wizard.set_md_source(self.md_source_edited)
            time.sleep(2)
            wizard.click_on_save_changes()
            time.sleep(2)
            main_page.set_md_source_at_filter(self.md_source_edited)
            time.sleep(2)
            self.verify("After saved ", self.md_source_edited, main_page.get_md_source())
        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
