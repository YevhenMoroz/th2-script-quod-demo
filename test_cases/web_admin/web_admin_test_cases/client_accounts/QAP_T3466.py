import sys
import time
import traceback
import random
import string

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.clients_accounts.clients.clients_page import ClientsPage
from test_framework.web_admin_core.pages.clients_accounts.clients.clients_values_sub_wizard import ClientsValuesSubWizard
from test_framework.web_admin_core.pages.clients_accounts.clients.clients_wizard import ClientsWizard
from test_framework.web_admin_core.pages.clients_accounts.clients.clients_assignments_sub_wizard \
    import ClientsAssignmentsSubWizard
from test_framework.web_admin_core.pages.clients_accounts.clients.clietns_venues_sub_wizard import ClientsVenuesSubWizard
from test_framework.web_admin_core.pages.clients_accounts.clients.clients_routes_sub_wizard import ClientsRoutesSubWizard
from test_framework.web_admin_core.pages.general.common.common_page import CommonPage

from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T3466(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None,
                 db_manager=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.db_manager = db_manager
        self.id = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.name = self.__class__.__name__
        self.ext_id_client = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.disclose_exec = 'Manual'
        self.desk = self.data_set.get_desk("desk_1")

        self.venues = [self.data_set.get_venue_by_name('venue_1'), self.data_set.get_venue_by_name('venue_2')]
        self.venue_client_name = [''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6)) for _ in range(2)]
        self.venue_client_account_group_name = [f'VName_{_}' for _ in range(2)]

        self.route = self.data_set.get_route('route_1')
        self.routes_client_name = 'RName_1'

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        values_tab = ClientsValuesSubWizard(self.web_driver_container)
        assignments_tab = ClientsAssignmentsSubWizard(self.web_driver_container)
        venues_tab = ClientsVenuesSubWizard(self.web_driver_container)
        routes_tab = ClientsRoutesSubWizard(self.web_driver_container)
        wizard = ClientsWizard(self.web_driver_container)
        side_menu = SideMenu(self.web_driver_container)
        main_page = ClientsPage(self.web_driver_container)
        common_act = CommonPage(self.web_driver_container)

        login_page.login_to_web_admin(self.login, self.password)
        side_menu.open_clients_page()
        if main_page.is_client_lookup_displayed_in_header():
            main_page.load_client_from_global_filter(self.name)
            time.sleep(1)
        main_page.set_name(self.name)
        time.sleep(1)
        if not main_page.is_searched_client_found(self.name):
            main_page.click_on_new()
            values_tab.set_id(self.id)
            values_tab.set_name(self.name)
            values_tab.set_ext_id_client(self.ext_id_client)
            values_tab.set_disclose_exec(self.disclose_exec)
            assignments_tab.set_desk(self.desk)
            venues_tab.click_on_plus()
            venues_tab.set_venue(self.venues[0])
            venues_tab.set_venue_client_name(self.venue_client_name[0])
            venues_tab.set_venue_client_account(self.venue_client_account_group_name[0])
            venues_tab.click_on_checkmark()
            venues_tab.click_on_plus()
            venues_tab.set_venue(self.venues[1])
            venues_tab.set_venue_client_name(self.venue_client_name[1])
            venues_tab.set_venue_client_account(self.venue_client_account_group_name[1])
            venues_tab.click_on_checkmark()
            routes_tab.click_on_plus()
            routes_tab.set_route(self.route)
            routes_tab.set_route_client_name(self.routes_client_name)
            routes_tab.click_on_checkmark()
            wizard.click_on_save_changes()
            time.sleep(2)
        main_page.set_name(self.name)
        time.sleep(1)

        self.db_manager.my_db.execute(
            "UPDATE QUODSETTINGS SET settingvalue = '10' WHERE settingkey = 'WEB_ADMIN_CACHE_THRESHOLD'")
        common_act.refresh_page(True)
        time.sleep(2)

    def test_context(self):
        common_act = CommonPage(self.web_driver_container)
        main_page = ClientsPage(self.web_driver_container)

        try:
            self.precondition()

            main_page.load_client_from_global_filter(self.name)
            time.sleep(1)
            main_page.set_name(self.name)
            time.sleep(1)
            expected_result = [self.venue_client_account_group_name, self.routes_client_name]
            actual_result = [main_page.get_venue_names().split(','), main_page.get_route_names()]
            self.verify("Venue Names and Route Names are displayed on the main page",
                        expected_result, actual_result)

            self.db_manager.my_db.execute(
                "UPDATE QUODSETTINGS SET settingvalue = '500' WHERE settingkey = 'WEB_ADMIN_CACHE_THRESHOLD'")
            common_act.refresh_page(True)
            time.sleep(2)
            main_page.set_name(self.name)
            time.sleep(1)
            expected_result = [self.venue_client_account_group_name, self.routes_client_name]
            actual_result = [main_page.get_venue_names().split(','), main_page.get_route_names()]
            self.verify("Venue Names and Route Names are displayed on the main page",
                        expected_result, actual_result)

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)

        finally:
            self.db_manager.my_db.execute(
                "UPDATE QUODSETTINGS SET settingvalue = '500' WHERE settingkey = 'WEB_ADMIN_CACHE_THRESHOLD'")
