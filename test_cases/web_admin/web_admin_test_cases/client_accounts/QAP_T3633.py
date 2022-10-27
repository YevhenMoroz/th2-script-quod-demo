import random
import string
import sys
import time
import traceback

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.clients_accounts.clients.clients_page import ClientsPage
from test_framework.web_admin_core.pages.clients_accounts.clients.clients_wizard import ClientsWizard
from test_framework.web_admin_core.pages.clients_accounts.clients.clients_values_sub_wizard import ClientsValuesSubWizard
from test_framework.web_admin_core.pages.clients_accounts.clients.clients_assignments_sub_wizard \
    import ClientsAssignmentsSubWizard

from test_framework.web_admin_core.pages.clients_accounts.accounts.accounts_page import AccountsPage
from test_framework.web_admin_core.pages.clients_accounts.accounts.accounts_wizard import AccountsWizard

from test_framework.web_admin_core.pages.general.common.common_page import CommonPage
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T3633(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)

        self.test_data = {
            "adm_user": {
                "login": "adm03",
                "password": "adm03"
            },
            "desk_user": {
                "login": "adm_desk",
                "password": "adm_desk"
            },
            "client": {
                "id": 'QAP5416' + ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6)),
                "name": 'QAP5416',
                "disclose_exec": 'Manual',
                "ext_id_client": ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6)),
                "desk": 'Quod Desk',
                "user_manager": 'adm_desk'
            },
            "account": {
                "id": 'QAP5416',
                "ext_id_client": ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6)),
                "client": 'QAP5416',
                "clearing_account_type": 'Firm',
                "client_id_source": 'BIC'
            }
        }

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.test_data['adm_user']['login'], self.test_data['adm_user']['password'])
        time.sleep(2)
        side_menu = SideMenu(self.web_driver_container)
        side_menu.open_clients_page()
        time.sleep(2)
        client_page = ClientsPage(self.web_driver_container)
        client_page.set_name(self.test_data['client']['name'])
        time.sleep(2)
        if not client_page.is_searched_client_found(self.test_data['client']['name']):
            client_page.click_on_new()
            time.sleep(2)
            client_values_tab = ClientsValuesSubWizard(self.web_driver_container)
            client_values_tab.set_id(self.test_data['client']['id'])
            client_values_tab.set_name(self.test_data['client']['name'])
            client_values_tab.set_ext_id_client(self.test_data['client']['ext_id_client'])
            client_values_tab.set_disclose_exec(self.test_data['client']['disclose_exec'])
            client_assignments_tab = ClientsAssignmentsSubWizard(self.web_driver_container)
            client_assignments_tab.set_desk(self.test_data['client']['desk'])
            client_assignments_tab.set_user_manager(self.test_data['client']['user_manager'])
            client_wizard = ClientsWizard(self.web_driver_container)
            client_wizard.click_on_save_changes()
            time.sleep(2)

        side_menu.open_accounts_page()
        time.sleep(2)
        account_page = AccountsPage(self.web_driver_container)
        account_page.set_id(self.test_data['account']['id'])
        time.sleep(2)
        if not account_page.is_searched_account_found(self.test_data['account']['id']):
            account_page.click_new_button()
            time.sleep(2)
            account_values_tab = AccountsWizard(self.web_driver_container)
            account_values_tab.set_id(self.test_data['account']['id'])
            account_values_tab.set_ext_id_client(self.test_data['account']['ext_id_client'])
            account_values_tab.set_client(self.test_data['account']['client'])
            # account_values_tab.set_clearing_account_type(self.test_data['account']['clearing_account_type'])
            account_values_tab.set_client_id_source(self.test_data['account']['client_id_source'])
            account_values_tab.click_save_button()
            time.sleep(2)

        common_act = CommonPage(self.web_driver_container)
        common_act.click_on_info_error_message_pop_up()
        common_act.click_on_user_icon()
        time.sleep(1)
        common_act.click_on_logout()
        time.sleep(2)

    def test_context(self):
        try:
            self.precondition()

            login_page = LoginPage(self.web_driver_container)
            login_page.login_to_web_admin(self.test_data['desk_user']['login'], self.test_data['desk_user']['password'])
            time.sleep(2)
            side_menu = SideMenu(self.web_driver_container)
            side_menu.open_accounts_page()
            time.sleep(2)
            account_page = AccountsPage(self.web_driver_container)
            account_page.set_id(self.test_data['account']['id'])
            time.sleep(2)
            account_page.click_more_actions_button()
            time.sleep(1)
            account_page.click_edit_entity_button()
            time.sleep(2)
            account_values_tab = AccountsWizard(self.web_driver_container)
            clients_available_for_selection = account_values_tab.get_all_clients_from_drop_menu()

            self.verify("Client field displays dropdown only with available Client values for User",
                        True, True if self.test_data['account']['client'] in clients_available_for_selection else False)

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
