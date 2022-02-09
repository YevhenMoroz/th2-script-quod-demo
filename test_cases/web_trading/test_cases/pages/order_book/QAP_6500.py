import sys
import time
import traceback

from custom import basic_custom_actions

from test_cases.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase
from test_framework.web_trading.web_trading_core.pages.login.login_page import LoginPage
from test_framework.web_trading.web_trading_core.pages.main_page.main_page import MainPage
from test_framework.web_trading.web_trading_core.pages.main_page.menu.menu_page import MenuPage
from test_framework.web_trading.web_trading_core.pages.main_page.menu.profile.profile_page import ProfilePage
from test_framework.web_trading.web_trading_core.pages.main_page.menu.profile.profile_preference_sub_wizard import \
    ProfilePreferenceSubWizard
from test_framework.web_trading.web_trading_core.pages.main_page.order_ticket.order_confirmation.order_confirmation_page import OrderConfirmationPage
from test_framework.web_trading.web_trading_core.pages.main_page.order_ticket.order_ticket_page import OrderTicketPage
from test_framework.web_trading.web_trading_core.pages.main_page.workspace.order_book.order_book_page import OrderBookPage


class QAP_6500(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id)
        self.login = "QA5"
        self.password = "QA5"

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
        preference_page = ProfilePreferenceSubWizard(self.web_driver_container)
        preference_page.set_default_client_from_dropdown_list("POOJA GANESHAN")
        profile_page.click_on_save_button()
        profile_page.click_on_close_button()
        main_page.click_on_new_workspace_button()
        main_page.click_on_order_book_button()
        order_book = OrderBookPage(self.web_driver_container)
        order_book.click_on_maximize_button()
        main_page.click_on_buy_button()
        time.sleep(2)
        order_ticket = OrderTicketPage(self.web_driver_container)
        order_ticket.create_order("FIFMPS4FQP-MF ", " POOJA GANESHAN ", "11", "22", " Limit ")
        time.sleep(2)
        order_ticket.click_on_buy_button()
        confirmation_page = OrderConfirmationPage(self.web_driver_container)
        confirmation_page.click_on_place_button()
        self.order_id = order_book.get_order_id()
        order_book.click_on_filter_order_id_button()
        order_book.set_search_field(self.order_id)
        order_book.click_on_apply_button()
        self.status_order = order_book.get_order_status()

    def test_context(self):
        try:
            self.precondition()

            self.verify("Does the order created successfully? ", self.status_order, "Open")

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)