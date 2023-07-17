import time
import random
import string

from test_framework.web_admin_core.pages.clients_accounts.client_lists.main_page import ClientListsPage
from test_framework.web_admin_core.pages.clients_accounts.client_lists.wizard import ClientListsWizard
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T3554(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")

        self.client_list_name = "QAP5907"
        self.new_client_list_name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.client_list_description = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.client = "CLIENT1"

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        time.sleep(2)
        side_menu = SideMenu(self.web_driver_container)
        side_menu.open_client_list_page()
        time.sleep(2)
        client_list_page = ClientListsPage(self.web_driver_container)
        client_list_page.set_name(self.client_list_name)
        time.sleep(1)
        if not client_list_page.is_client_list_found(self.client_list_name):
            client_list_page.click_on_new()
            time.sleep(2)
            wizard = ClientListsWizard(self.web_driver_container)
            wizard.set_client_list_name(self.client_list_name)
            wizard.set_client_list_description(self.client_list_description)
            wizard.click_on_plus()
            wizard.set_client(self.client)
            wizard.click_on_checkmark()
            wizard.click_on_save_changes()
            time.sleep(2)
            client_list_page.set_name(self.client_list_name)
            time.sleep(1)

    def post_conditions(self):
        client_list_page = ClientListsPage(self.web_driver_container)
        client_list_page.click_on_more_actions()
        time.sleep(1)
        client_list_page.click_on_edit()
        time.sleep(2)
        wizard = ClientListsWizard(self.web_driver_container)
        wizard.set_client_list_name(self.client_list_name)
        wizard.set_client_list_description("")
        wizard.click_on_save_changes()
        time.sleep(2)

    def test_context(self):
        self.precondition()

        client_list_page = ClientListsPage(self.web_driver_container)
        client_list_page.click_on_more_actions()
        time.sleep(1)
        client_list_page.click_on_edit()
        time.sleep(2)
        wizard = ClientListsWizard(self.web_driver_container)
        wizard.set_client_list_name(self.new_client_list_name)
        wizard.set_client_list_description(self.client_list_description)
        wizard.click_on_save_changes()
        time.sleep(2)
        client_list_page.set_name(self.client_list_name)
        time.sleep(1)
        self.verify("Old Client List is not displayed at main page", False,
                    client_list_page.is_client_list_found(self.client_list_name))
        client_list_page.set_name(self.new_client_list_name)
        time.sleep(1)
        self.verify("Client List is edited and displayed at main page", True,
                    client_list_page.is_client_list_found(self.new_client_list_name))

        self.post_conditions()
