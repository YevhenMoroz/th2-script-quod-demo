import random
import string
import time
import traceback

from custom import basic_custom_actions
from quod_qa.web_admin.web_admin_core.pages.client_accounts.accounts.accounts_page import AccountsPage
from quod_qa.web_admin.web_admin_core.pages.client_accounts.accounts.accounts_routes_subwizard import \
    AccountsRoutesSubWizard
from quod_qa.web_admin.web_admin_core.pages.client_accounts.accounts.accounts_wizard import AccountsWizard
from quod_qa.web_admin.web_admin_core.pages.login.login_page import LoginPage
from quod_qa.web_admin.web_admin_core.pages.root.side_menu import SideMenu
from quod_qa.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer
from quod_qa.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_1740(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id)
        self.console_error_lvl_id = second_lvl_id
        self.login = "adm02"
        self.password = "adm02"
        self.route_account_name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.route = "DB RFQ"

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        time.sleep(2)
        side_menu.open_accounts_page()
        accounts_main_page = AccountsPage(self.web_driver_container)
        accounts_main_page.click_more_actions_button()
        time.sleep(1)
        accounts_main_page.click_edit_entity_button()
        routes_tab = AccountsRoutesSubWizard(self.web_driver_container)
        routes_tab.open_routes_subwizard()
        routes_tab.set_route_account_name(self.route_account_name)
        routes_tab.set_route(self.route)
        routes_tab.click_create_entity_button()
        time.sleep(2)

    def test_context(self):
        accounts_wizard = AccountsWizard(self.web_driver_container)
        try:
            self.precondition()
            try:
                accounts_wizard.click_save_button()
                self.verify("Account edit correctly", True, True)
            except Exception as e:
                self.verify("Problem in Save Changes button", True, e.__class__.__name__)

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.console_error_lvl_id,
                                              status='FAILED')
            print(traceback.format_exc() + " Search in ->  " + self.__class__.__name__)
