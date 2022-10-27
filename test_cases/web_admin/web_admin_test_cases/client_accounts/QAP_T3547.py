import sys
import time
import traceback

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.client_accounts.client_lists.main_page import ClientListsPage
from test_framework.web_admin_core.pages.client_accounts.client_lists.wizard import ClientListsWizard
from test_framework.web_admin_core.pages.client_accounts.clients.clients_page import ClientsPage
from test_framework.web_admin_core.pages.client_accounts.clients.clients_assignments_sub_wizard import \
    ClientsAssignmentsSubWizard
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T3547(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")

        self.first_client_list_name = "first_QAP5919"
        self.second_client_list_name = "second_QAP5919"
        self.client_list_description = "for QAP5919 test"
        self.clients = ["CLIENT1", "CLIENT2"]

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        side_menu.open_client_list_page()
        client_list_page = ClientListsPage(self.web_driver_container)
        client_list_page.set_name(self.first_client_list_name)
        time.sleep(1)
        if not client_list_page.is_client_list_found(self.first_client_list_name):
            client_list_page.click_on_new()
            wizard = ClientListsWizard(self.web_driver_container)
            wizard.set_client_list_name(self.first_client_list_name)
            wizard.set_client_list_description(self.client_list_description)
            wizard.click_on_plus()
            wizard.set_client(self.clients[0])
            wizard.click_on_checkmark()
            wizard.click_on_plus()
            wizard.set_client(self.clients[1])
            wizard.click_on_checkmark()
            wizard.click_on_save_changes()
            time.sleep(2)

        client_list_page.set_name(self.second_client_list_name)
        time.sleep(1)
        if not client_list_page.is_client_list_found(self.second_client_list_name):
            client_list_page.click_on_new()
            wizard = ClientListsWizard(self.web_driver_container)
            wizard.set_client_list_name(self.second_client_list_name)
            wizard.set_client_list_description(self.client_list_description)
            wizard.click_on_plus()
            wizard.set_client(self.clients[0])
            wizard.click_on_checkmark()
            wizard.click_on_plus()
            wizard.set_client(self.clients[1])
            wizard.click_on_checkmark()
            wizard.click_on_save_changes()

        side_menu.open_clients_page()

    def test_context(self):

        try:
            self.precondition()

            client_page = ClientsPage(self.web_driver_container)
            client_page.set_name(self.clients[0])
            time.sleep(1)
            client_page.click_on_more_actions()
            client_page.click_on_edit()
            client_assignments_tab = ClientsAssignmentsSubWizard(self.web_driver_container)
            assigned_client_lists = client_assignments_tab.get_all_assigned_client_lists()
            actual_result = True if self.first_client_list_name and self.second_client_list_name in assigned_client_lists else False
            self.verify("All assigned Client List displayed", True, actual_result)

            client_assignments_tab.click_on_client_list_link(self.second_client_list_name)
            client_list_wizard = ClientListsWizard(self.web_driver_container)
            time.sleep(2)
            self.verify("Client List wizard has been open", True, client_list_wizard.is_client_list_wizard_opened())
            side_menu = SideMenu(self.web_driver_container)
            client_list_wizard.click_on_revert_changes()
            side_menu.open_clients_page()
            time.sleep(1)
            client_page.set_name(self.clients[1])
            time.sleep(1)
            client_page.click_on_more_actions()
            client_page.click_on_edit()
            client_assignments_tab = ClientsAssignmentsSubWizard(self.web_driver_container)
            assigned_client_lists = client_assignments_tab.get_all_assigned_client_lists()
            actual_result = True if self.first_client_list_name and self.second_client_list_name in assigned_client_lists else False
            self.verify("All assigned Client List displayed", True, actual_result)

            client_assignments_tab.click_on_client_list_link(self.first_client_list_name)
            client_list_wizard = ClientListsWizard(self.web_driver_container)
            time.sleep(2)
            self.verify("Client List wizard has been open", True, client_list_wizard.is_client_list_wizard_opened())

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
