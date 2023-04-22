import random
import string
import sys
import time
import traceback

from custom import basic_custom_actions

from test_framework.web_admin_core.pages.clients_accounts.clients.clients_page import ClientsPage
from test_framework.web_admin_core.pages.clients_accounts.clients.clients_values_sub_wizard import \
    ClientsValuesSubWizard
from test_framework.web_admin_core.pages.clients_accounts.clients.clients_assignments_sub_wizard import \
    ClientsAssignmentsSubWizard
from test_framework.web_admin_core.pages.clients_accounts.clients.clients_wizard import ClientsWizard
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T3900(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.id = 'QAP_T3900'
        self.name = 'QAP_T3900'
        self.ext_id_client = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.disclose_exec = self.data_set.get_disclose_exec("disclose_exec_1")
        self.block_approval = ['Manual', 'Automatic']
        self.desk = self.data_set.get_desk("desk_1")

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        time.sleep(2)
        side_menu = SideMenu(self.web_driver_container)
        side_menu.open_clients_page()

        main_page = ClientsPage(self.web_driver_container)
        main_page.set_name(self.name)
        time.sleep(1)
        if not main_page.is_searched_client_found(self.name):
            main_page.click_on_new()
            values_tab = ClientsValuesSubWizard(self.web_driver_container)
            values_tab.set_id(self.id)
            values_tab.set_name(self.name)
            values_tab.set_ext_id_client(self.ext_id_client)
            values_tab.set_disclose_exec(self.disclose_exec)
            assignments_tab = ClientsAssignmentsSubWizard(self.web_driver_container)
            assignments_tab.set_desk(self.desk)
            wizard = ClientsWizard(self.web_driver_container)
            wizard.click_on_save_changes()
            main_page.set_name(self.name)
            time.sleep(1)

    def test_context(self):
        try:
            self.precondition()

            main_page = ClientsPage(self.web_driver_container)
            main_page.click_on_more_actions()
            main_page.click_on_edit()
            values_tab = ClientsValuesSubWizard(self.web_driver_container)
            values_tab.set_block_approval(self.block_approval[0])
            wizard = ClientsWizard(self.web_driver_container)
            wizard.click_on_save_changes()
            main_page.set_name(self.name)
            time.sleep(1)
            main_page.click_on_more_actions()

            self.verify("PDF file contains Block Approval = Manual", True,
                        main_page.click_download_pdf_entity_button_and_check_pdf(self.block_approval[0]))

            main_page.click_on_more_actions()
            main_page.click_on_edit()

            self.verify("Block Approval has been save correct", self.block_approval[0], values_tab.get_block_approval())

            values_tab.set_block_approval(self.block_approval[1])
            wizard.click_on_save_changes()
            main_page.set_name(self.name)
            time.sleep(1)
            main_page.click_on_more_actions()
            main_page.click_on_edit()

            self.verify("Block Approval has been save correct", self.block_approval[1], values_tab.get_block_approval())

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
