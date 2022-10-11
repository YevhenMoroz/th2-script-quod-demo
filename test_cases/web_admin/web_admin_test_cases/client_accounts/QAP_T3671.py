import sys
import time
import traceback
import random
import string

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.client_accounts.accounts.accounts_page import AccountsPage
from test_framework.web_admin_core.pages.client_accounts.accounts.accounts_wizard import AccountsWizard
from test_framework.web_admin_core.pages.client_accounts.accounts.accounts_routes_subwizard \
    import AccountsRoutesSubWizard
from test_framework.web_admin_core.pages.client_accounts.accounts.accounts_dimensions_subwizard \
    import AccountsDimensionsSubWizard
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T3671(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")

        self.id = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.ext_id_client = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.client = 'CLIENT1'
        self.description = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.position_source = 'External'
        self.clearing_account_type = 'Institutional'
        self.client_id_source = 'BIC'
        self.client_matching_id = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.bo_field_1 = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.bo_field_2 = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.bo_field_3 = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.bo_field_4 = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.bo_field_5 = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.counterpart = 'TCOther'

        self.venue_account = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.venue = 'AMEX'
        self.account_id_source = 'SID'
        self.dimensions_default_route = 'Credit Suisse'
        self.venue_client_account_name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))

        self.route_account_name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.route = 'Credit Suisse'
        self.default_route = 'Credit Suisse'

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        time.sleep(2)
        side_menu = SideMenu(self.web_driver_container)
        side_menu.open_accounts_page()
        time.sleep(2)

    def test_context(self):

        try:
            self.precondition()

            main_page = AccountsPage(self.web_driver_container)
            main_page.click_new_button()
            time.sleep(2)
            values_tab = AccountsWizard(self.web_driver_container)
            values_tab.set_id(self.id)
            values_tab.set_ext_id_client(self.ext_id_client)
            values_tab.set_client(self.client)
            values_tab.set_description(self.description)
            values_tab.set_position_source(self.position_source)
            values_tab.set_client_id_source(self.client_id_source)
            values_tab.toggle_trade_confirm_eligibility()
            values_tab.set_client_matching_id(self.client_matching_id)
            values_tab.set_bo_field_1(self.bo_field_1)
            values_tab.set_bo_field_2(self.bo_field_2)
            values_tab.set_bo_field_3(self.bo_field_3)
            values_tab.set_bo_field_4(self.bo_field_4)
            values_tab.set_bo_field_5(self.bo_field_5)
            values_tab.toggle_commission_exemption()
            values_tab.set_counterpart(self.counterpart)
            dimensions_tab = AccountsDimensionsSubWizard(self.web_driver_container)
            dimensions_tab.click_on_plus()
            dimensions_tab.set_venue_account(self.venue_account)
            dimensions_tab.set_venue(self.venue)
            dimensions_tab.set_account_id_source(self.account_id_source)
            dimensions_tab.set_default_route(self.dimensions_default_route)
            dimensions_tab.set_stamp_exempt()
            dimensions_tab.set_levy_exempt()
            dimensions_tab.set_per_transac_exempt()
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
            time.sleep(2)

            actual_result = [self.id, self.ext_id_client, self.client, self.description, self.position_source,
                             self.clearing_account_type, self.client_id_source, self.client_matching_id, self.bo_field_1,
                             self.bo_field_2, self.bo_field_3, self.bo_field_4, self.bo_field_5, self.counterpart,
                             self.venue_account, self.venue, self.account_id_source, self.dimensions_default_route,
                             self.venue_client_account_name, self.route_account_name, self.route, self.default_route,
                             'true', 'false']
            self.verify("Is PDF file contains data?", True,
                        wizard.click_download_pdf_entity_button_and_check_pdf(actual_result))
            wizard.click_save_button()
            time.sleep(2)
            main_page.set_id(self.id)
            time.sleep(1)

            self.verify("New Account has been created", True, main_page.is_searched_account_found(self.id))

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
