import random
import string
import sys
import time
import traceback

from custom import basic_custom_actions
from test_cases.web_admin.web_admin_core.pages.login.login_page import LoginPage
from test_cases.web_admin.web_admin_core.pages.others.market_data_source.market_data_source_page import \
    MarketDataSourcePage
from test_cases.web_admin.web_admin_core.pages.others.market_data_source.market_data_source_wizard import \
    MarketDataSourceWizard
from test_cases.web_admin.web_admin_core.pages.root.side_menu import SideMenu
from test_cases.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_679(CommonTestCase):
    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id)
        self.login = "adm02"
        self.password = "adm02"
        self.symbol = "EUR/PHP"
        self.user = "adm02"
        self.venue = "AMEX"
        self.md_source = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        time.sleep(2)
        side_menu.open_market_data_source_page()
        main_page = MarketDataSourcePage(self.web_driver_container)
        main_page.click_on_new_button()
        time.sleep(2)
        wizard = MarketDataSourceWizard(self.web_driver_container)
        wizard.set_symbol(self.symbol)
        time.sleep(1)
        wizard.set_user(self.user)
        time.sleep(1)
        wizard.set_venue(self.venue)
        time.sleep(1)

    def test_context(self):
        try:
            self.precondition()
            wizard = MarketDataSourceWizard(self.web_driver_container)
            wizard.click_on_save_changes()
            time.sleep(1)
            self.verify("Incorrect or missing values message displayed", True, wizard.is_incorrect_or_missing_value_message_displayed())

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
