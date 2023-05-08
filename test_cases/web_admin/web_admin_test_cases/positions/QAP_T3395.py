import sys
import time
import traceback
import random
import string

from custom import basic_custom_actions

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


class QAP_T3395(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.users = {"adm":
                          {"login": self.data_set.get_user("user_1"),
                           "password": self.data_set.get_password("password_1")},
                      "zone":
                          {"login": self.data_set.get_user("user_4"),
                           "password": self.data_set.get_password("password_4")}
                      }

        self.client_name = f"Client {self.__class__.__name__}"
        self.account_id = f"Account {self.__class__.__name__}"
        self.client_id = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.ext_id_client = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.disclose_exec = 'Manual'
        self.desk = self.data_set.get_desk("desk_3")
        self.user_manager = self.data_set.get_user("user_3")
        self.clearing_account_type = 'Firm'
        self.client_id_source = 'BIC'

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        side_menu = SideMenu(self.web_driver_container)
        client_page = ClientsPage(self.web_driver_container)
        account_page = AccountsPage(self.web_driver_container)
        common_act = CommonPage(self.web_driver_container)

        login_page.login_to_web_admin(self.users["adm"]["login"], self.users["adm"]["password"])
        side_menu.open_clients_page()
        client_page.set_name(self.client_name)
        time.sleep(1)
        if not client_page.is_searched_client_found(self.client_name):
            client_page.click_on_new()
            values_tab = ClientsValuesSubWizard(self.web_driver_container)
            values_tab.set_id(self.client_id)
            values_tab.set_name(self.client_name)
            values_tab.set_ext_id_client(self.ext_id_client)
            values_tab.set_disclose_exec(self.disclose_exec)
            assignments_tab = ClientsAssignmentsSubWizard(self.web_driver_container)
            assignments_tab.set_desk(self.desk)
            assignments_tab.set_user_manager(self.user_manager)
            wizard = ClientsWizard(self.web_driver_container)
            wizard.click_on_save_changes()
            time.sleep(1)

        side_menu.open_accounts_page()
        account_page.set_id(self.account_id)
        time.sleep(1)
        if not account_page.is_searched_account_found(self.account_id):
            account_page.click_new_button()
            values_tab = AccountsWizard(self.web_driver_container)
            values_tab.set_id(self.account_id)
            values_tab.set_ext_id_client(self.ext_id_client)
            values_tab.set_client_id_source(self.client_id_source)
            values_tab.set_client(self.client_name)
            wizard = AccountsWizard(self.web_driver_container)
            wizard.click_save_button()
            time.sleep(1)

        common_act.click_on_info_error_message_pop_up()
        common_act.click_on_user_icon()
        common_act.click_on_logout()
        time.sleep(2)
        common_act.refresh_page()

    def test_context(self):
        login_page = LoginPage(self.web_driver_container)
        side_menu = SideMenu(self.web_driver_container)
        cash_positions = SecurityPositionsPage(self.web_driver_container)

        try:
            self.precondition()

            login_page.login_to_web_admin(self.users["zone"]["login"], self.users["zone"]["password"])
            side_menu.open_security_positions_page()
            time.sleep(1)
            actual_result = cash_positions.get_all_accounts_from_drop_down_by_entered_pattern(self.account_id)
            self.verify("Dropdown contain only Security Accounts according with hierarchy "
                        f"the administrator(*user_zone*) is assigned to {self.account_id} is in dropdown.",
                        True, self.account_id in actual_result)

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
