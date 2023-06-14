import sys
import time
import traceback
import random
import string

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.clients_accounts.clients.clients_values_sub_wizard import \
    ClientsValuesSubWizard
from test_framework.web_admin_core.pages.clients_accounts.clients.clients_assignments_sub_wizard \
    import ClientsAssignmentsSubWizard
from test_framework.web_admin_core.pages.clients_accounts.clients.clients_external_sources_sub_wizard \
    import ClientsExternalSourcesSubWizard
from test_framework.web_admin_core.pages.clients_accounts.clients.clients_policies_sub_wizard \
    import ClientsPoliciesSubWizard
from test_framework.web_admin_core.pages.clients_accounts.clients.clients_pos_maintance_sub_wizard \
    import ClientsPosMaintenanceSubWizard
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


class QAP_T3672(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None,
                 db_manager=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.db_manager = db_manager

        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")

        self.name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.id = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.ext_id_client = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.clearing_account_type = 'Firm'
        self.description = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.disclose_exec = 'Manual'
        self.client_group = 'ACAClientGroup'
        self.invalid_tick_size_policy = 'Reject'
        self.virtual_account = 'ACABankFirm'
        self.external_ordID_format = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.booking_inst = 'Manual'
        self.allocation_preference = 'Manual'
        self.allocation_matching_service = 'Manual'
        self.block_approval = 'Manual'
        self.rounding_direction = 'RoundDown'
        self.fix_matching_profile = ''
        self.counterparts = 'TC Counterpart'
        self.short_sell_account = 'true'

        self.user_manager = self.data_set.get_user("user_6")
        self.desk = self.data_set.get_desk("desk_3")
        self.fix_order_recipient_user = self.data_set.get_user("user_15")
        self.fix_order_recipient_desk = self.data_set.get_desk("desk_1")
        self.middle_office_user = self.data_set.get_user("user_15")
        self.middle_office_desk = self.data_set.get_desk("desk_1")

        self.bic = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.dtcc = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.omgeo = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.other = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.sid = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.tfm = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.booking_field_1 = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.booking_field_2 = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.booking_field_3 = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.booking_field_4 = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.booking_field_5 = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))

        self.default_execution_strategy_type = 'Auction'
        self.default_execution_strategy = 'TC_VWAP'
        self.default_child_execution_strategy_type = 'TCA_TWAP'
        self.default_routing_instruction = 'BlockDiscovery'
        self.custom_validation_rules = 'HeldRule'

        self.position_maintenance = 'MaintainedAndValidated'
        self.validate_pos_limit = 'true'
        self.underl_position_maintenance = 'MaintainedAndValidated'
        self.validate_underl_position = 'true'
        self.cash_maintenance = 'MaintainedAndValidated'
        self.pnl_maintenance = 'true'
        self.posit_price_currency = 'InstrCurrency'

        self.instr_type = 'Bond'
        self.pos_keeping_mode = 'Gross'

        self.venue = self.data_set.get_venue_by_name("venue_1")
        self.venue_client_name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.venue_client_account_group_name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.default_route = self.data_set.get_route("route_1")
        self.max_commission_type = 'BasisPoints'
        self.max_commission_value = '987'

        self.route = self.data_set.get_route("route_1")
        self.route_client_name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))

        self.trade_confirm_generation = 'Automatic'
        self.trade_confirm_preference = 'Both'
        self.net_gross_ind_type = 'Gross'
        self.email_address = '2@2'
        self.recipient_type = 'BCC'

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        side_menu = SideMenu(self.web_driver_container)

        login_page.login_to_web_admin(self.login, self.password)
        side_menu.open_clients_page()

    def test_context(self):
        page = ClientsPage(self.web_driver_container)
        values_tab = ClientsValuesSubWizard(self.web_driver_container)
        assignments_tab = ClientsAssignmentsSubWizard(self.web_driver_container)
        external_source_tab = ClientsExternalSourcesSubWizard(self.web_driver_container)
        policies_tab = ClientsPoliciesSubWizard(self.web_driver_container)
        pos_maintenance = ClientsPosMaintenanceSubWizard(self.web_driver_container)
        instr_type_tab = ClientsInstrTypesSubWizard(self.web_driver_container)
        venues_tab = ClientsVenuesSubWizard(self.web_driver_container)
        route_tab = ClientsRoutesSubWizard(self.web_driver_container)
        trade_confirm = ClientsTradeConfirmSubWizard(self.web_driver_container)
        wizard = ClientsWizard(self.web_driver_container)

        try:
            self.precondition()

            page.click_on_new()

            values_tab.set_name(self.name)
            values_tab.set_id(self.id)
            values_tab.set_ext_id_client(self.ext_id_client)
            values_tab.set_clearing_account_type(self.clearing_account_type)
            values_tab.set_description(self.description)
            values_tab.set_disclose_exec(self.disclose_exec)
            values_tab.set_client_group(self.client_group)
            values_tab.set_invalid_tick_size_policy(self.invalid_tick_size_policy)
            values_tab.set_virtual_account(self.virtual_account)
            values_tab.set_external_odr_id_format(self.external_ordID_format)
            values_tab.set_booking_inst(self.booking_inst)
            values_tab.set_allocation_preference(self.allocation_preference)
            values_tab.set_allocation_matching_service(self.allocation_matching_service)
            values_tab.set_block_approval(self.block_approval)
            values_tab.set_rounding_direction(self.rounding_direction)
            self.fix_matching_profile = random.choice(values_tab.get_all_fix_matching_profile_from_drop_menu())
            values_tab.set_fix_matching_profile(self.fix_matching_profile)
            values_tab.set_counterpart(self.counterparts)
            values_tab.click_on_short_sell_account_checkbox()

            assignments_tab.set_user_manager(self.user_manager)
            assignments_tab.set_desk(self.desk)
            assignments_tab.set_fix_order_recipient_user(self.fix_order_recipient_user)
            assignments_tab.set_fix_order_recipient_desk(self.fix_order_recipient_desk)
            assignments_tab.set_middle_office_desk(self.middle_office_desk)
            assignments_tab.set_middle_office_user(self.middle_office_user)

            external_source_tab.set_bic_venue_act_grp_name(self.bic)
            external_source_tab.set_dtcc_venue_act_grp_name(self.dtcc)
            external_source_tab.set_omgeo_venue_act_grp_name(self.omgeo)
            external_source_tab.set_other_venue_act_grp_name(self.other)
            external_source_tab.set_sid_venue_act_grp_name(self.sid)
            external_source_tab.set_tfm_venue_act_grp_name(self.tfm)
            external_source_tab.set_bo_field_1(self.booking_field_1)
            external_source_tab.set_bo_field_2(self.booking_field_2)
            external_source_tab.set_bo_field_3(self.booking_field_3)
            external_source_tab.set_bo_field_4(self.booking_field_4)
            external_source_tab.set_bo_field_5(self.booking_field_5)

            policies_tab.set_default_execution_strategy_type(self.default_execution_strategy_type)
            policies_tab.set_default_execution_strategies(self.default_execution_strategy)
            policies_tab.set_default_child_execution_strategy(self.default_child_execution_strategy_type)
            policies_tab.set_default_routing_instruction(self.default_routing_instruction)
            policies_tab.set_custom_validation_rules(self.custom_validation_rules)

            pos_maintenance.set_position_maintenance(self.position_maintenance)
            pos_maintenance.click_on_validate_pos_limit()
            pos_maintenance.set_underl_position_maintenance(self.underl_position_maintenance)
            pos_maintenance.click_on_validate_pos_limit()
            pos_maintenance.set_cash_maintenance(self.cash_maintenance)
            pos_maintenance.click_on_pnl_maintenance()
            pos_maintenance.set_posit_price_currency(self.posit_price_currency)

            instr_type_tab.click_on_plus()
            instr_type_tab.set_instr_type(self.instr_type)
            instr_type_tab.set_pos_keeping_mode(self.pos_keeping_mode)
            instr_type_tab.click_on_checkmark()
            time.sleep(1)

            venues_tab.click_on_plus()
            venues_tab.set_venue(self.venue)
            venues_tab.set_venue_client_name(self.venue_client_name)
            venues_tab.set_venue_client_account(self.venue_client_account_group_name)
            venues_tab.set_default_route(self.route)
            venues_tab.set_max_commission_type(self.max_commission_type)
            venues_tab.set_max_commission_value(self.max_commission_value)
            venues_tab.click_on_checkmark()
            time.sleep(1)

            route_tab.click_on_plus()
            route_tab.set_route(self.route)
            route_tab.set_route_client_name(self.route_client_name)
            route_tab.click_on_checkmark()
            time.sleep(1)

            trade_confirm.set_trade_confirm_generation(self.trade_confirm_generation)
            trade_confirm.set_trade_confirm_preference(self.trade_confirm_preference)
            trade_confirm.set_net_gross_ind_type(self.net_gross_ind_type)
            trade_confirm.click_on_plus()
            trade_confirm.set_email_address(self.email_address)
            trade_confirm.set_recipient_types(self.recipient_type)
            trade_confirm.click_on_checkmark()
            time.sleep(1)
            expected_pdf_content = [f"ID: {self.id}", f"Name: {self.name}", f"Ext ID Client: {self.ext_id_client}",
                                    f"Clearing Account Type: {self.clearing_account_type}",
                                    f"Description: {self.description}", f"Disclose Exec: {self.disclose_exec}",
                                    f"Client Group: {self.client_group}",
                                    f"Invalid Tick Size Policy: {self.invalid_tick_size_policy}",
                                    f"Virtual Account: {self.virtual_account}",
                                    f"External OrdID Format: {self.external_ordID_format}",
                                    f"Booking Inst: {self.booking_inst}",
                                    f"Allocation Preference: {self.allocation_preference}",
                                    f"Allocation Matching Service: {self.allocation_matching_service}",
                                    f"Block Approval: {self.block_approval}",
                                    f"Rounding Direction: {self.rounding_direction}",
                                    f"FIX Matching Profile: {self.fix_matching_profile}",
                                    f"Counterpart: {self.counterparts}", f"Short Sell Account: {self.short_sell_account}",
                                    f"User Manager: {self.user_manager}", f"Desk Manager: {self.desk}",
                                    f"FIX Order Recipient User: {self.fix_order_recipient_user}",
                                    f"FIX Order Recipient Desk: {self.fix_order_recipient_desk}",
                                    f"Middle Office User: {self.middle_office_user}",
                                    f"Middle Office Desk: {self.middle_office_desk}",
                                    f"BIC: {self.bic}", f"DTCC: {self.dtcc}", f"OMGEO: {self.omgeo}",
                                    f"Other: {self.other}", f"SID: {self.sid}", f"TFM: {self.tfm}",
                                    f"Booking Field 1: {self.booking_field_1}", f"Booking Field 2: {self.booking_field_2}",
                                    f"Booking Field 3: {self.booking_field_3}", f"Booking Field 4: {self.booking_field_4}",
                                    f"Booking Field 5: {self.booking_field_5}",
                                    f"Default Execution Strategy Type: {self.default_child_execution_strategy_type}",
                                    f"Default Execution Strategy: {self.default_execution_strategy_type}",
                                    f"Default Child Execution Strategy: {self.default_child_execution_strategy_type}",
                                    f"Default Routing Instruction: {self.default_routing_instruction}",
                                    f"Custom Validation Rules: {self.custom_validation_rules}",
                                    f"Position Maintenance: {self.position_maintenance}",
                                    f"Validate PosLimit: {self.validate_pos_limit}",
                                    f"Underl Position Maintenance: {self.underl_position_maintenance}",
                                    f"Validate Underl PosLimit: {self.validate_underl_position}",
                                    f"Cash Maintenance: {self.cash_maintenance}",
                                    f"PNL Maintenance: {self.pnl_maintenance}",
                                    f"Posit Price Currency: {self.posit_price_currency}",
                                    f"{self.instr_type} - {self.pos_keeping_mode}",
                                    f"Venue: {self.venue}, Venue Client Name: {self.venue_client_name}, "
                                    f"Venue Client AccountGroup Name: {self.venue_client_account_group_name},"
                                    f"Default Route: {self.default_route}, "
                                    f"Max Commission Type: {self.max_commission_type},"
                                    f"Max Commission Value: {self.max_commission_value}.",
                                    f"Route: {self.route}", f"Route Client Name: {self.route_client_name}",
                                    f"Trade Confirm Generation: {self.trade_confirm_generation}",
                                    f"Trade Confirm Preference: {self.trade_confirm_preference}",
                                    f"Net Gross Ind Type: {self.net_gross_ind_type}",
                                    f"{self.email_address}: {self.recipient_type}"]

            self.verify(f"Is PDF contains {expected_pdf_content}", True,
                        wizard.click_download_pdf_entity_button_and_check_pdf(expected_pdf_content))

            wizard.click_on_save_changes()
            time.sleep(2)
            page.set_name(self.name)
            time.sleep(1)
            self.verify("New Client has been create", True, page.is_searched_client_found(self.name))

        except Exception:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            errors = f'"{[traceback.extract_tb(exc_traceback, limit=4)]}"'.replace("\\", "/")
            basic_custom_actions.create_event(f"FAILED", self.test_case_id, status='FAILED',
                                              body="[{\"type\": \"message\", \"data\":"+f"{errors}"+"}]")
            traceback.print_tb(exc_traceback, limit=3, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)

