import random
import string
import sys
import time
import traceback

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.client_accounts.clients.clients_page import ClientsPage
from test_framework.web_admin_core.pages.client_accounts.accounts.accounts_page import AccountsPage
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T3252(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.test_client = 'ACABankFirm'

        self.id = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.ext_id_client = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.disclose_exec = self.data_set.get_disclose_exec("disclose_exec_1")
        self.desks = 'Quod Desk'
        self.user_manager = '12'

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)

    def post_condition(self):
        side_menu = SideMenu(self.web_driver_container)
        side_menu.open_clients_page()
        client_page = ClientsPage(self.web_driver_container)
        client_page.set_name(self.test_client)
        time.sleep(1)
        if not client_page.is_client_enable():
            client_page.click_on_enable_disable()

    def test_context(self):
        try:
            self.precondition()

            side_menu = SideMenu(self.web_driver_container)
            side_menu.open_accounts_page()
            account_page = AccountsPage(self.web_driver_container)
            account_page.set_id(self.test_client)
            time.sleep(1)
            account_status = account_page.is_account_enabled()

            side_menu.open_clients_page()
            client_page = ClientsPage(self.web_driver_container)
            client_page.set_name(self.test_client)
            time.sleep(1)
            if not client_page.is_client_enable():
                client_page.click_on_enable_disable()
                time.sleep(1)
                client_page.click_on_enable_disable()
            else:
                client_page.click_on_enable_disable()

            side_menu.open_accounts_page()

            account_page.set_id(self.test_client)
            time.sleep(1)
            self.verify("Account still enable", account_status, account_page.is_account_enabled())

            self.post_condition()

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
