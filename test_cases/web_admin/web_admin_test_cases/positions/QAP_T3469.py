import random
import string
import time

from test_framework.web_admin_core.pages.positions.cash_positions.main_page import *
from test_framework.web_admin_core.pages.positions.cash_positions.wizards import *

from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T3469(CommonTestCase):

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
        self.currency = 'EUR'
        self.client = ''
        self.transaction_type = ['TemporaryCashDeposit', 'TemporaryCashWithdrawal']
        self.amount = 10

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        side_menu = SideMenu(self.web_driver_container)
        cash_positions_page = MainPage(self.web_driver_container)
        values_tab = ValuesTab(self.web_driver_container)
        wizard = MainWizard(self.web_driver_container)

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
            cash_positions_page.set_name(self.name)
            time.sleep(1)

    def test_context(self):
        cash_positions_page = MainPage(self.web_driver_container)
        positions_tab = PositionsTab(self.web_driver_container)
        wizard = MainWizard(self.web_driver_container)

        self.precondition()

        cash_positions_page.click_on_transaction()
        cash_positions_page.set_transaction_type(self.transaction_type[0])
        cash_positions_page.set_amount(self.amount)
        cash_positions_page.click_on_ok_button()
        time.sleep(1)
        cash_positions_page.click_on_more_actions()
        cash_positions_page.click_on_edit()
        time.sleep(1)
        # TODO
        # Now only done for Postgres, needs to be completed for Oracle
        self.db_manager.my_db.execute(f"SELECT temporarycash  FROM cashaccount WHERE cashaccountname = '{self.name}'")
        temporary_cash = self.db_manager.my_db.fetchall()[0][0]
        self.verify(f"Temporary Cash is increased on entered Amount value. {self.amount}.",
                    "{:.2f}".format(int(temporary_cash)), str(positions_tab.get_temporary_cash()))

        wizard.click_on_close()
        time.sleep(1)
        if wizard.is_confirmation_of_leave_wizard_displayed():
            wizard.click_on_ok_button()
        cash_positions_page.set_name(self.name)
        time.sleep(1)
        cash_positions_page.click_on_transaction()
        cash_positions_page.set_transaction_type(self.transaction_type[1])
        cash_positions_page.set_amount(self.amount)
        cash_positions_page.click_on_ok_button()
        time.sleep(1)
        cash_positions_page.click_on_more_actions()
        cash_positions_page.click_on_edit()
        time.sleep(1)
        # TODO
        # Now only done for Postgres, needs to be completed for Oracle
        self.db_manager.my_db.execute(f"SELECT temporarycash  FROM cashaccount WHERE cashaccountname = '{self.name}'")
        temporary_cash = self.db_manager.my_db.fetchall()[0][0]
        self.verify(f"Temporary Cash is decreased on entered Amount value. {self.amount}.",
                    "{:.2f}".format(int(temporary_cash)), str(positions_tab.get_temporary_cash()))
