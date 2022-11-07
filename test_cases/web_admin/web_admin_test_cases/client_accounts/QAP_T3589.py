import random
import sys
import time
import traceback

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.clients_accounts.clients.clients_page import ClientsPage
from test_framework.web_admin_core.pages.clients_accounts.clients.clients_assignments_sub_wizard \
    import ClientsAssignmentsSubWizard
from test_framework.web_admin_core.pages.clients_accounts.accounts.accounts_wizard import AccountsWizard

from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T3589(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.client = 'CLIENT1'

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        time.sleep(2)

    def test_context(self):
        try:
            self.precondition()

            side_menu = SideMenu(self.web_driver_container)
            side_menu.open_clients_page()
            time.sleep(2)
            client_page = ClientsPage(self.web_driver_container)
            client_page.set_name(self.client)
            time.sleep(1)
            client_page.click_on_more_actions()
            time.sleep(1)
            client_page.click_on_edit()
            time.sleep(2)
            client_assignments_tab = ClientsAssignmentsSubWizard(self.web_driver_container)
            list_of_assignee_accounts = client_assignments_tab.get_all_assigned_accounts()
            client_assignments_tab.click_on_account_link(random.choice(list_of_assignee_accounts))
            time.sleep(2)

            account_wizard = AccountsWizard(self.web_driver_container)
            self.verify("Account wizard page has been open", True, account_wizard.is_wizard_page_open())

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
