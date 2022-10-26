import sys
import time
import traceback

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.markets.venues.venues_market_data_sub_wizard import \
    VenuesMarketDataSubWizard
from test_framework.web_admin_core.pages.markets.venues.venues_page import VenuesPage
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T3875(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.feed_source = [
            self.data_set.get_feed_source("feed_source_1"),
            self.data_set.get_feed_source("feed_source_2"),
            self.data_set.get_feed_source("feed_source_3"),
            self.data_set.get_feed_source("feed_source_4"),
            self.data_set.get_feed_source("feed_source_5"),
            self.data_set.get_feed_source("feed_source_6"),
            self.data_set.get_feed_source("feed_source_7")
        ]

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

    def test_context(self):
        try:
            self.precondition()
            market_data_sub_wizard = VenuesMarketDataSubWizard(self.web_driver_container)

            try:
                for i in range(len(self.feed_source)):
                    market_data_sub_wizard.set_feed_source(self.feed_source[i])
                self.verify("Is feed source contains all valid values", True, True)
            except Exception as e:
                self.verify("Is feed source contains all valid values", True, e.__class__.__name__)

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
