import sys
import time
import traceback

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.clients_accounts.clients.clients_assignments_sub_wizard import \
    ClientsAssignmentsSubWizard
from test_framework.web_admin_core.pages.clients_accounts.clients.clients_page import ClientsPage
from test_framework.web_admin_core.pages.clients_accounts.clients.clients_values_sub_wizard import \
    ClientsValuesSubWizard
from test_framework.web_admin_core.pages.clients_accounts.clients.clients_wizard import ClientsWizard
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T3680(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.name = 'RogueTrader'
        self.assigned_accounts = ''

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        side_menu.open_clients_page()

    def test_context(self):

        try:
            self.precondition()

            main_page = ClientsPage(self.web_driver_container)
            main_page.set_name(self.name)
            time.sleep(1)
            main_page.click_on_more_actions()
            main_page.click_on_edit()
            assignments_sub_wizard = ClientsAssignmentsSubWizard(self.web_driver_container)
            self.assigned_accounts = assignments_sub_wizard.get_all_assigned_accounts()

            values_sub_wizard = ClientsValuesSubWizard(self.web_driver_container)
            values_sub_wizard.set_default_account(self.assigned_accounts[0])

            wizard = ClientsWizard(self.web_driver_container)
            wizard.click_on_save_changes()

            main_page.set_name(self.name)
            time.sleep(1)
            main_page.click_on_more_actions()
            main_page.click_on_edit()

            self.verify("Default account has been save", self.assigned_accounts[0],
                        values_sub_wizard.get_default_account())

            values_sub_wizard.set_default_account(self.assigned_accounts[1])

            wizard = ClientsWizard(self.web_driver_container)
            wizard.click_on_save_changes()

            main_page.set_name(self.name)
            time.sleep(1)
            main_page.click_on_more_actions()
            main_page.click_on_edit()

            self.verify("Default account has been save", self.assigned_accounts[1],
                        values_sub_wizard.get_default_account())

            values_sub_wizard.clear_default_account()
            wizard.click_on_save_changes()

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
