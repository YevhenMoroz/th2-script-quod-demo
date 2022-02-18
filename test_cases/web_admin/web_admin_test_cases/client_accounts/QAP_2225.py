import random
import string
import sys
import time
import traceback

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.client_accounts.clients.clients_assignments_sub_wizard import \
    ClientsAssignmentsSubWizard
from test_framework.web_admin_core.pages.client_accounts.clients.clients_page import ClientsPage
from test_framework.web_admin_core.pages.client_accounts.clients.clients_values_sub_wizard import \
    ClientsValuesSubWizard
from test_framework.web_admin_core.pages.client_accounts.clients.clients_wizard import ClientsWizard
from test_framework.web_admin_core.pages.client_accounts.clients.clietns_venues_sub_wizard import \
    ClientsVenuesSubWizard
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_2225(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id)
        self.login = "adm03"
        self.password = "adm03"
        self.id = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.disclose_exec = 'Manual'
        self.venue = "AMEX"
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
        venues_sub_wizard.click_on_plus()
        time.sleep(1)
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
        venues_sub_wizard.click_on_delete()

    def test_context(self):
        main_page = ClientsPage(self.web_driver_container)
        wizard = ClientsWizard(self.web_driver_container)
        venues_sub_wizard = ClientsVenuesSubWizard(self.web_driver_container)
        try:
            self.precondition()

            self.verify("PDF file don't contains venue", False,
                        wizard.click_download_pdf_entity_button_and_check_pdf(self.venue))
            self.verify("PDF file don't contains venue client", False,
                        wizard.click_download_pdf_entity_button_and_check_pdf(self.venue_client_name))
            self.verify("Is PDF  don't contains venue client account group name", False,
                        wizard.click_download_pdf_entity_button_and_check_pdf(self.venue_client_account_group_name))
            time.sleep(2)
            wizard.click_on_save_changes()
            time.sleep(2)
            main_page.set_name(self.name)
            time.sleep(2)
            main_page.click_on_more_actions()
            time.sleep(2)
            main_page.click_on_edit()
            time.sleep(2)
            venues_sub_wizard.set_venue_client_name(self.venue_client_name)
            time.sleep(2)

            self.verify("Venue is delete", False,
                        venues_sub_wizard.is_venue_present())


        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
