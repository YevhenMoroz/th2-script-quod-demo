import sys
import time
import traceback
import random
import string

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.clients_accounts.accounts.accounts_page import AccountsPage
from test_framework.web_admin_core.pages.clients_accounts.accounts.accounts_wizard import AccountsWizard
from test_framework.web_admin_core.pages.clients_accounts.accounts.accounts_dimensions_subwizard \
    import AccountsDimensionsSubWizard
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T3348(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.account_id = 'QAP_T3348'
        self.ext_id_client = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.client_id_source = 'BIC'

        self.venue_account = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.venue = 'AMEX'
        self.account_id_source = 'SID'
        self.dimensions_default_route = self.data_set.get_default_route("default_route_1")
        self.venue_client_account_name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        time.sleep(2)
        side_menu = SideMenu(self.web_driver_container)
        side_menu.open_accounts_page()
        main_page = AccountsPage(self.web_driver_container)
        main_page.set_id(self.account_id)
        time.sleep(1)
        if not main_page.is_searched_account_found(self.account_id):
            main_page.click_new_button()
            values_tab = AccountsWizard(self.web_driver_container)
            values_tab.set_id(self.account_id)
            values_tab.set_ext_id_client(self.ext_id_client)
            values_tab.set_client_id_source(self.client_id_source)
            wizard = AccountsWizard(self.web_driver_container)
            wizard.click_save_button()

    def test_context(self):

        try:
            self.precondition()

            main_page = AccountsPage(self.web_driver_container)
            main_page.set_id(self.account_id)
            time.sleep(1)
            main_page.click_more_actions_button()
            main_page.click_edit_entity_button()

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

            actual_result = [dimensions_tab.get_stamp_exempt(), dimensions_tab.get_levy_exempt(),
                             dimensions_tab.get_per_transac_exempt()]

            wizard = AccountsWizard(self.web_driver_container)
            wizard.click_save_button()
            time.sleep(1)
            main_page.set_id(self.account_id)
            time.sleep(1)
            main_page.click_more_actions_button()
            main_page.click_edit_entity_button()

            expected_result = [dimensions_tab.get_stamp_exempt(), dimensions_tab.get_levy_exempt(),
                               dimensions_tab.get_per_transac_exempt()]

            self.verify("All checkboxes has been save", actual_result, expected_result)

            dimensions_tab.set_venue_filter(self.venue)
            time.sleep(1)
            dimensions_tab.click_delete_button()

            wizard.click_save_button()

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
