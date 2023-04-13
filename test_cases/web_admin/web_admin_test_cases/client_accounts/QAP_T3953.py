import sys
import time
import traceback
import random
import string

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.clients_accounts.accounts.accounts_page import AccountsPage
from test_framework.web_admin_core.pages.clients_accounts.accounts.accounts_wizard import AccountsWizard
from test_framework.web_admin_core.pages.clients_accounts.accounts.accounts_routes_subwizard \
    import AccountsRoutesSubWizard
from test_framework.web_admin_core.pages.clients_accounts.accounts.accounts_dimensions_subwizard \
    import AccountsDimensionsSubWizard
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T3953(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")

        self.id = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.ext_id_client = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.new_id = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.new_ext_id_client = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.client = 'CLIENT1'
        self.description = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.clearing_account_type = 'Institutional'
        self.client_id_source = 'BIC'
        self.bo_field_5 = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.counterpart = 'TCOther'

        self.venue_account = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.new_venue_account = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.venue = 'AMEX'
        self.account_id_source = 'SID'
        self.dimensions_default_route = 'Credit Suisse'
        self.venue_client_account_name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.new_venue_client_account_name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))

        self.route_account_name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.route = 'ESDEMO'
        self.default_route = 'ESDEMO'

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        side_menu.open_accounts_page()

        main_page = AccountsPage(self.web_driver_container)
        main_page.click_new_button()
        values_tab = AccountsWizard(self.web_driver_container)
        values_tab.set_id(self.id)
        values_tab.set_ext_id_client(self.ext_id_client)
        values_tab.set_client(self.client)
        values_tab.set_description(self.description)
        values_tab.set_client_id_source(self.client_id_source)
        values_tab.set_bo_field_5(self.bo_field_5)
        values_tab.toggle_commission_exemption()
        values_tab.set_counterpart(self.counterpart)

        dimensions_tab = AccountsDimensionsSubWizard(self.web_driver_container)
        dimensions_tab.click_on_plus()
        dimensions_tab.set_venue_account(self.venue_account)
        dimensions_tab.set_venue(self.venue)
        dimensions_tab.set_account_id_source(self.account_id_source)
        dimensions_tab.set_stamp_exempt()
        dimensions_tab.set_venue_client_account_name(self.venue_client_account_name)
        dimensions_tab.click_on_checkmark_button()

        routes_tab = AccountsRoutesSubWizard(self.web_driver_container)
        routes_tab.click_on_plus_button()
        routes_tab.set_route_account_name(self.route_account_name)
        routes_tab.set_route(self.route)
        routes_tab.select_agent_fee_exemption_checkbox()
        routes_tab.click_on_checkmark_button()
        routes_tab.set_default_route(self.default_route)
        wizard = AccountsWizard(self.web_driver_container)
        wizard.click_save_button()

    def test_context(self):
        values_tab = AccountsWizard(self.web_driver_container)
        dimensions_tab = AccountsDimensionsSubWizard(self.web_driver_container)
        routes_tab = AccountsRoutesSubWizard(self.web_driver_container)
        wizard = AccountsWizard(self.web_driver_container)

        try:
            self.precondition()

            main_page = AccountsPage(self.web_driver_container)
            main_page.set_id(self.id)
            time.sleep(1)
            main_page.click_more_actions_button()
            main_page.click_clone_entity_button()
            dimensions_tab.click_edit_button()
            routes_tab.click_edit_button()

            expected_result = [self.client, self.description, self.client_id_source, self.bo_field_5, "True",
                               self.counterpart, self.venue_account, self.venue, self.account_id_source, "True",
                               self.venue_client_account_name, self.route_account_name, self.route, "True",
                               self.default_route]

            actual_result = [values_tab.get_client(), values_tab.get_description(), values_tab.get_client_id_source(),
                             values_tab.get_bo_field_5(), str(values_tab.is_commission_exemption_checked()),
                             values_tab.get_counterpart(), dimensions_tab.get_venue_account(),
                             dimensions_tab.get_venue(), dimensions_tab.get_account_id_source(),
                             str(dimensions_tab.get_stamp_exempt()), dimensions_tab.get_venue_client_account_name(),
                             routes_tab.get_route_account_name(), routes_tab.get_route(),
                             str(routes_tab.is_agent_fee_exemption_selected()),
                             routes_tab.get_default_route()]

            self.verify("Cloned data the same as parent", expected_result, actual_result)

            values_tab.set_id(self.new_id)
            values_tab.set_ext_id_client(self.new_ext_id_client)
            dimensions_tab.set_venue_account(self.new_venue_account)
            dimensions_tab.set_venue_client_account_name(self.new_venue_client_account_name)
            dimensions_tab.click_on_checkmark_button()
            wizard.click_save_button()

            main_page.set_id(self.new_id)
            time.sleep(1)
            self.verify("New account has been create", True, main_page.is_searched_account_found(self.new_id))

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
