import random
import string
import time
import traceback

from custom import basic_custom_actions
from test_cases.web_admin.web_admin_core.pages.client_accounts.accounts.accounts_page import AccountsPage
from test_cases.web_admin.web_admin_core.pages.client_accounts.accounts.accounts_wizard import AccountsWizard
from test_cases.web_admin.web_admin_core.pages.login.login_page import LoginPage
from test_cases.web_admin.web_admin_core.pages.root.side_menu import SideMenu
from test_cases.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_3104(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id)
        self.login = "adm03"
        self.password = "adm03"
        self.id = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.ext_id_client = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.client = "CLIENT1"
        self.client_id_source = "BIC"

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        time.sleep(2)
        side_menu.open_accounts_page()
        time.sleep(2)
        accounts_page = AccountsPage(self.web_driver_container)
        accounts_page.click_new_button()
        time.sleep(2)
        accounts_wizard = AccountsWizard(self.web_driver_container)
        accounts_wizard.set_id(self.id)
        time.sleep(1)
        accounts_wizard.set_ext_id_client(self.ext_id_client)
        time.sleep(1)
        accounts_wizard.set_client(self.client)
        time.sleep(1)
        accounts_wizard.set_client_id_source(self.client_id_source)
        time.sleep(1)

    def test_context(self):
        try:
            self.precondition()
            accounts_wizard = AccountsWizard(self.web_driver_container)
            accounts_page = AccountsPage(self.web_driver_container)
            try:
                accounts_wizard.click_save_button()
                time.sleep(2)
                accounts_page.set_id(self.id)
                time.sleep(2)
                accounts_page.click_more_actions_button()
                self.verify("Account created correctly", True, True)
            except Exception as e:
                self.verify("Account not created", True, e.__class__.__name__)

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            print(traceback.format_exc() + " Search in ->  " + self.__class__.__name__)
