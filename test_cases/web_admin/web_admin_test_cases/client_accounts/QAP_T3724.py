import time
import random
import string

from test_framework.web_admin_core.pages.clients_accounts.accounts.accounts_page import AccountsPage
from test_framework.web_admin_core.pages.clients_accounts.accounts.accounts_wizard import AccountsWizard
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T3724(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")

        self.client = "BrokerACA"
        self.client_id_source = "BIC"
        self.ext_id_client = 'ACABankFirm'
        self.id = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        side_menu = SideMenu(self.web_driver_container)

        login_page.login_to_web_admin(self.login, self.password)
        side_menu.open_accounts_page()

    def test_context(self):
        main_page = AccountsPage(self.web_driver_container)
        values_sub_wizard = AccountsWizard(self.web_driver_container)
        wizard = AccountsWizard(self.web_driver_container)

        self.precondition()

        main_page.click_new_button()
        values_sub_wizard.set_id(self.id)
        values_sub_wizard.set_ext_id_client(self.ext_id_client)
        values_sub_wizard.set_client(self.client)
        values_sub_wizard.set_client_id_source(self.client_id_source)
        wizard.click_save_button()
        time.sleep(1)
        main_page.set_id(self.id)
        time.sleep(1)

        self.verify("Account with the same Ext Id Client created",
                    True, main_page.is_searched_account_found(self.id))
