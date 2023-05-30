import random
import string
import sys
import time
import traceback

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.clients_accounts.accounts.accounts_page import AccountsPage
from test_framework.web_admin_core.pages.clients_accounts.accounts.accounts_routes_subwizard import \
    AccountsRoutesSubWizard
from test_framework.web_admin_core.pages.clients_accounts.accounts.accounts_wizard import AccountsWizard
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T10959(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.id = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.ext_id_client = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.client_id_source = self.data_set.get_client_id_source("client_id_source_1")
        self.route_name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.routes = [self.data_set.get_route("route_1"), self.data_set.get_route("route_2")]

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        side_menu = SideMenu(self.web_driver_container)

        login_page.login_to_web_admin(self.login, self.password)
        side_menu.open_accounts_page()

    def test_context(self):
        main_page = AccountsPage(self.web_driver_container)
        values_tab = AccountsWizard(self.web_driver_container)
        wizard = AccountsWizard(self.web_driver_container)
        routes_tab = AccountsRoutesSubWizard(self.web_driver_container)

        try:
            self.precondition()

            main_page.click_new_button()
            values_tab.set_id(self.id)
            values_tab.set_ext_id_client(self.ext_id_client)
            values_tab.set_client_id_source(self.client_id_source)

            for i in range(len(self.routes)):
                routes_tab.click_on_plus_button()
                routes_tab.set_route_account_name(self.route_name)
                routes_tab.set_route(self.routes[i])
                routes_tab.click_on_checkmark_button()

            wizard.click_save_button()
            main_page.set_id(self.id)
            time.sleep(1)
            main_page.click_more_actions_button()
            main_page.click_edit_entity_button()

            expected_result = [[self.route_name for _ in range(2)], sorted(self.routes)]
            actual_result = [routes_tab.get_all_route_account_names_in_table(),
                             sorted(routes_tab.get_all_routes_in_table())]

            self.verify("New Account has been saved with same RouteAccountName", expected_result, actual_result)

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
