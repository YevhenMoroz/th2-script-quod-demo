import sys
import time
import random
import string
import traceback

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.client_accounts.clients.clients_page import ClientsPage
from test_framework.web_admin_core.pages.client_accounts.clients.clients_values_sub_wizard import \
    ClientsValuesSubWizard
from test_framework.web_admin_core.pages.client_accounts.clients.clients_assignments_sub_wizard import \
    ClientsAssignmentsSubWizard
from test_framework.web_admin_core.pages.client_accounts.clients.clients_external_sources_sub_wizard import \
    ClientsExternalSourcesSubWizard
from test_framework.web_admin_core.pages.client_accounts.clients.clients_policies_sub_wizard \
    import ClientsPoliciesSubWizard
from test_framework.web_admin_core.pages.client_accounts.clients.clients_managements_sub_wizard \
    import ClientsManagementsSubWizard
from test_framework.web_admin_core.pages.client_accounts.clients.clients_pos_maintance_sub_wizard \
    import ClientsPosMaintenanceSubWizard
from test_framework.web_admin_core.pages.client_accounts.clients.clients_instr_types_sub_wizard \
    import ClientsInstrTypesSubWizard
from test_framework.web_admin_core.pages.client_accounts.clients.clietns_venues_sub_wizard \
    import ClientsVenuesSubWizard
from test_framework.web_admin_core.pages.client_accounts.clients.clients_routes_sub_wizard \
    import ClientsRoutesSubWizard
from test_framework.web_admin_core.pages.client_accounts.clients.clients_trade_confirm_sub_wizard \
    import ClientsTradeConfirmSubWizard
