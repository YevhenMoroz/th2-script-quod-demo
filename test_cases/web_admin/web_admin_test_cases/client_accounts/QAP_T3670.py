import time

from test_framework.web_admin_core.pages.clients_accounts.accounts.accounts_page import AccountsPage
from test_framework.web_admin_core.pages.clients_accounts.accounts.accounts_wizard import AccountsWizard
from test_framework.web_admin_core.pages.clients_accounts.account_lists.main_page import MainPage as AccountListPage
from test_framework.web_admin_core.pages.clients_accounts.account_lists.wizard import Wizard as AccountListWizard
from test_framework.web_admin_core.pages.clients_accounts.clients.clients_page import ClientsPage
from test_framework.web_admin_core.pages.clients_accounts.clients.clients_values_sub_wizard \
    import ClientsValuesSubWizard
from test_framework.web_admin_core.pages.clients_accounts.clients.clients_assignments_sub_wizard \
    import ClientsAssignmentsSubWizard
from test_framework.web_admin_core.pages.clients_accounts.clients.clients_wizard import ClientsWizard
from test_framework.web_admin_core.pages.clients_accounts.client_lists.main_page import ClientListsPage
from test_framework.web_admin_core.pages.clients_accounts.client_lists.wizard import ClientListsWizard
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T3670(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)

        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")

        self.account = {"id": f"Account {self.__class__.__name__}",
                        "ext_id_client": f"{self.__class__.__name__}_ext_id_client",
                        "name": f"Account {self.__class__.__name__}_name",
                        "client_id_source": "OMGEO"}

        self.account_list = {"name": f"{self.__class__.__name__}",
                             "account": "ACABankFirm"}

        self.client = {"id": f"Client {self.__class__.__name__}",
                       "name": f"Client {self.__class__.__name__}_name",
                       "ext_id_client": f"{self.__class__.__name__}_ext_id_client",
                       "disclose_exec": "RealTime",
                       "desks": self.data_set.get_desk("desk_1")}

        self.client_list = {"name": f"{self.__class__.__name__}",
                            "description": f"{self.__class__.__name__}_description",
                            "client": "CLIENT1"}

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)

    def test_context(self):
        side_menu = SideMenu(self.web_driver_container)
        accounts_page = AccountsPage(self.web_driver_container)
        accounts_wizard = AccountsWizard(self.web_driver_container)
        account_lists_page = AccountListPage(self.web_driver_container)
        account_lists_wizard = AccountListWizard(self.web_driver_container)
        clients_page = ClientsPage(self.web_driver_container)
        clients_values_tab = ClientsValuesSubWizard(self.web_driver_container)
        clients_assignments_tab = ClientsAssignmentsSubWizard(self.web_driver_container)
        clients_wizard = ClientsWizard(self.web_driver_container)
        client_lists_page = ClientListsPage(self.web_driver_container)
        client_lists_wizard = ClientListsWizard(self.web_driver_container)

        self.precondition()

        side_menu.open_accounts_page()
        accounts_page.set_id(self.account["id"])
        time.sleep(1)
        if not accounts_page.is_searched_account_found(self.account["id"]):
            accounts_page.click_new_button()
            accounts_wizard.set_id(self.account["id"])
            accounts_wizard.set_name(self.account["name"])
            accounts_wizard.set_ext_id_client(self.account["ext_id_client"])
            accounts_wizard.set_client_id_source(self.account["client_id_source"])
            accounts_wizard.click_save_button()
            time.sleep(1)
            accounts_page.set_id(self.account["id"])
            time.sleep(1)
        account_csv = accounts_page.click_on_download_csv_button_and_get_content()[0].values()
        actual_result = ''
        for i in list(self.account.items()):
            if i[1] not in account_csv:
                actual_result = f'{i[0]} = {i[1]} - not in CSV'
                break
            else: actual_result = True
        self.verify("CSV file contains Account data", True, actual_result)

        side_menu.open_account_list_page()
        time.sleep(1)
        account_lists_page.set_name(self.account_list["name"])
        time.sleep(1)
        if not account_lists_page.is_account_list_found(self.account_list["name"]):
            account_lists_page.click_on_new()
            account_lists_wizard.set_account_list_name(self.account_list["name"])
            account_lists_wizard.click_on_plus()
            account_lists_wizard.set_account(self.account_list["account"])
            account_lists_wizard.click_on_checkmark()
            account_lists_wizard.click_on_save_changes()
            time.sleep(1)
            account_lists_page.set_name(self.account_list["name"])
            time.sleep(1)
        account_list_csv = account_lists_page.click_on_download_csv_button_and_get_content()[0].values()
        self.account_list.pop("account")
        actual_result = ''
        for i in list(self.account_list.items()):
            if i[1] not in account_list_csv:
                actual_result = f'{i[0]} = {i[1]} - not in CSV'
                break
            else:
                actual_result = True
        self.verify("CSV file contains Account List data", True, actual_result)

        side_menu.open_clients_page()
        clients_page.set_name(self.client["name"])
        time.sleep(1)
        if not clients_page.is_searched_client_found(self.client["name"]):
            clients_page.click_on_new()
            clients_values_tab.set_id(self.client["id"])
            clients_values_tab.set_name(self.client["name"])
            clients_values_tab.set_ext_id_client(self.client["ext_id_client"])
            clients_values_tab.set_disclose_exec(self.client["disclose_exec"])
            clients_assignments_tab.set_desk(self.client["desks"])
            clients_wizard.click_on_save_changes()
            time.sleep(1)
            clients_page.set_name(self.client["name"])
            time.sleep(1)
        clients_csv = clients_page.click_on_download_csv_button_and_get_content()[0].values()
        self.client.pop("id")
        actual_result = ''
        for i in list(self.client.items()):
            if i[1] not in clients_csv:
                actual_result = f'{i[0]} = {i[1]} - not in CSV'
                break
            else:
                actual_result = True
        self.verify("CSV file contains Client data", True, actual_result)

        side_menu.open_client_list_page()
        client_lists_page.set_name(self.client_list["name"])
        time.sleep(1)
        if not client_lists_page.is_client_list_found(self.client_list["name"]):
            client_lists_page.click_on_new()
            client_lists_wizard.set_client_list_name(self.client_list["name"])
            client_lists_wizard.set_client_list_description(self.client_list["description"])
            client_lists_wizard.click_on_plus()
            client_lists_wizard.set_client(self.client_list["client"])
            client_lists_wizard.click_on_checkmark()
            client_lists_wizard.click_on_save_changes()
            client_lists_page.set_name(self.client_list["name"])
            time.sleep(1)
        client_list_csv = client_lists_page.click_on_download_csv_button_and_get_content()[0].values()
        self.client_list.pop("client")
        actual_result = ''
        for i in list(self.client_list.items()):
            if i[1] not in client_list_csv:
                actual_result = f'{i[0]} = {i[1]} - not in CSV'
                break
            else:
                actual_result = True
        self.verify("CSV file contains Client List data", True, actual_result)
