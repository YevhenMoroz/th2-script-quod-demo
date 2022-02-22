import sys
import time
import traceback

from custom import basic_custom_actions
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase
from test_framework.web_trading.web_trading_core.pages.login.login_page import LoginPage
from test_framework.web_trading.web_trading_core.pages.main_page.main_page import MainPage
from test_framework.web_trading.web_trading_core.pages.main_page.menu.menu_page import MenuPage
from test_framework.web_trading.web_trading_core.pages.main_page.menu.profile.profile_page import ProfilePage
from test_framework.web_trading.web_trading_core.pages.main_page.order_ticket.order_ticket_page import OrderTicketPage


class QAP_6568(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id)
        self.login = "QA3"
        self.password = "QA3"
        self.quantity = '11'
        self.price = "22"
        self.symbol = "AADIIND-Z  "
        self.order_type = " Limit "
        self.time_in_force = "Day "

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.set_login(self.login)
        login_page.set_password(self.password)
        login_page.click_login_button()
        time.sleep(2)
        main_page = MainPage(self.web_driver_container)
        main_page.click_on_menu_button()
        menu_page = MenuPage(self.web_driver_container)
        menu_page.click_on_profile_button()
        profile_page = ProfilePage(self.web_driver_container)
        profile_page.click_on_preference_button()
        profile_page.click_on_cancel_button()
        profile_page.click_on_save_button()
        profile_page.click_on_close_button()
        main_page.click_on_new_workspace_button()
        main_page.click_on_buy_button()
        order_ticket = OrderTicketPage(self.web_driver_container)
        order_ticket.set_symbol(self.symbol)
        order_ticket.click_on_buy_mode_button()
        order_ticket.set_quantity(self.quantity)
        order_ticket.set_price(self.price)
        order_ticket.set_order_type(self.order_type)
        order_ticket.set_time_in_force(self.time_in_force)
        order_ticket.click_on_buy_button()

    def test_context(self):
        try:
            self.precondition()
            order_ticket = OrderTicketPage(self.web_driver_container)
            error_notification = order_ticket.get_error_notification()
            self.verify("Is there an error message? ", error_notification,
                        "Please set a Default Client in the Preferences page")

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
