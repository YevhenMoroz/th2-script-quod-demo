import random
import string
import time
import traceback
from uuid import uuid1

from custom import basic_custom_actions
from quod_qa.web_admin.web_admin_core.pages.client_accounts.accounts.accounts_page import AccountsPage
from quod_qa.web_admin.web_admin_core.pages.client_accounts.accounts.accounts_wizard import AccountsWizard
from quod_qa.web_admin.web_admin_core.pages.login.login_page import LoginPage
from quod_qa.web_admin.web_admin_core.pages.root.side_menu import SideMenu
from quod_qa.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer
from quod_qa.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_2183(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id)
        self.login = "adm03"
        self.password = "adm03"
        self.id = f"QAP-2183_{str(uuid1())}"
        self.client = "CLIENT1"
        self.client_id_source = "BIC"
        self.ext_id_client = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.clearing_type = "Firm"

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        time.sleep(2)
        side_menu.open_accounts_page()
        accounts_main_page = AccountsPage(self.web_driver_container)
        accounts_main_page.click_new_button()
        time.sleep(2)
        accounts_wizard = AccountsWizard(self.web_driver_container)
        accounts_wizard.set_id(self.id)
        time.sleep(2)
        accounts_wizard.set_client_id_source(self.client_id_source)
        time.sleep(2)
        accounts_wizard.set_ext_id_client(self.ext_id_client)
        time.sleep(1)
        accounts_wizard.set_clearing_account_type(self.clearing_type)
        time.sleep(2)
        accounts_wizard.set_client(self.client)
        time.sleep(2)


    def test_context(self):
        accounts_wizard = AccountsWizard(self.web_driver_container)
        accounts_main_page = AccountsPage(self.web_driver_container)
        try:
            self.precondition()
            try:
                accounts_wizard.click_save_button()
                self.verify("Account edit correctly", True, True)
                time.sleep(2)
                expected_saved_data = [self.client, self.clearing_type]
                actual_saved_data = [accounts_main_page.get_client(), accounts_main_page.get_clearing_account_type()]
                self.verify("Values displayed correctly", expected_saved_data, actual_saved_data)
            except Exception as e:
                self.verify("Problem in Save Changes", True, e.__class__.__name__)

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            print(traceback.format_exc() + " Search in ->  " + self.__class__.__name__)
