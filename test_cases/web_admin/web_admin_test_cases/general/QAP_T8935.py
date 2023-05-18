import sys
import time
import traceback

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.general.common.common_page import CommonPage
from test_framework.web_admin_core.pages.users.users.users_page import UsersPage
from test_framework.web_admin_core.pages.users.users.users_wizard import UsersWizard
from test_framework.web_admin_core.pages.clients_accounts.clients.clients_page import ClientsPage
from test_framework.web_admin_core.pages.clients_accounts.clients.clients_wizard import ClientsWizard

from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T8935(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")

    def test_context(self):
        login_page = LoginPage(self.web_driver_container)
        side_menu = SideMenu(self.web_driver_container)
        users_page = UsersPage(self.web_driver_container)
        users_wizard = UsersWizard(self.web_driver_container)
        clients_page = ClientsPage(self.web_driver_container)
        clients_wizard = ClientsWizard(self.web_driver_container)
        common_act = CommonPage(self.web_driver_container)

        try:
            login_page.login_to_web_admin(self.login, self.password)
            side_menu.open_users_page()

            users_page.click_on_new_button()
            time.sleep(1)
            common_act.click_on_user_icon()
            common_act.click_on_logout()
            time.sleep(2)
            login_page.login_to_web_admin(self.login, self.password)
            time.sleep(1)

            self.verify("User create wizard opened after re-login", True, users_wizard.is_wizard_open())

            side_menu.open_clients_page()
            time.sleep(1)
            self.verify("Confirmation pop-up not appears", False, common_act.is_confirmation_pop_displayed())

            clients_page.click_on_more_actions()
            clients_page.click_on_edit()
            time.sleep(1)
            common_act.click_on_user_icon()
            common_act.click_on_logout()
            time.sleep(2)
            login_page.login_to_web_admin(self.login, self.password)
            time.sleep(1)

            self.verify("Clients edit wizard opened after re-login", True, clients_wizard.is_wizard_open())

            side_menu.open_clients_page()
            time.sleep(1)
            self.verify("Confirmation pop-up not appears", False, common_act.is_confirmation_pop_displayed())

            side_menu.open_users_page()
            time.sleep(1)
            self.verify("Confirmation pop-up not appears", False, common_act.is_confirmation_pop_displayed())

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
