import random
import string
import sys
import time
import traceback

from custom import basic_custom_actions
from test_cases.web_admin.web_admin_core.pages.client_accounts.accounts.accounts_dimensions_subwizard import \
    AccountsDimensionsSubWizard
from test_cases.web_admin.web_admin_core.pages.client_accounts.accounts.accounts_page import AccountsPage
from test_cases.web_admin.web_admin_core.pages.client_accounts.accounts.accounts_wizard import AccountsWizard
from test_cases.web_admin.web_admin_core.pages.login.login_page import LoginPage
from test_cases.web_admin.web_admin_core.pages.root.side_menu import SideMenu
from test_cases.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_2196(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id)
        self.login = "adm02"
        self.password = "Qwerty123!"
        self.id = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.ext_id_client = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.client_id_source = "BIC"
        self.venue_account = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.venue = "AMSTERDAM"
        self.client = "CLIENT1"
        self.account_id_source = "BIC"

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        time.sleep(2)
        side_menu.open_accounts_page()
        main_page = AccountsPage(self.web_driver_container)
        main_page.click_new_button()
        time.sleep(2)
        values_sub_wizard = AccountsWizard(self.web_driver_container)
        values_sub_wizard.set_id(self.id)
        time.sleep(1)
        values_sub_wizard.set_ext_id_client(self.ext_id_client)
        time.sleep(1)
        values_sub_wizard.set_client(self.client)
        time.sleep(1)
        values_sub_wizard.set_client_id_source(self.client_id_source)
        time.sleep(2)
        dimensions_sub_wizard = AccountsDimensionsSubWizard(self.web_driver_container)
        dimensions_sub_wizard.click_on_plus()
        dimensions_sub_wizard.set_venue_account(self.venue_account)
        dimensions_sub_wizard.set_venue(self.venue)
        dimensions_sub_wizard.set_account_id_source(self.account_id_source)
        time.sleep(2)
        dimensions_sub_wizard.click_create_entity_button()
        time.sleep(2)
        wizard = AccountsWizard(self.web_driver_container)
        wizard.click_save_button()
        time.sleep(2)
        main_page.set_id(self.id)
        time.sleep(2)
        main_page.click_more_actions_button()
        time.sleep(1)
        main_page.click_edit_entity_button()
        time.sleep(2)

    def test_context(self):
        try:
            self.precondition()
            main_page = AccountsPage(self.web_driver_container)
            wizard = AccountsWizard(self.web_driver_container)
            dimensions_sub_wizard = AccountsDimensionsSubWizard(self.web_driver_container)
            time.sleep(5)
            dimensions_sub_wizard.click_delete_button()
            time.sleep(2)
            expected_pdf_content = [
                self.ext_id_client,
                self.client_id_source, ]
            self.verify("Is PDF contains correctly values", True,
                        wizard.click_download_pdf_entity_button_and_check_pdf(expected_pdf_content))
            wizard.click_save_button()
            time.sleep(2)
            main_page.set_id(self.id)
            time.sleep(2)
            main_page.click_more_actions_button()
            time.sleep(1)
            main_page.click_edit_entity_button()
            time.sleep(2)
            dimensions_sub_wizard.filter_dimensions(venue_account=self.venue_account)
            time.sleep(1)

            try:
                self.verify("Venue account deleted correctly", False, dimensions_sub_wizard.is_venue_account_present())
            except Exception as e:
                self.verify("Error Venue account not  deleted !", True, e.__class__.__name__)
        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
