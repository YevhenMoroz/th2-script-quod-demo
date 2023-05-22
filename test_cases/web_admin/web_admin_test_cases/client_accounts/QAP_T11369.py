import sys
import time
import traceback
import random
import string

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.general.common.common_page import CommonPage
from test_framework.web_admin_core.pages.clients_accounts.clients.clients_values_sub_wizard import \
    ClientsValuesSubWizard
from test_framework.web_admin_core.pages.clients_accounts.clients.clients_assignments_sub_wizard \
    import ClientsAssignmentsSubWizard
from test_framework.web_admin_core.pages.clients_accounts.clients.clients_instr_types_sub_wizard \
    import ClientsInstrTypesSubWizard
from test_framework.web_admin_core.pages.clients_accounts.clients.clietns_venues_sub_wizard \
    import ClientsVenuesSubWizard
from test_framework.web_admin_core.pages.clients_accounts.clients.clients_routes_sub_wizard \
    import ClientsRoutesSubWizard
from test_framework.web_admin_core.pages.clients_accounts.clients.clients_trade_confirm_sub_wizard \
    import ClientsTradeConfirmSubWizard
from test_framework.web_admin_core.pages.clients_accounts.clients.clients_page import ClientsPage
from test_framework.web_admin_core.pages.clients_accounts.clients.clients_wizard import ClientsWizard

from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T11369(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None,
                 db_manager=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.db_manager = db_manager

        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.name = self.__class__.__name__
        self.id = self.__class__.__name__
        self.ext_id_client = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.disclose_exec = 'Manual'
        self.allocation_matching_service = 'External'
        self.external_allocation_matching_service = 'CTM'
        self.desk = self.data_set.get_desk("desk_1")
        self.instr_type = 'Bond'
        self.venue = self.data_set.get_venue_by_name("venue_1")
        self.venue_client_name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.route = self.data_set.get_route("route_1")
        self.route_client_name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.email_address = '2@2'
        self.recipient_type = 'BCC'

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        wizard = ClientsWizard(self.web_driver_container)
        side_menu = SideMenu(self.web_driver_container)
        page = ClientsPage(self.web_driver_container)
        values_tab = ClientsValuesSubWizard(self.web_driver_container)
        assignments_tab = ClientsAssignmentsSubWizard(self.web_driver_container)
        instr_type_tab = ClientsInstrTypesSubWizard(self.web_driver_container)
        venues_tab = ClientsVenuesSubWizard(self.web_driver_container)
        route_tab = ClientsRoutesSubWizard(self.web_driver_container)
        trade_confirm = ClientsTradeConfirmSubWizard(self.web_driver_container)

        login_page.login_to_web_admin(self.login, self.password)
        side_menu.open_clients_page()
        page.set_name(self.name)
        time.sleep(1)
        if not page.is_searched_client_found(self.name):
            page.click_on_new()
            values_tab.set_id(self.id)
            values_tab.set_name(self.name)
            values_tab.set_ext_id_client(self.ext_id_client)
            values_tab.set_disclose_exec(self.disclose_exec)
            values_tab.set_allocation_matching_service(self.allocation_matching_service)
            values_tab.set_external_allocation_matching_service(self.external_allocation_matching_service)
            assignments_tab.set_desk(self.desk)
            instr_type_tab.click_on_plus()
            instr_type_tab.set_instr_type(self.instr_type)
            instr_type_tab.click_on_checkmark()
            venues_tab.click_on_plus()
            venues_tab.set_venue(self.venue)
            venues_tab.set_venue_client_name(self.venue_client_name)
            venues_tab.click_on_checkmark()
            route_tab.click_on_plus()
            route_tab.set_route(self.route)
            route_tab.set_route_client_name(self.route_client_name)
            route_tab.click_on_checkmark()
            trade_confirm.click_on_plus()
            trade_confirm.set_email_address(self.email_address)
            trade_confirm.set_recipient_types(self.recipient_type)
            trade_confirm.click_on_checkmark()
            wizard.click_on_save_changes()

    def test_context(self):
        wizard = ClientsWizard(self.web_driver_container)
        page = ClientsPage(self.web_driver_container)
        values_tab = ClientsValuesSubWizard(self.web_driver_container)
        assignments_tab = ClientsAssignmentsSubWizard(self.web_driver_container)
        instr_type_tab = ClientsInstrTypesSubWizard(self.web_driver_container)
        venues_tab = ClientsVenuesSubWizard(self.web_driver_container)
        route_tab = ClientsRoutesSubWizard(self.web_driver_container)
        trade_confirm = ClientsTradeConfirmSubWizard(self.web_driver_container)
        common_act = CommonPage(self.web_driver_container)

        try:
            self.precondition()

            page.set_name(self.name)
            time.sleep(1)
            page.click_on_enable_disable()
            time.sleep(2)
            page.click_on_more_actions()
            page.click_on_edit()

            expected_result = [self.external_allocation_matching_service, self.desk, self.instr_type, self.venue,
                               self.route, self.email_address]
            actual_result = [values_tab.get_external_allocation_matching_service(), assignments_tab.get_desk(),
                             instr_type_tab.get_instr_type_in_table(), venues_tab.get_venue_in_table(),
                             route_tab.get_route_in_table(), trade_confirm.get_email_address_in_table()]
            self.verify("Data for disabled client still displayed", expected_result, actual_result)
            common_act.click_on_info_error_message_pop_up()
            wizard.click_on_close()
            page.set_name(self.name)
            time.sleep(1)
            page.click_on_enable_disable()
            time.sleep(2)
            page.click_on_more_actions()
            page.click_on_edit()

            expected_result = [self.external_allocation_matching_service, self.desk, self.instr_type, self.venue,
                               self.route, self.email_address]
            actual_result = [values_tab.get_external_allocation_matching_service(), assignments_tab.get_desk(),
                             instr_type_tab.get_instr_type_in_table(), venues_tab.get_venue_in_table(),
                             route_tab.get_route_in_table(), trade_confirm.get_email_address_in_table()]
            self.verify("Data for enabled client still displayed", expected_result, actual_result)

        except Exception:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            errors = f'"{[traceback.extract_tb(exc_traceback, limit=4)]}"'.replace("\\", "/")
            basic_custom_actions.create_event(f"FAILED", self.test_case_id, status='FAILED',
                                              body="[{\"type\": \"message\", \"data\":"+f"{errors}"+"}]")
            traceback.print_tb(exc_traceback, limit=3, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)

        finally:
            self.db_manager.my_db.execute(f"UPDATE ACCOUNTGROUP SET ALIVE = 'Y' WHERE ACCOUNTGROUPID = '{self.id}'")
            self.db_manager.my_db.execute(f"UPDATE VENUEACCOUNTGROUP SET ALIVE = 'Y' WHERE ACCOUNTGROUPID = '{self.id}'")
            self.db_manager.my_db.execute(f"UPDATE ROUTEACCOUNTGROUP SET ALIVE = 'Y' WHERE ACCOUNTGROUPID = '{self.id}'")
            self.db_manager.my_db.execute(f"UPDATE ACTGRPINSTRTYPE SET ALIVE = 'Y' WHERE ACCOUNTGROUPID = '{self.id}'")
            self.db_manager.my_db.execute(f"UPDATE ACTGRPEXTCONFIRMSERVICE SET ALIVE = 'Y' WHERE ACCOUNTGROUPID = '{self.id}'")
