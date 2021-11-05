import random
import string
import time
import traceback

from custom import basic_custom_actions
from quod_qa.web_admin.web_admin_core.pages.client_accounts.client_list.client_list_page import ClientListPage
from quod_qa.web_admin.web_admin_core.pages.client_accounts.client_list.client_list_wizard import ClientListWizard
from quod_qa.web_admin.web_admin_core.pages.login.login_page import LoginPage
from quod_qa.web_admin.web_admin_core.pages.root.side_menu import SideMenu
from quod_qa.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer
from quod_qa.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_5443(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id)
        self.login = "adm03"
        self.password = "adm03"
        self.name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.clients = ["CLIENT1", "CLIENT2", "CLIENT3"]

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        time.sleep(2)
        side_menu.open_client_list_page()
        client_list_page = ClientListPage(self.web_driver_container)
        client_list_wizard = ClientListWizard(self.web_driver_container)
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
            client_list_page = ClientListPage(self.web_driver_container)
            expected_pdf_content = [self.name,
                                    "CLIENT1",
                                    "CLIENT2",
                                    "CLIENT3"]
            self.verify("Is client list saved correctly ", True,
                        client_list_page.click_download_pdf_entity_button_and_check_pdf(expected_pdf_content))
        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            print(traceback.format_exc() + " Search in ->  " + self.__class__.__name__)
