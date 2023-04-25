import sys
import time
import traceback
import random
import string

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.clients_accounts.accounts.accounts_dimensions_subwizard import \
    AccountsDimensionsSubWizard
from test_framework.web_admin_core.pages.clients_accounts.accounts.accounts_page import AccountsPage
from test_framework.web_admin_core.pages.clients_accounts.accounts.accounts_wizard import AccountsWizard
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


# Draft
class QAP_T3940(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)

        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.account = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.ext_id_client = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.client = str
        self.client_id_source = self.data_set.get_client_id_source("client_id_source_2")
        self.venue_account = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.venue = self.data_set.get_venue_by_name("venue_10")
        self.account_id_source = self.data_set.get_account_id_source("account_id_source_1")
        self.default_route = self.data_set.get_default_route("default_route_1")

        self.new_venue_account = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.new_venue = self.data_set.get_venue_by_name("venue_8")
        self.new_account_id_source = "Other"
        self.new_default_route = self.data_set.get_default_route("default_route_2")

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.set_login(self.login)
        login_page.set_password(self.password)
        login_page.click_login_button()
        login_page.check_is_login_successful()

        side_menu = SideMenu(self.web_driver_container)
        side_menu.open_accounts_page()
        time.sleep(2)

        accounts_page = AccountsPage(self.web_driver_container)
        accounts_page.click_new_button()
        time.sleep(2)
        accounts_wizard = AccountsWizard(self.web_driver_container)
        accounts_wizard.set_id(self.account)
        accounts_wizard.set_ext_id_client(self.ext_id_client)
        self.client = random.choice(accounts_wizard.get_all_clients_from_drop_menu())
        accounts_wizard.set_client(self.client)
        accounts_wizard.set_client_id_source(self.client_id_source)

        accounts_dimensions_subwizard = AccountsDimensionsSubWizard(self.web_driver_container)
        accounts_dimensions_subwizard.open_dimensions_subwizard()
        accounts_dimensions_subwizard.set_venue_account(self.venue_account)
        accounts_dimensions_subwizard.set_venue(self.venue)
        accounts_dimensions_subwizard.set_account_id_source(self.account_id_source)
        accounts_dimensions_subwizard.set_default_route(self.default_route)
        accounts_dimensions_subwizard.click_on_checkmark_button()

        accounts_wizard.click_save_button()
        time.sleep(2)

    def test_context(self):
        try:
            self.precondition()

            expected_pdf_content = [self.new_venue_account, self.new_venue, self.new_account_id_source]

            accounts_page = AccountsPage(self.web_driver_container)
            accounts_page.filter_grid(self.account)
            time.sleep(2)
            accounts_page.click_more_actions_button()
            accounts_page.click_edit_entity_button()
            time.sleep(2)
            accounts_wizard = AccountsWizard(self.web_driver_container)
            accounts_dimensions_subwizard = AccountsDimensionsSubWizard(self.web_driver_container)
            accounts_dimensions_subwizard.click_delete_button()
            time.sleep(1)
            accounts_dimensions_subwizard.click_on_plus()
            accounts_dimensions_subwizard.set_venue_account(self.new_venue_account)
            accounts_dimensions_subwizard.set_venue(self.new_venue)
            accounts_dimensions_subwizard.set_account_id_source(self.new_account_id_source)
            accounts_dimensions_subwizard.set_default_route(self.new_default_route)
            accounts_dimensions_subwizard.click_on_checkmark_button()
            accounts_wizard.click_save_button()
            time.sleep(2)
            self.verify("Popup context", "Account changes saved", accounts_page.get_popup_text())

            accounts_page.filter_grid(self.account)
            time.sleep(2)
            accounts_page.click_more_actions_button()
            time.sleep(1)
            accounts_page.click_edit_entity_button()
            time.sleep(2)
            self.verify(f"Is PDF contains {expected_pdf_content}", True,
                        accounts_wizard.click_download_pdf_entity_button_and_check_pdf(expected_pdf_content))

            time.sleep(2)
            accounts_dimensions_subwizard.filter_dimensions(venue_account=self.new_venue_account)

            accounts_dimensions_subwizard.click_edit_button()
            self.verify("Venue Account", self.new_venue_account, accounts_dimensions_subwizard.get_venue_account())
            self.verify("Venue", self.new_venue, accounts_dimensions_subwizard.get_venue())
            self.verify("Account ID Source", self.new_account_id_source,
                        accounts_dimensions_subwizard.get_account_id_source())
            self.verify("Default Route", self.new_default_route, accounts_dimensions_subwizard.get_default_route())

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
