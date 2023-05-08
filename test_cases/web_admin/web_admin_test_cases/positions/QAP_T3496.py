import random
import string
import sys
import time
import traceback

from custom import basic_custom_actions
from test_framework.db_wrapper.db_manager import DBManager

from test_framework.web_admin_core.pages.positions.cash_positions.main_page import *
from test_framework.web_admin_core.pages.positions.cash_positions.wizards import *
from test_framework.web_admin_core.pages.general.common.common_page import CommonPage

from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T3496(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")

        self.name = self.__class__.__name__
        self.client_cash_account_id = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.venue_cash_account_id = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.currency = 'EUR'
        self.client = ''
        self.enable_message = f"Cash Position {self.name} Disabled"
        self.disable_message = f"Cash Position {self.name} Enabled"

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
            cash_positions_page.set_name(self.name)
            time.sleep(1)

        self.db_manager.execute_query(f"UPDATE cashaccount SET initialbalance= '0', amountbought = '0', "
                                      f"amountsoldin = '0', cashdeposited = '0', cashwithdrawn = '0', "
                                      f"bookedamt = '0' WHERE cashaccountname = '{self.name}'")

        common_act.refresh_page(True)
        cash_positions_page.set_name(self.name)
        time.sleep(1)

    def test_context(self):
        pass
        cash_positions_page = MainPage(self.web_driver_container)
        common_act = CommonPage(self.web_driver_container)

        try:
            self.precondition()

            cash_positions_page.click_on_enable_disable_button()
            cash_positions_page.click_on_ok_button()
            time.sleep(1)
            self.verify("Entity disabled", self.disable_message, common_act.get_error_pop_up_text())

            common_act.click_on_info_error_message_pop_up()
            cash_positions_page.click_on_enable_disable_button()
            cash_positions_page.click_on_ok_button()
            time.sleep(1)
            self.verify("Entity enabled", self.enable_message, common_act.get_error_pop_up_text())

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
