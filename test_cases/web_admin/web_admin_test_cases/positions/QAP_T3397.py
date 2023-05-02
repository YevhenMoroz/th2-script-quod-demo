import sys
import time
import traceback
import random
import string

from custom import basic_custom_actions
from test_framework.db_wrapper.db_manager import DBManager

from test_framework.web_admin_core.pages.clients_accounts.clients.clients_values_sub_wizard import \
    ClientsValuesSubWizard
from test_framework.web_admin_core.pages.clients_accounts.clients.clients_assignments_sub_wizard \
    import ClientsAssignmentsSubWizard
from test_framework.web_admin_core.pages.clients_accounts.clients.clients_page import ClientsPage
from test_framework.web_admin_core.pages.clients_accounts.clients.clients_wizard import ClientsWizard
from test_framework.web_admin_core.pages.general.common.common_page import CommonPage
from test_framework.web_admin_core.pages.clients_accounts.accounts.accounts_page import AccountsPage
from test_framework.web_admin_core.pages.clients_accounts.accounts.accounts_wizard import AccountsWizard
from test_framework.web_admin_core.pages.positions.security_positions.main_page import MainPage as SecurityPositionsPage

from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T3397(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None,
                 db_manager=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.users = {"adm": {"login": self.data_set.get_user("user_1"),
                           "password": self.data_set.get_password("password_1")}}
        self.db_manager = db_manager
        self.security_accounts = []

    def precondition(self):
        self.security_accounts = [_[0] for _ in self.db_manager.my_db.execute(
            f"SELECT ACCOUNTID FROM SECURITYACCOUNT WHERE ALIVE = 'Y' AND ISWASHBOOK = 'N' OR ISWASHBOOK IS NULL")]
        print(self.security_accounts)

    def test_context(self):
        login_page = LoginPage(self.web_driver_container)
        side_menu = SideMenu(self.web_driver_container)
        cash_positions = SecurityPositionsPage(self.web_driver_container)

        try:
            self.precondition()

            login_page.login_to_web_admin(self.users["adm"]["login"], self.users["adm"]["password"])
            side_menu.open_security_positions_page()
            time.sleep(1)

            actual_result = [cash_positions.is_searched_account_in_drop_down(_) for _ in
                             random.choices(self.security_accounts, k=5)]
            self.verify("Dropdown contain all Security Accounts",
                        [True for _ in range(5)], actual_result)

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
