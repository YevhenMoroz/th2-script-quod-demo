import random
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
from test_framework.web_trading.web_trading_core.pages.main_page.menu.profile.profile_preference_sub_wizard import \
    ProfilePreferenceSubWizard
from test_framework.web_trading.web_trading_core.pages.main_page.order_ticket.order_confirmation.order_confirmation_page import \
    OrderConfirmationPage
from test_framework.web_trading.web_trading_core.pages.main_page.order_ticket.order_ticket_page import OrderTicketPage
from test_framework.web_trading.web_trading_core.pages.main_page.workspace.order_book.order_book_page import \
    OrderBookPage


class QAP_6500(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.default_client = "POOJA"
        # Order info
        self.instrument = 'VALECHAENG-RL'
        self.account = 'POOJA'
        self.quantity = random.randint(0, 300)
        self.price = random.randint(0, 200)
        self.order_type = 'Limit'

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.set_login(self.login)
        login_page.set_password(self.password)
        login_page.click_login_button()
        time.sleep(2)
        main_page = MainPage(self.web_driver_container)
        # region set default client
        main_page.click_on_menu_button()
        menu_page = MenuPage(self.web_driver_container)
        menu_page.click_on_profile_button()
        profile_page = ProfilePage(self.web_driver_container)
        profile_page.click_on_preference_button()
        time.sleep(2)
        preference_page = ProfilePreferenceSubWizard(self.web_driver_container)
        preference_page.set_default_client_from_dropdown_list(self.default_client)
        time.sleep(2)
        profile_page.click_on_save_button()
        profile_page.click_on_close_button()
        time.sleep(2)
        # endregion
        # region set new order
        main_page.click_on_new_workspace_button()
        time.sleep(2)
        main_page.click_on_order_book_button()
        time.sleep(2)
        order_book = OrderBookPage(self.web_driver_container)
        order_book.click_on_maximize_button()
        main_page.click_on_buy_button()
        time.sleep(2)
        order_ticket = OrderTicketPage(self.web_driver_container)
        order_ticket.create_order(self.instrument, self.account, self.quantity, self.price, self.order_type)
        time.sleep(2)
        order_ticket.click_on_buy_button()
        time.sleep(2)
        confirmation_page = OrderConfirmationPage(self.web_driver_container)
        confirmation_page.click_on_place_button()
        time.sleep(4)

    def test_context(self):
        try:
            self.precondition()
            try:
                order_book = OrderBookPage(self.web_driver_container)
                self.verify("Does the order created successfully? ", self.quantity, order_book.get_order_qty())
            except Exception as e:
                print(e.__class__.__name__)

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
