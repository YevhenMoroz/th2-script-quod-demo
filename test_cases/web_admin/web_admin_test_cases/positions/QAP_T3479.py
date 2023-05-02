import random
import string
import sys
import time
import traceback

from custom import basic_custom_actions

from test_framework.web_admin_core.pages.positions.cash_positions.main_page import *
from test_framework.web_admin_core.pages.positions.cash_positions.wizards import *
from test_framework.web_admin_core.pages.general.common.common_page import CommonPage

from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T3479(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None,
                 db_manager=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.db_manager = db_manager

        self.name = self.__class__.__name__
        self.client_cash_account_id = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.venue_cash_account_id = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.currency = 'ALL'
        self.client = ''
        self.initialbalance = 100
        self.amountbought = 150
        self.amountsoldin = 200
        self.cashdeposited = 250
        self.cashwithdrawn = 300
        self.bookedamt = 350
        self.reservedamt = 400

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        side_menu = SideMenu(self.web_driver_container)
        cash_positions_page = MainPage(self.web_driver_container)
        values_tab = ValuesTab(self.web_driver_container)
        wizard = MainWizard(self.web_driver_container)
        common_act = CommonPage(self.web_driver_container)

        login_page.login_to_web_admin(self.login, self.password)
        side_menu.open_cash_positions_page()
        cash_positions_page.set_name(self.name)
        time.sleep(1)
        if not cash_positions_page.is_searched_cash_account_found(self.name):
            cash_positions_page.click_on_new()
            values_tab.set_name(self.name)
            values_tab.set_client_cash_account_id(self.client_cash_account_id)
            values_tab.set_venue_cash_account_id(self.venue_cash_account_id)
            values_tab.set_currency(self.currency)
            self.client = random.choice(values_tab.get_all_client_from_drop_menu_by_patter('client'))
            values_tab.set_client(self.client)
            wizard.click_on_save_changes()
            time.sleep(1)

        self.db_manager.my_db.execute(f"UPDATE cashaccount SET initialbalance = {self.initialbalance},"
                                      f" amountbought = {self.amountbought}, amountsoldin = {self.amountsoldin},"
                                      f" cashdeposited = {self.cashdeposited}, cashwithdrawn = {self.cashwithdrawn},"
                                      f" bookedamt = {self.bookedamt}, reservedamt = {self.reservedamt}"
                                      f" WHERE cashaccountname = '{self.name}'")
        common_act.refresh_page(True)
        time.sleep(1)
        cash_positions_page.set_name(self.name)
        time.sleep(1)

    def test_context(self):
        cash_positions_page = MainPage(self.web_driver_container)
        positions_tab = PositionsTab(self.web_driver_container)

        try:
            self.precondition()

            cash_positions_page.click_on_more_actions()
            cash_positions_page.click_on_edit()
            time.sleep(1)
            available_balance = self.initialbalance - self.amountbought + self.cashdeposited - self.cashwithdrawn - \
                                self.bookedamt - self.reservedamt
            actual_balance = self.initialbalance + self.amountsoldin - self.amountbought + self.cashdeposited - \
                             self.cashwithdrawn

            self.verify(f"Available Balance = Initial Balance - Buy Amount + Cash Deposited - "
                        f"Cash Withdrawn - Booked Amount - Reserved Amount;.",
                        "{:.2f}".format(available_balance), positions_tab.get_available_balance())

            self.verify(f"Actual Balance = Initial Balance + Sell Amount - Buy Amount + Cash Deposited - Cash Withdrawn;",
                        "{:.2f}".format(actual_balance), positions_tab.get_actual_balance())

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
