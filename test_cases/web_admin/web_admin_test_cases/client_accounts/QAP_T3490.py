import random
import string
import sys
import time
import traceback

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.clients_accounts.clients.clients_page import ClientsPage
from test_framework.web_admin_core.pages.clients_accounts.clients.clients_wizard import ClientsWizard
from test_framework.web_admin_core.pages.clients_accounts.clients.clients_values_sub_wizard import \
    ClientsValuesSubWizard
from test_framework.web_admin_core.pages.clients_accounts.clients.clients_assignments_sub_wizard import \
    ClientsAssignmentsSubWizard
from test_framework.web_admin_core.pages.clients_accounts.clients.clients_managements_sub_wizard import \
    ClientsManagementsSubWizard
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T3490(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.id = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.ext_id_client = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.disclose_exec = self.data_set.get_disclose_exec("disclose_exec_1")
        self.desk = self.data_set.get_desk("desk_3")
        self.middle_office_desk = "Quod Desk"

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        side_menu.open_clients_page()

        page = ClientsPage(self.web_driver_container)
        page.click_on_new()

        time.sleep(2)
        wizard_values = ClientsValuesSubWizard(self.web_driver_container)
        wizard_values.set_id(self.id)
        wizard_values.set_name(self.name)
        wizard_values.set_disclose_exec(self.disclose_exec)
        wizard_values.set_ext_id_client(self.ext_id_client)

        wizard_assignments = ClientsAssignmentsSubWizard(self.web_driver_container)
        wizard_assignments.set_desk(self.desk)

        wizard_managements = ClientsManagementsSubWizard(self.web_driver_container)
        wizard_managements.set_middle_office_desk(self.middle_office_desk)

        wizard_page = ClientsWizard(self.web_driver_container)
        wizard_page.click_on_save_changes()
        time.sleep(2)

    def test_context(self):
        try:
            self.precondition()

            page = ClientsPage(self.web_driver_container)
            page.set_name(self.name)
            time.sleep(2)
            self.verify("Created account found", self.name, page.get_client_name())

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
