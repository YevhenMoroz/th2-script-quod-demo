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


class QAP_T3943(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.id = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.client = self.data_set.get_client("client_1")
        self.client_id_source = self.data_set.get_client_id_source("client_id_source_1")
        self.ext_id_client = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.clearing_type = [
            self.data_set.get_clearing_account_type("clearing_account_type_1"),
            self.data_set.get_clearing_account_type("clearing_account_type_2"),
            self.data_set.get_clearing_account_type("clearing_account_type_3")]

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        time.sleep(2)
        side_menu.open_accounts_page()
        accounts_main_page = AccountsPage(self.web_driver_container)
        accounts_main_page.click_new_button()
        time.sleep(2)
        accounts_wizard = AccountsWizard(self.web_driver_container)
        accounts_wizard.set_id(self.id)
        accounts_wizard.set_client_id_source(self.client_id_source)
        accounts_wizard.set_ext_id_client(self.ext_id_client)
        accounts_wizard.set_clearing_account_type(self.clearing_type[-1])
        accounts_wizard.set_client(self.client)
        time.sleep(2)

    def test_context(self):
        accounts_wizard = AccountsWizard(self.web_driver_container)
        accounts_main_page = AccountsPage(self.web_driver_container)
        try:
            self.precondition()
            try:

                accounts_wizard.click_save_button()
                time.sleep(2)
                accounts_main_page.set_id(self.id)
                time.sleep(2)
                expected_saved_data = [self.client, "Institutional"]
                actual_saved_data = [accounts_main_page.get_client(), accounts_main_page.get_clearing_account_type()]
                self.verify("Values displayed correctly", expected_saved_data, actual_saved_data)
            except Exception as e:
                self.verify("Problem in or after Save Changes", True, e.__class__.__name__)
                time.sleep(5)
        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
