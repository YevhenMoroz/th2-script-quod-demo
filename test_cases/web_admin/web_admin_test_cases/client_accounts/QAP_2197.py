import time
import traceback
from uuid import uuid1

from custom import basic_custom_actions
from test_cases.web_admin.web_admin_core.pages.client_accounts.accounts.accounts_dimensions_subwizard import \
    AccountsDimensionsSubWizard
from test_cases.web_admin.web_admin_core.pages.client_accounts.accounts.accounts_page import AccountsPage
from test_cases.web_admin.web_admin_core.pages.client_accounts.accounts.accounts_wizard import AccountsWizard
from test_cases.web_admin.web_admin_core.pages.login.login_page import LoginPage
from test_cases.web_admin.web_admin_core.pages.root.side_menu import SideMenu
from test_cases.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


# Draft
class QAP_2197(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id)
        self.account = f"QAP-2197_{str(uuid1())}"
        self.client = "CLIENT1"
        self.client_id_source = "Other"

        self.venue_account = "TestVenueAccount"
        self.venue = "AMEX"
        self.account_id_source = "BIC"
        self.default_route = "Direct"

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.set_login("adm03")
        login_page.set_password("adm03")
        login_page.click_login_button()
        login_page.check_is_login_successful()

        side_menu = SideMenu(self.web_driver_container)
        side_menu.open_accounts_page()

        accounts_page = AccountsPage(self.web_driver_container)
        accounts_page.click_new_button()
        accounts_wizard = AccountsWizard(self.web_driver_container)
        accounts_wizard.set_id(self.account)
        accounts_wizard.set_ext_id_client(self.account)
        accounts_wizard.set_client(self.client)
        accounts_wizard.set_client_id_source(self.client_id_source)

        accounts_dimensions_subwizard = AccountsDimensionsSubWizard(self.web_driver_container)
        accounts_dimensions_subwizard.open_dimensions_subwizard()
        accounts_dimensions_subwizard.set_venue_account(self.venue_account)
        accounts_dimensions_subwizard.set_venue(self.venue)
        accounts_dimensions_subwizard.set_account_id_source(self.account_id_source)
        accounts_dimensions_subwizard.set_default_route(self.default_route)
        accounts_dimensions_subwizard.click_create_entity_button()

        accounts_wizard.click_save_button()

    def test_context(self):
        try:
            self.precondition()

            new_venue_account = "TestVenueAccount2"
            new_venue = "ADX"
            new_account_id_source = "Other"
            new_default_route = "Credit Suisse"
            expected_pdf_content = [new_venue_account, new_venue, new_account_id_source, new_default_route]
            side_menu = SideMenu(self.web_driver_container)
            side_menu.open_accounts_page()
            accounts_page = AccountsPage(self.web_driver_container)
            accounts_page.filter_grid(self.account)
            accounts_page.click_more_actions_button()
            accounts_page.click_edit_entity_button()
            time.sleep(2)
            accounts_wizard = AccountsWizard(self.web_driver_container)
            accounts_dimensions_subwizard = AccountsDimensionsSubWizard(self.web_driver_container)
            accounts_dimensions_subwizard.click_delete_button()
            time.sleep(2)
            accounts_dimensions_subwizard.filter_dimensions(venue_account=self.venue_account,
                                                            venue=self.venue,
                                                            account_id_source=self.account_id_source,
                                                            default_route=self.default_route)

            accounts_dimensions_subwizard.click_on_plus()
            accounts_dimensions_subwizard.set_venue_account(new_venue_account)
            time.sleep(1)
            accounts_dimensions_subwizard.set_venue(new_venue)
            time.sleep(1)
            accounts_dimensions_subwizard.set_account_id_source(new_account_id_source)
            time.sleep(1)
            accounts_dimensions_subwizard.set_default_route(new_default_route)
            time.sleep(1)
            accounts_dimensions_subwizard.click_create_entity_button()
            time.sleep(2)
            accounts_wizard.click_save_button()
            time.sleep(2)
            self.verify("Popup context", "Account changes saved", accounts_page.get_popup_text())

            accounts_page.filter_grid(self.account)
            time.sleep(2)
            accounts_page.click_more_actions_button()
            time.sleep(2)
            accounts_page.click_edit_entity_button()
            time.sleep(2)
            self.verify(f"Is PDF contains {expected_pdf_content}", True,
                        accounts_wizard.click_download_pdf_entity_button_and_check_pdf(expected_pdf_content))

            time.sleep(5)
            accounts_dimensions_subwizard.filter_dimensions(venue_account=new_venue_account,
                                                            venue=new_venue,
                                                            account_id_source=new_account_id_source,
                                                            default_route=new_default_route)

            accounts_dimensions_subwizard.click_edit_button()
            self.verify("Venue Account", new_venue_account, accounts_dimensions_subwizard.get_venue_account())
            self.verify("Venue", new_venue, accounts_dimensions_subwizard.get_venue())
            self.verify("Account ID Source", new_account_id_source,
                        accounts_dimensions_subwizard.get_account_id_source())
            self.verify("Default Route", new_default_route, accounts_dimensions_subwizard.get_default_route())

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            print(traceback.format_exc() + " Search in ->  " + self.__class__.__name__)
