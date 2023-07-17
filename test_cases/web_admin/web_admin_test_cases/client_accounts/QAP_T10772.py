import random
import string
import time

from test_framework.web_admin_core.pages.clients_accounts.accounts.accounts_page import AccountsPage
from test_framework.web_admin_core.pages.clients_accounts.accounts.accounts_dimensions_subwizard \
    import AccountsDimensionsSubWizard
from test_framework.web_admin_core.pages.clients_accounts.accounts.accounts_wizard import AccountsWizard
from test_framework.web_admin_core.pages.clients_accounts.account_lists.main_page import MainPage as AccountListPage
from test_framework.web_admin_core.pages.clients_accounts.account_lists.wizard import Wizard as AccountListWizard
from test_framework.web_admin_core.pages.clients_accounts.clients.clients_page import ClientsPage
from test_framework.web_admin_core.pages.clients_accounts.clients.clietns_venues_sub_wizard \
    import ClientsVenuesSubWizard
from test_framework.web_admin_core.pages.clients_accounts.clients.clients_routes_sub_wizard \
    import ClientsRoutesSubWizard
from test_framework.web_admin_core.pages.clients_accounts.clients.clients_wizard import ClientsWizard
from test_framework.web_admin_core.pages.clients_accounts.client_lists.main_page import ClientListsPage
from test_framework.web_admin_core.pages.clients_accounts.client_lists.wizard import ClientListsWizard
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T10772(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)

        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")

        self.account = {"venue_account": ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6)),
                        "venue": self.data_set.get_venue_by_name("venue_1"),
                        "account_id_source": "OMGEO"}
        self.account_list = {"account": "ACABankFirm"}
        self.client = {"venue": self.data_set.get_venue_by_name("venue_1"),
                       "venue_client_name": ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6)),
                       "route": self.data_set.get_route("route_1"),
                       "route_client_name": ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))}
        self.client_list = {"client": "CLIENT1"}

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)

    def test_context(self):
        side_menu = SideMenu(self.web_driver_container)
        accounts_page = AccountsPage(self.web_driver_container)
        accounts_dimension_tab = AccountsDimensionsSubWizard(self.web_driver_container)
        accounts_wizard = AccountsWizard(self.web_driver_container)
        account_lists_page = AccountListPage(self.web_driver_container)
        account_lists_wizard = AccountListWizard(self.web_driver_container)
        clients_page = ClientsPage(self.web_driver_container)
        clients_venues_tab = ClientsVenuesSubWizard(self.web_driver_container)
        clients_routes_tab = ClientsRoutesSubWizard(self.web_driver_container)
        clients_wizard = ClientsWizard(self.web_driver_container)
        client_lists_page = ClientListsPage(self.web_driver_container)
        client_lists_wizard = ClientListsWizard(self.web_driver_container)

        self.precondition()

        side_menu.open_accounts_page()
        accounts_page.click_new_button()
        accounts_dimension_tab.click_on_plus()
        accounts_dimension_tab.set_venue_account(self.account["venue_account"])
        accounts_dimension_tab.set_venue(self.account["venue"])
        accounts_dimension_tab.set_account_id_source(self.account["account_id_source"])
        accounts_dimension_tab.click_on_checkmark_button()
        time.sleep(1)
        accounts_dimension_tab.filter_dimensions(venue_account=self.account["venue_account"].lower())
        time.sleep(1)
        self.verify("Account Dimension Tab - entry found by Venue Account in lower case",
                    True, accounts_dimension_tab.is_venue_account_present())
        accounts_dimension_tab.filter_dimensions(venue=self.account["venue"].lower())
        time.sleep(1)
        self.verify("Account Dimension Tab - entry found by Venue in lower case",
                    True, accounts_dimension_tab.is_venue_account_present())
        accounts_dimension_tab.filter_dimensions(venue=self.account["venue"].upper())
        time.sleep(1)
        self.verify("Account Dimension Tab - entry found by Venue in upper case",
                    True, accounts_dimension_tab.is_venue_account_present())
        accounts_dimension_tab.filter_dimensions(account_id_source=self.account["account_id_source"].lower())
        self.verify("Account Dimension Tab - entry found by Account ID Source in lower case",
                    True, accounts_dimension_tab.is_venue_account_present())
        accounts_wizard.click_on_close_button()
        accounts_wizard.click_on_no_button()
        time.sleep(1)

        side_menu.open_account_list_page()
        account_lists_page.click_on_new()
        account_lists_wizard.click_on_plus()
        account_lists_wizard.set_account(self.account_list["account"])
        account_lists_wizard.click_on_checkmark()
        time.sleep(1)
        account_lists_wizard.set_account_filter(self.account_list["account"].upper())
        time.sleep(1)
        self.verify("Account List - entry found by Account in upper case",
                    True, account_lists_wizard.is_account_present())
        account_lists_wizard.set_account_filter(self.account_list["account"].lower())
        time.sleep(1)
        self.verify("Account List - entry found by Account in lower case",
                    True, account_lists_wizard.is_account_present())

        account_lists_wizard.click_on_close_wizard()
        account_lists_wizard.click_on_no_button()
        time.sleep(1)

        side_menu.open_clients_page()
        clients_page.click_on_new()
        clients_venues_tab.click_on_plus()
        clients_venues_tab.set_venue(self.client["venue"])
        clients_venues_tab.set_venue_client_name(self.client["venue_client_name"])
        clients_venues_tab.click_on_checkmark()
        time.sleep(1)
        clients_venues_tab.set_venue_filter(self.client["venue"].upper())
        time.sleep(1)
        self.verify("Client Venues - entry found by Account in upper case",
                    True, clients_venues_tab.is_venue_present())
        clients_venues_tab.set_venue_filter(self.client["venue"].lower())
        time.sleep(1)
        self.verify("Client Venues - entry found by Account in lower case",
                    True, clients_venues_tab.is_venue_present())
        clients_venues_tab.set_venue_client_name_filter(self.client["venue_client_name"].upper())
        time.sleep(1)
        self.verify("Client Venues - entry found by Venue Client Name in upper case",
                    True, clients_venues_tab.is_venue_present())
        clients_venues_tab.set_venue_client_name_filter(self.client["venue_client_name"].lower())
        time.sleep(1)
        self.verify("Client Venues - entry found by Venue Client Name in lower case",
                    True, clients_venues_tab.is_venue_present())

        clients_routes_tab.click_on_plus()
        clients_routes_tab.set_route(self.client["route"])
        clients_routes_tab.set_route_client_name(self.client["route_client_name"])
        clients_routes_tab.click_on_checkmark()
        time.sleep(1)
        clients_routes_tab.set_route_filter(self.client["route"].upper())
        time.sleep(1)
        self.verify("Client Routes - entry found by Route in upper case",
                    True, clients_routes_tab.is_route_present())
        time.sleep(1)
        clients_routes_tab.set_route_filter(self.client["route"].lower())
        time.sleep(1)
        self.verify("Client Routes - entry found by Route in lower case",
                    True, clients_routes_tab.is_route_present())
        time.sleep(1)
        clients_routes_tab.set_route_client_name_filter(self.client["route_client_name"].upper())
        time.sleep(1)
        self.verify("Client Routes - entry found by Route Client Name in upper case",
                    True, clients_routes_tab.is_route_present())
        clients_routes_tab.set_route_client_name_filter(self.client["route_client_name"].lower())
        time.sleep(1)
        self.verify("Client Routes - entry found by Route Client Name in lower case",
                    True, clients_routes_tab.is_route_present())
        clients_wizard.click_on_close()
        clients_wizard.click_on_no_button()

        side_menu.open_client_list_page()
        client_lists_page.click_on_new()
        client_lists_wizard.click_on_plus()
        client_lists_wizard.set_client(self.client_list["client"])
        client_lists_wizard.click_on_checkmark()
        time.sleep(1)
        client_lists_wizard.set_client_filter(self.client_list["client"].lower())
        time.sleep(1)
        self.verify("Client List - entry found by Client in lower case",
                    True, client_lists_wizard.is_client_present())
        client_lists_wizard.set_client_filter(self.client_list["client"].upper())
        time.sleep(1)
        self.verify("Client List - entry found by Client in upper case",
                    True, client_lists_wizard.is_client_present())
