import random
import string
import sys
import time
import traceback

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.clients_accounts.client_lists.main_page import ClientListsPage
from test_framework.web_admin_core.pages.clients_accounts.client_lists.wizard import ClientListsWizard
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T3630(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.clients = [
            self.data_set.get_client("client_1"),
            self.data_set.get_client("client_2"),
            self.data_set.get_client("client_3")]

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        time.sleep(2)
        side_menu.open_client_list_page()
        client_list_page = ClientListsPage(self.web_driver_container)
        client_list_wizard = ClientListsWizard(self.web_driver_container)
        time.sleep(2)
        client_list_page.click_on_new()
        time.sleep(2)
        client_list_wizard.set_client_list_name(self.name)
        time.sleep(2)
        for client in self.clients:
            client_list_wizard.click_on_plus()
            time.sleep(2)
            client_list_wizard.set_client(client)
            client_list_wizard.click_on_checkmark()
        time.sleep(2)
        client_list_wizard.click_on_save_changes()
        time.sleep(2)
        client_list_page.set_name(self.name)
        time.sleep(2)
        client_list_page.click_on_more_actions()
        time.sleep(2)

    def test_context(self):
        try:
            self.precondition()
            client_list_page = ClientListsPage(self.web_driver_container)
            expected_pdf_content = [self.name,
                                    "CLIENT1",
                                    "CLIENT2",
                                    "CLIENT3"]
            self.verify("Is client list saved correctly ", True,
                        client_list_page.click_download_pdf_entity_button_and_check_pdf(expected_pdf_content))
        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
