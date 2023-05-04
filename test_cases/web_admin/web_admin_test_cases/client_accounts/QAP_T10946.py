import sys
import time
import traceback
import random
import string

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.clients_accounts.account_lists.main_page import MainPage
from test_framework.web_admin_core.pages.clients_accounts.account_lists.wizard import Wizard
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T10946(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")

        self.account_list_name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.accounts = ["ACABankFirm", "ACABankInst"]

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        side_menu = SideMenu(self.web_driver_container)

        login_page.login_to_web_admin(self.login, self.password)
        side_menu.open_account_list_page()

    def test_context(self):
        main_page = MainPage(self.web_driver_container)
        wizard = Wizard(self.web_driver_container)

        try:
            self.precondition()

            main_page.click_on_new()
            wizard.set_account_list_name(self.account_list_name)
            for i in self.accounts:
                wizard.click_on_plus()
                wizard.set_account(i)
                wizard.click_on_checkmark()
            wizard.click_on_save_changes()

            main_page.set_name(self.account_list_name)
            time.sleep(1)
            self.verify("New Account List is displayed in the grid",
                        True, main_page.is_account_list_found(self.account_list_name))
            main_page.click_on_more_actions()
            main_page.click_on_edit()

            self.verify("Added accounts are displayed correctly", self.accounts, wizard.get_all_accounts_from_table())

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
