import time
import traceback

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.clients_accounts.clients.clients_page import ClientsPage
from test_framework.web_admin_core.pages.clients_accounts.clients.clients_values_sub_wizard import \
    ClientsValuesSubWizard
from test_framework.web_admin_core.pages.clients_accounts.clients.clients_wizard import ClientsWizard
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T3733(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id)
        self.login = "adm03"
        self.password = "adm03"
        self.disclose_exec = "Manual"

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        time.sleep(2)
        side_menu.open_clients_page()
        time.sleep(2)
        main_page = ClientsPage(self.web_driver_container)
        main_page.click_on_new()
        wizard = ClientsWizard(self.web_driver_container)
        values_sub_wizard = ClientsValuesSubWizard(self.web_driver_container)
        values_sub_wizard.set_disclose_exec(self.disclose_exec)
        time.sleep(2)
        wizard.click_on_save_changes()

    def test_context(self):
        try:
            self.precondition()
            wizard = ClientsWizard(self.web_driver_container)
            self.verify("Is incorrect or missing value message displayed", True,
                        wizard.is_incorrect_or_missing_value_message_displayed())

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            print(traceback.format_exc() + " Search in ->  " + self.__class__.__name__)
