import random
import string
import sys
import time
import traceback

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.clients_accounts.accounts.accounts_page import AccountsPage
from test_framework.web_admin_core.pages.clients_accounts.accounts.accounts_wizard import AccountsWizard
from test_framework.web_admin_core.pages.clients_accounts.accounts.accounts_routes_subwizard import \
    AccountsRoutesSubWizard
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T3499(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.id = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.ext_id_client = self.id + "1"
        self.acc_route_name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.client_id_source = self.data_set.get_client_id_source("client_id_source_1")
        self.route = self.data_set.get_route("route_1")

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        side_menu.open_accounts_page()

        main_page = AccountsPage(self.web_driver_container)
        main_page.click_new_button()
        time.sleep(2)
        wizard = AccountsWizard(self.web_driver_container)
        wizard.set_id(self.id)
        wizard.set_ext_id_client(self.ext_id_client)
        wizard.set_client_id_source(self.client_id_source)

        routes_tab = AccountsRoutesSubWizard(self.web_driver_container)
        routes_tab.click_on_plus_button()
        time.sleep(2)
        routes_tab.set_route_account_name(self.acc_route_name)
        routes_tab.set_route(self.route)
        routes_tab.click_on_checkmark_button()

        wizard.click_save_button()
        time.sleep(2)

    def test_context(self):
        try:
            self.precondition()

            main_page = AccountsPage(self.web_driver_container)

            main_page.set_id(self.id)
            time.sleep(2)
            self.verify("Account was found by Name", self.id, main_page.get_id_grid_value())

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
