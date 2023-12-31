import random
import string
import time

from test_framework.web_admin_core.pages.clients_accounts.accounts.accounts_dimensions_subwizard import \
    AccountsDimensionsSubWizard
from test_framework.web_admin_core.pages.clients_accounts.accounts.accounts_page import AccountsPage
from test_framework.web_admin_core.pages.clients_accounts.accounts.accounts_wizard import AccountsWizard
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T3938(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.venue_account = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.venue = self.data_set.get_venue_by_name("venue_1")
        self.account_id_source = self.data_set.get_account_id_source("account_id_source_2")

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        time.sleep(2)
        side_menu.open_accounts_page()
        main_page = AccountsPage(self.web_driver_container)
        main_page.click_more_actions_button()
        time.sleep(2)
        main_page.click_edit_entity_button()
        time.sleep(2)

        dimensions_sub_wizard = AccountsDimensionsSubWizard(self.web_driver_container)
        dimensions_sub_wizard.click_on_plus()
        dimensions_sub_wizard.set_venue_account(self.venue_account)
        dimensions_sub_wizard.set_venue(self.venue)
        dimensions_sub_wizard.set_account_id_source(self.account_id_source)
        dimensions_sub_wizard.click_on_checkmark_button()

    def test_context(self):

        self.precondition()
        main_page = AccountsPage(self.web_driver_container)
        wizard = AccountsWizard(self.web_driver_container)
        expected_pdf_content = [self.venue_account,
                                self.venue,
                                self.account_id_source]
        self.verify("Is PDF contains correctly values", True,
                    wizard.click_download_pdf_entity_button_and_check_pdf(expected_pdf_content))
        ext_id_client = wizard.get_ext_id_client()
        wizard.click_save_button()
        time.sleep(2)
        self.verify("Is entity saved correctly", ext_id_client, main_page.get_ext_id_client())

