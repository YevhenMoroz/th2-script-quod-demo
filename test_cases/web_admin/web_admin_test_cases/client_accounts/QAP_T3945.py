import random
import string
import sys
import time
import traceback

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.clients_accounts.clients.clients_assignments_sub_wizard import \
    ClientsAssignmentsSubWizard
from test_framework.web_admin_core.pages.clients_accounts.clients.clients_page import ClientsPage
from test_framework.web_admin_core.pages.clients_accounts.clients.clients_values_sub_wizard import \
    ClientsValuesSubWizard
from test_framework.web_admin_core.pages.clients_accounts.clients.clients_wizard import ClientsWizard
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T3945(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.id = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.ext_id_client = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.disclose_exec = self.data_set.get_disclose_exec("disclose_exec_1")
        self.clearing_account_type = [
            self.data_set.get_clearing_account_type("clearing_account_type_1"),
            self.data_set.get_clearing_account_type("clearing_account_type_2"),
            self.data_set.get_clearing_account_type("clearing_account_type_3")]
        self.desk = self.data_set.get_desk("desk_3")

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        time.sleep(2)
        side_menu.open_clients_page()
        main_page = ClientsPage(self.web_driver_container)
        values_sub_wizard = ClientsValuesSubWizard(self.web_driver_container)
        wizard = ClientsWizard(self.web_driver_container)
        time.sleep(2)
        main_page.click_on_new()
        time.sleep(2)
        values_sub_wizard.set_id(self.id)
        values_sub_wizard.set_name(self.name)
        values_sub_wizard.set_ext_id_client(self.ext_id_client)
        values_sub_wizard.set_disclose_exec(self.disclose_exec)
        assignments_sub_wizard = ClientsAssignmentsSubWizard(self.web_driver_container)
        assignments_sub_wizard.set_desk(self.desk)
        wizard.click_on_save_changes()
        time.sleep(2)
        main_page.set_name(self.name)
        time.sleep(1)
        main_page.click_on_more_actions()
        time.sleep(1)
        main_page.click_on_edit()
        time.sleep(2)

    def test_context(self):
        values_sub_wizard = ClientsValuesSubWizard(self.web_driver_container)
        main_page = ClientsPage(self.web_driver_container)
        wizard = ClientsWizard(self.web_driver_container)
        try:
            self.precondition()

            for i in self.clearing_account_type:
                values_sub_wizard.set_clearing_account_type(i)
                time.sleep(1)
            self.verify(f"Drop-down list contains {self.clearing_account_type}", True, True)

            wizard.click_on_save_changes()
            time.sleep(2)
            main_page.set_name(self.name)
            time.sleep(2)
            self.verify("Is entity saved correctly", self.clearing_account_type[-1],
                        main_page.get_clearing_account_type())

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
