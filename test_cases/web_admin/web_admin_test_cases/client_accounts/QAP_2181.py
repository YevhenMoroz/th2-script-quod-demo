import random
import string
import sys
import time
import traceback

from custom import basic_custom_actions
from test_cases.web_admin.web_admin_core.pages.client_accounts.clients.clients_assignments_sub_wizard import \
    ClientsAssignmentsSubWizard
from test_cases.web_admin.web_admin_core.pages.client_accounts.clients.clients_page import ClientsPage
from test_cases.web_admin.web_admin_core.pages.client_accounts.clients.clients_values_sub_wizard import \
    ClientsValuesSubWizard
from test_cases.web_admin.web_admin_core.pages.client_accounts.clients.clients_wizard import ClientsWizard
from test_cases.web_admin.web_admin_core.pages.login.login_page import LoginPage
from test_cases.web_admin.web_admin_core.pages.root.side_menu import SideMenu
from test_cases.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_2181(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id)
        self.login = "adm03"
        self.password = "adm03"
        self.id = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.disclose_exec = 'Manual'
        self.clearing_account_type = 'Retail'
        self.desk = "Quod Desk"

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
        time.sleep(2)
        values_sub_wizard.set_name(self.name)
        time.sleep(2)
        values_sub_wizard.set_disclose_exec(self.disclose_exec)
        time.sleep(1)
        assignments_sub_wizard = ClientsAssignmentsSubWizard(self.web_driver_container)
        assignments_sub_wizard.set_desk(self.desk)
        time.sleep(1)
        wizard.click_on_save_changes()
        time.sleep(2)
        main_page.set_name(self.name)
        time.sleep(2)
        main_page.click_on_more_actions()
        time.sleep(2)
        main_page.click_on_edit()
        time.sleep(2)
        values_sub_wizard.set_clearing_account_type(self.clearing_account_type)
        time.sleep(1)
        wizard.click_on_save_changes()

    def test_context(self):
        try:
            self.precondition()
            main_page = ClientsPage(self.web_driver_container)
            time.sleep(2)
            main_page.set_name(self.name)
            time.sleep(2)
            self.verify("Is entity saved correctly", self.clearing_account_type, main_page.get_clearing_account_type())

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
