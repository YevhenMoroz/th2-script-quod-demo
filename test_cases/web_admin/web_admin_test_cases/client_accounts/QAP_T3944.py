import random
import string
import sys
import time
import traceback

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.clients_accounts.accounts.accounts_page import AccountsPage
from test_framework.web_admin_core.pages.clients_accounts.accounts.accounts_wizard import AccountsWizard
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T3944(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.route_account_name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.route = self.data_set.get_route("route_2")
        self.client = "ACABankFirm"
        self.clear_client = "Not found"
        self.test_client = ''
        self.clearing_type = [
            self.data_set.get_clearing_account_type("clearing_account_type_1"),
            self.data_set.get_clearing_account_type("clearing_account_type_2"),
            self.data_set.get_clearing_account_type("clearing_account_type_3")]

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        side_menu.open_accounts_page()
        time.sleep(2)
        accounts_main_page = AccountsPage(self.web_driver_container)
        self.test_client = accounts_main_page.get_id_grid_value()
        accounts_main_page.set_id(self.test_client)
        time.sleep(1)
        accounts_main_page.click_more_actions_button()
        time.sleep(1)
        accounts_main_page.click_edit_entity_button()
        time.sleep(2)
        accounts_wizard = AccountsWizard(self.web_driver_container)
        accounts_wizard.set_client(self.clear_client)
        time.sleep(1)

    def test_context(self):
        accounts_wizard = AccountsWizard(self.web_driver_container)
        accounts_main_page = AccountsPage(self.web_driver_container)
        try:
            self.precondition()
            try:
                for i in self.clearing_type:
                    accounts_wizard.set_clearing_account_type(i)
                    time.sleep(1)
                self.verify(f"\"Clearing Account Type\" drop-down contains {self.clearing_type}", True, True)

                accounts_wizard.set_client(self.client)
                accounts_wizard.click_save_button()
                self.verify("Account edit correctly", True, True)
                time.sleep(2)
                accounts_main_page.set_id(self.test_client)
                time.sleep(1)
                expected_saved_data = [self.client, self.clearing_type[1]]
                actual_saved_data = [accounts_main_page.get_client(), accounts_main_page.get_clearing_account_type()]
                self.verify("Values displayed correctly", expected_saved_data, actual_saved_data)
            except Exception as e:
                self.verify("Problem in Save Changes", True, e.__class__.__name__)

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
