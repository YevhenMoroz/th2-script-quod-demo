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
from test_cases.web_admin.web_admin_core.pages.client_accounts.clients.clietns_venues_sub_wizard import \
    ClientsVenuesSubWizard
from test_cases.web_admin.web_admin_core.pages.login.login_page import LoginPage
from test_cases.web_admin.web_admin_core.pages.root.side_menu import SideMenu
from test_cases.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_2224(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id)
        self.login = "adm03"
        self.password = "adm03"
        self.id = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.disclose_exec = 'Manual'
        self.venue = "AMEX"
        self.new_venue = "ADX"
        self.venue_client_name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.venue_client_account_group_name = "48934"
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
        venues_sub_wizard = ClientsVenuesSubWizard(self.web_driver_container)
        time.sleep(2)
        main_page.click_on_new()
        time.sleep(2)
        values_sub_wizard.set_id(self.id)
        values_sub_wizard.set_name(self.name)
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
        venues_sub_wizard.click_on_plus()
        venues_sub_wizard.set_venue(self.venue)
        venues_sub_wizard.set_venue_client_name(self.venue_client_name)
        venues_sub_wizard.set_venue_client_account(self.venue_client_account_group_name)
        venues_sub_wizard.click_on_checkmark()
        wizard.click_on_save_changes()
        time.sleep(2)
        main_page.set_name(self.name)
        time.sleep(2)
        main_page.click_on_more_actions()
        time.sleep(2)
        main_page.click_on_edit()
        time.sleep(2)
        venues_sub_wizard.click_on_edit()
        venues_sub_wizard.set_venue(self.new_venue)
        venues_sub_wizard.click_on_checkmark()

    def test_context(self):
        try:
            self.precondition()
            wizard = ClientsWizard(self.web_driver_container)
            main_page = ClientsPage(self.web_driver_container)
            expected_pdf_content = [self.name,
                                    self.disclose_exec,
                                    self.new_venue,
                                    self.venue_client_name,
                                    self.venue_client_account_group_name]

            self.verify("Is PDF contains correctly value", True,
                        wizard.click_download_pdf_entity_button_and_check_pdf(expected_pdf_content))
            wizard.click_on_save_changes()
            time.sleep(2)
            main_page.set_name(self.name)
            time.sleep(2)
            try:
                main_page.click_on_more_actions()
                self.verify("Entity created correctly", True, True)

            except Exception as e:
                self.verify("Entity not created!!!ERROR!!!", True, e.__class__.__name__)

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
