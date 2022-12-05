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
from test_framework.web_admin_core.pages.clients_accounts.clients.clietns_venues_sub_wizard import \
    ClientsVenuesSubWizard
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T8813(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.id = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.disclose_exec = self.data_set.get_disclose_exec("disclose_exec_1")
        self.ext_id_client = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))

        self.venues = list
        self.venue_client_name = [''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
                                  for _ in range(3)]
        self.venue_client_account_group_name = [''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
                                                for _ in range(3)]

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)

        side_menu = SideMenu(self.web_driver_container)
        side_menu.open_clients_page()

        main_page = ClientsPage(self.web_driver_container)
        values_sub_wizard = ClientsValuesSubWizard(self.web_driver_container)
        wizard = ClientsWizard(self.web_driver_container)
        venues_sub_wizard = ClientsVenuesSubWizard(self.web_driver_container)

        main_page.click_on_new()
        values_sub_wizard.set_id(self.id)
        values_sub_wizard.set_name(self.name)
        values_sub_wizard.set_disclose_exec(self.disclose_exec)
        values_sub_wizard.set_ext_id_client(self.ext_id_client)

        self.venues = venues_sub_wizard.get_all_venue_from_drop_menu()
        venues_sub_wizard.create_new_venue(self.venues[0], self.venue_client_name[0], self.venue_client_account_group_name[0])
        venues_sub_wizard.create_new_venue(self.venues[1], self.venue_client_name[1], self.venue_client_account_group_name[1])
        venues_sub_wizard.create_new_venue(self.venues[2], self.venue_client_name[2], self.venue_client_account_group_name[2])
        wizard.click_on_save_changes()

    def test_context(self):
        wizard = ClientsWizard(self.web_driver_container)
        main_page = ClientsPage(self.web_driver_container)
        venues_sub_wizard = ClientsVenuesSubWizard(self.web_driver_container)
        try:
            self.precondition()

            main_page.set_name(self.name)
            time.sleep(1)
            main_page.click_on_more_actions()
            main_page.click_on_edit()

            venue_to_delete = random.choice(self.venue_client_name)
            venues_sub_wizard.set_venue_client_name_filter(venue_to_delete)
            time.sleep(1)
            venues_sub_wizard.click_on_delete()
            wizard.click_on_save_changes()

            main_page.set_name(self.name)
            time.sleep(1)
            main_page.click_on_more_actions()
            main_page.click_on_edit()

            venues_sub_wizard.set_venue_client_name_filter(venue_to_delete)
            time.sleep(1)
            self.verify("Venue has been delete", False, venues_sub_wizard.is_venue_present())

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
