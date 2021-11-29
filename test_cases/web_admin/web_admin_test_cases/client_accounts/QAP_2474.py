import random
import string
import sys
import time
import traceback

from custom import basic_custom_actions
from test_cases.web_admin.web_admin_core.pages.client_accounts.accounts.accounts_dimensions_subwizard import \
    AccountsDimensionsSubWizard
from test_cases.web_admin.web_admin_core.pages.client_accounts.accounts.accounts_page import AccountsPage
from test_cases.web_admin.web_admin_core.pages.login.login_page import LoginPage
from test_cases.web_admin.web_admin_core.pages.root.side_menu import SideMenu
from test_cases.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_2474(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id)
        self.login = "adm02"
        self.password = "adm02"
        self.venue_account = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.venue = "AMEX"
        self.account_id_source = "BIC"
        self.default_route = "Direct"

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        time.sleep(2)
        side_menu.open_accounts_page()
        main_page = AccountsPage(self.web_driver_container)
        main_page.click_new_button()
        time.sleep(2)
        dimensions_sub_wizard = AccountsDimensionsSubWizard(self.web_driver_container)
        dimensions_sub_wizard.click_on_plus()
        dimensions_sub_wizard.set_venue_account(self.venue_account)
        dimensions_sub_wizard.set_venue(self.venue)
        dimensions_sub_wizard.set_account_id_source(self.account_id_source)
        dimensions_sub_wizard.set_default_route(self.default_route)
        dimensions_sub_wizard.click_create_entity_button()
        time.sleep(2)

    def test_context(self):

        try:
            self.precondition()
            dimensions_sub_wizard = AccountsDimensionsSubWizard(self.web_driver_container)
            expected_content_at_dimensions_tab = [
                self.venue_account,
                self.venue,
                self.account_id_source,
                self.default_route]
            dimensions_sub_wizard.click_edit_button()
            actual_content_at_dimensions_tab = [dimensions_sub_wizard.get_venue_account(),
                                                dimensions_sub_wizard.get_venue(),
                                                dimensions_sub_wizard.get_account_id_source(),
                                                dimensions_sub_wizard.get_default_route()]
            self.verify("Is data at dimensions tab set correctly", expected_content_at_dimensions_tab,
                        actual_content_at_dimensions_tab)

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
