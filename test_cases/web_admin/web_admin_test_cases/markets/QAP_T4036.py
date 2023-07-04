import random
import string
import time

from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.markets.market_data_sources.main_page import \
    MarketDataSourcesPage
from test_framework.web_admin_core.pages.markets.market_data_sources.wizard import \
    MarketDataSourcesWizard
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T4036(CommonTestCase):
    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.symbol = self.data_set.get_symbol_by_name("symbol_6")
        self.user = self.data_set.get_user("user_12")
        self.venue = self.data_set.get_venue_by_name("venue_1")
        self.md_source = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        time.sleep(2)
        side_menu.open_market_data_source_page()
        main_page = MarketDataSourcesPage(self.web_driver_container)
        main_page.click_on_new_button()
        time.sleep(2)
        wizard = MarketDataSourcesWizard(self.web_driver_container)
        wizard.set_symbol(self.symbol)
        time.sleep(1)
        wizard.set_user(self.user)
        time.sleep(1)
        wizard.set_venue(self.venue)
        time.sleep(1)

    def test_context(self):
        self.precondition()
        wizard = MarketDataSourcesWizard(self.web_driver_container)
        wizard.click_on_save_changes()
        time.sleep(1)
        self.verify("Incorrect or missing values message displayed", True,
                    wizard.is_incorrect_or_missing_value_message_displayed())