from test_framework.web_admin_core.pages.client_accounts.clients.clients_wizard import ClientsWizard
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T3407(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.client_name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))

        self.id = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.ext_id_client = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.description = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.disclose_exec = 'Manual'
        self.confirmation_service = "Internal"
        self.desk = self.data_set.get_desk("desk_1")
        self.fix_order_recipient_desk = self.data_set.get_desk("desk_2")
        self.bic = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.bo_field_1 = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.default_execution_strategy = data_set.get_default_execution_strategy("default_execution_strategy_1")
        self.cash_maintenance = 'NotMaintained'
        self.instr_type = 'Bond'
        self.venue = self.data_set.get_venue_by_name("venue_1")
        self.venue_client_name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.route = self.data_set.get_route("route_1")
        self.route_client_name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.trade_confirm_preference = 'Both'
        self.email = "test@test.com"
        self.recipient_types = 'To'

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        time.sleep(2)
        side_menu = SideMenu(self.web_driver_container)
        side_menu.open_clients_page()
        time.sleep(2)
        main_page = ClientsPage(self.web_driver_container)
        main_page.click_on_new()
        time.sleep(2)

        values_tab = ClientsValuesSubWizard(self.web_driver_container)
        values_tab.set_id(self.id)
        values_tab.set_name(self.client_name)
        values_tab.set_ext_id_client(self.ext_id_client)
        values_tab.set_description(self.description)
        values_tab.set_disclose_exec(self.disclose_exec)
        values_tab.set_confirmation_service(self.confirmation_service)

        assignments_tab = ClientsAssignmentsSubWizard(self.web_driver_container)
        assignments_tab.set_desk(self.desk)

        external_source_tab = ClientsExternalSourcesSubWizard(self.web_driver_container)
        external_source_tab.set_bic_venue_act_grp_name(self.bic)
        external_source_tab.set_bo_field_1(self.bo_field_1)

        managements_tab = ClientsManagementsSubWizard(self.web_driver_container)
        managements_tab.set_fix_order_recipient_desk(self.fix_order_recipient_desk)

        policies_tab = ClientsPoliciesSubWizard(self.web_driver_container)
        policies_tab.set_default_execution_strategies(self.default_execution_strategy)

        pos_maintenance_tab = ClientsPosMaintenanceSubWizard(self.web_driver_container)
        pos_maintenance_tab.set_cash_maintenance(self.cash_maintenance)
        pos_maintenance_tab.click_on_pnl_maintenance()

        instr_types_tab = ClientsInstrTypesSubWizard(self.web_driver_container)
        instr_types_tab.click_on_plus()
        instr_types_tab.set_instr_type(self.instr_type)
        instr_types_tab.click_on_checkmark()

        venues_tab = ClientsVenuesSubWizard(self.web_driver_container)
        venues_tab.click_on_plus()
        venues_tab.set_venue(self.venue)
        venues_tab.set_venue_client_name(self.venue_client_name)
        venues_tab.click_on_checkmark()

        routes_tab = ClientsRoutesSubWizard(self.web_driver_container)
        routes_tab.click_on_plus()
        routes_tab.set_route(self.route)
        routes_tab.set_route_client_name(self.route_client_name)
        routes_tab.click_on_checkmark()

        trade_confirm_tab = ClientsTradeConfirmSubWizard(self.web_driver_container)
        trade_confirm_tab.set_trade_confirm_preference(self.trade_confirm_preference)
        trade_confirm_tab.click_on_plus()
        trade_confirm_tab.set_email_address(self.email)
        trade_confirm_tab.set_recipient_types(self.recipient_types)
        trade_confirm_tab.click_on_checkmark()

        wizard = ClientsWizard(self.web_driver_container)
        wizard.click_on_save_changes()
        time.sleep(2)
        main_page.set_name(self.client_name)
        time.sleep(1)

        main_page.click_on_more_actions()
        time.sleep(1)
        main_page.click_on_clone()
        time.sleep(2)

    def test_context(self):
        values_tab = ClientsValuesSubWizard(self.web_driver_container)
        assignments_tab = ClientsAssignmentsSubWizard(self.web_driver_container)
        external_source_tab = ClientsExternalSourcesSubWizard(self.web_driver_container)
        managements_tab = ClientsManagementsSubWizard(self.web_driver_container)
        policies_tab = ClientsPoliciesSubWizard(self.web_driver_container)
        pos_maintenance_tab = ClientsPosMaintenanceSubWizard(self.web_driver_container)
        instr_types_tab = ClientsInstrTypesSubWizard(self.web_driver_container)
        venues_tab = ClientsVenuesSubWizard(self.web_driver_container)
        routes_tab = ClientsRoutesSubWizard(self.web_driver_container)
        trade_confirm_tab = ClientsTradeConfirmSubWizard(self.web_driver_container)

        try:
            self.precondition()

            actual_result = [values_tab.get_name(),
                             values_tab.get_description(),
                             values_tab.get_disclose_exec(),
                             values_tab.get_confirmation_service(),
                             assignments_tab.get_desk(),
                             external_source_tab.get_bic_venue_act_grp_name(),
                             external_source_tab.get_bo_field_1(),
                             managements_tab.get_fix_order_recipient_desk(),
                             policies_tab.get_default_execution_strategies(),
                             pos_maintenance_tab.get_cash_maintenance(),
                             pos_maintenance_tab.is_pnl_maintenance_selected(),
                             instr_types_tab.click_on_edit(),
                             instr_types_tab.get_instr_type(),
                             venues_tab.click_on_edit(),
                             venues_tab.get_venue(),
                             venues_tab.get_venue_client_name(),
                             routes_tab.click_on_edit(),
                             routes_tab.get_route(),
                             routes_tab.get_route_client_name(),
                             trade_confirm_tab.get_trade_confirm_preference(),
                             trade_confirm_tab.click_on_edit(),
                             trade_confirm_tab.get_email_address(),
                             trade_confirm_tab.get_recipient_types()]
            while None in actual_result:
                actual_result.pop(actual_result.index(None))

            excepted_result = [self.client_name,
                               self.description,
                               self.disclose_exec,
                               self.confirmation_service,
                               self.desk,
                               self.bic,
                               self.bo_field_1,
                               self.fix_order_recipient_desk,
                               self.default_execution_strategy,
                               self.cash_maintenance,
                               True,
                               self.instr_type,
                               self.venue,
                               self.venue_client_name,
                               self.route,
                               self.route_client_name,
                               self.trade_confirm_preference,
                               self.email,
                               self.recipient_types]

            self.verify("All data displayed after cloning", actual_result, excepted_result)

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
