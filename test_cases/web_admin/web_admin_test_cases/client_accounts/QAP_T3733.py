import time

from test_framework.web_admin_core.pages.clients_accounts.clients.clients_page import ClientsPage
from test_framework.web_admin_core.pages.clients_accounts.clients.clients_wizard import ClientsWizard
from test_framework.web_admin_core.pages.clients_accounts.clients.clients_values_sub_wizard import ClientsValuesSubWizard
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T3733(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = "adm03"
        self.password = "adm03"

        self.disclose_exec = "Manual"
        self.ext_id_client = 'CLIENT1'
        self.id = 'CLIENT1'

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        time.sleep(2)
        side_menu = SideMenu(self.web_driver_container)
        side_menu.open_clients_page()

    def test_context(self):
        self.precondition()

        main_page = ClientsPage(self.web_driver_container)
        main_page.click_on_new()
        values_sub_wizard = ClientsValuesSubWizard(self.web_driver_container)
        values_sub_wizard.set_disclose_exec(self.disclose_exec)
        wizard = ClientsWizard(self.web_driver_container)
        wizard.click_on_save_changes()
        time.sleep(1)
        self.verify("Is incorrect or missing value message displayed", True,
                    wizard.is_incorrect_or_missing_value_message_displayed())
        values_sub_wizard.set_id(self.id)
        values_sub_wizard.set_ext_id_client(self.ext_id_client)
        wizard.click_on_save_changes()
        time.sleep(1)
        self.verify("Such record already exists displayed", True, wizard.is_footer_warning_displayed())
