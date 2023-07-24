import random
import string
import time

from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.pages.users.users.users_page import UsersPage
from test_framework.web_admin_core.pages.users.users.users_venue_trader_sub_wizard import UsersVenueTraderSubWizard
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T11288(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")

        self.venue = self.data_set.get_venue_by_name("venue_1")
        self.venue_trade_name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        side_menu = SideMenu(self.web_driver_container)

        login_page.login_to_web_admin(self.login, self.password)
        side_menu.open_users_page()

    def test_context(self):
        users_page = UsersPage(self.web_driver_container)
        venues_trade_tab = UsersVenueTraderSubWizard(self.web_driver_container)

        self.precondition()
        users_page.click_on_new_button()

        venues_trade_tab.click_on_plus_button()
        venues_trade_tab.set_venue(self.venue)
        venues_trade_tab.set_venue_trader_name(self.venue_trade_name)
        venues_trade_tab.click_on_checkmark_button()
        time.sleep(1)
        self.verify("New entry has been added to table", True, venues_trade_tab.is_venue_trader_tab_contains_entries())
