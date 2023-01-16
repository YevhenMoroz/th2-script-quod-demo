import sys
import time
import traceback
import random
import string

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.clients_accounts.client_lists.main_page import ClientListsPage
from test_framework.web_admin_core.pages.clients_accounts.client_lists.wizard import ClientListsWizard
from test_framework.web_admin_core.pages.clients_accounts.clients.clients_values_sub_wizard import ClientsValuesSubWizard
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T3549(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")

        self.client_list_name = "QAP_T3549"
        self.client_list_description = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.client = "CLIENT1"

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        side_menu.open_client_list_page()
        client_list_page = ClientListsPage(self.web_driver_container)
        client_list_page.set_name(self.client_list_name)
        time.sleep(1)
        if not client_list_page.is_client_list_found(self.client_list_name):
            client_list_page.click_on_new()
            wizard = ClientListsWizard(self.web_driver_container)
            wizard.set_client_list_name(self.client_list_name)
            wizard.set_client_list_description(self.client_list_description)
            wizard.click_on_plus()
            wizard.set_client(self.client)
            wizard.click_on_checkmark()
            wizard.click_on_save_changes()
            client_list_page.set_name(self.client_list_name)
            time.sleep(1)

    def test_context(self):

        try:
            self.precondition()

            client_list_page = ClientListsPage(self.web_driver_container)
            client_list_page.click_on_more_actions()
            client_list_page.click_on_edit()
            wizard = ClientListsWizard(self.web_driver_container)
            wizard.set_client_filter(self.client)
            time.sleep(1)
            wizard.click_on_edit()
            wizard.click_at_client_link()

            time.sleep(2)
            client_values_tab = ClientsValuesSubWizard(self.web_driver_container)
            self.verify("Client page has been open correct", self.client, client_values_tab.get_name())

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
