import time
import traceback

from custom import basic_custom_actions
from test_cases.web_admin.web_admin_core.pages.client_accounts.clients.clients_page import ClientsPage
from test_cases.web_admin.web_admin_core.pages.client_accounts.clients.clients_policies_sub_wizard import \
    ClientsPoliciesSubWizard
from test_cases.web_admin.web_admin_core.pages.login.login_page import LoginPage
from test_cases.web_admin.web_admin_core.pages.root.side_menu import SideMenu
from test_cases.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_4381(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id)
        self.login = "adm03"
        self.password = "adm03"
        self.default_execution_strategy = "Default"

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        time.sleep(2)
        side_menu.open_clients_page()
        time.sleep(2)
        page = ClientsPage(self.web_driver_container)
        page.click_on_new()
        time.sleep(2)

    def test_context(self):
        try:
            self.precondition()
            policies_sub_wizard = ClientsPoliciesSubWizard(self.web_driver_container)
            self.verify("Is default execution strategy has italic font", True,
                        policies_sub_wizard.is_default_execution_strategy_has_italic_font())


        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            print(traceback.format_exc() + " Search in ->  " + self.__class__.__name__)
