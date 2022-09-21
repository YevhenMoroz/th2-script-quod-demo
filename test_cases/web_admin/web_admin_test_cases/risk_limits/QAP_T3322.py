import sys
import time
import traceback
import random
import string

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.risk_limits.risk_limit_dimensions.main_page import MainPage
from test_framework.web_admin_core.pages.risk_limits.risk_limit_dimensions.wizard \
    import MainWizard, ValuesTab, DimensionsTab
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T3322(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")

        self.name = [''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6)) for _ in range(4)]
        self.cum_trading_limits = list
        self.clients = list
        self.desks = list
        self.venues = list
        self.client_list = list
        self.user = list
        self.sub_venues = list
        self.accounts = list
        self.listing_group = list
        self.listing = "USDT"
        self.account_dimensions = ["Clients", "ClientList", "Accounts"]
        self.user_dimension = ["Desks", "Users"]
        self.reference_data_dimension = ["Venue", "SubVenue", "Listing"]

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        time.sleep(2)
        side_menu = SideMenu(self.web_driver_container)
        side_menu.open_risk_limit_dimension_page()
        time.sleep(2)

    def post_conditions(self):
        for i in self.name:
            main_page = MainPage(self.web_driver_container)
            main_page.set_name_filter(i)
            time.sleep(1)
            main_page.click_on_more_actions()
            main_page.click_on_delete(True)
            time.sleep(1)

    def test_context(self):
        try:
            self.precondition()

            main_page = MainPage(self.web_driver_container)
            main_page.click_on_new_button()
            time.sleep(2)
            values_tab = ValuesTab(self.web_driver_container)
            values_tab.set_name(self.name[0])
            time.sleep(1)
            self.cum_trading_limits = values_tab.get_all_cum_trading_limits_from_drop_menu()
            values_tab.set_cum_trading_limits([random.choice(self.cum_trading_limits)])

            dimensions_tab = DimensionsTab(self.web_driver_container)
            dimensions_tab.set_accounts_dimension(self.account_dimensions[0])
            time.sleep(1)
            self.clients = dimensions_tab.get_all_clients_from_drop_menu()
            dimensions_tab.set_clients(random.choices(self.clients, k=2))
            time.sleep(1)
            dimensions_tab.set_users_dimension(self.user_dimension[0])
            time.sleep(1)
            self.desks = dimensions_tab.get_all_desks_from_drop_menu()
            dimensions_tab.set_desks([random.choice(self.desks)])
            dimensions_tab.set_reference_data_dimension(self.reference_data_dimension[0])
            time.sleep(1)
            self.venues = dimensions_tab.get_all_venues_from_drop_menu()
            dimensions_tab.set_venue(random.choice(self.venues))

            wizard = MainWizard(self.web_driver_container)
            wizard.click_on_save_changes()
            time.sleep(2)
            main_page.set_name_filter(self.name[0])
            time.sleep(1)
            self.verify("New entity has been create", True, main_page.is_searched_entity_found(self.name[0]))
#################
            main_page.click_on_new_button()
            time.sleep(2)
            values_tab = ValuesTab(self.web_driver_container)
            values_tab.set_name(self.name[1])
            values_tab.set_cum_trading_limits([random.choice(self.cum_trading_limits)])

            dimensions_tab = DimensionsTab(self.web_driver_container)
            dimensions_tab.set_accounts_dimension(self.account_dimensions[1])
            time.sleep(1)
            self.client_list = dimensions_tab.get_all_client_list_from_drop_menu()
            dimensions_tab.set_client_list(random.choice(self.client_list))
            dimensions_tab.set_users_dimension(self.user_dimension[1])
            time.sleep(1)
            self.user = dimensions_tab.get_all_user_from_drop_menu()
            dimensions_tab.set_user([random.choice(self.user)])
            dimensions_tab.set_reference_data_dimension(self.reference_data_dimension[1])
            time.sleep(1)
            self.sub_venues = dimensions_tab.get_all_sub_venues_from_drop_menu()
            dimensions_tab.set_sub_venue(random.choice(self.sub_venues))

            wizard = MainWizard(self.web_driver_container)
            wizard.click_on_save_changes()
            time.sleep(2)
            main_page.set_name_filter(self.name[1])
            time.sleep(1)
            self.verify("New entity has been create", True, main_page.is_searched_entity_found(self.name[1]))
###################
            main_page.click_on_new_button()
            time.sleep(2)
            values_tab = ValuesTab(self.web_driver_container)
            values_tab.set_name(self.name[2])
            values_tab.set_cum_trading_limits([random.choice(self.cum_trading_limits)])

            dimensions_tab = DimensionsTab(self.web_driver_container)
            dimensions_tab.set_accounts_dimension(self.account_dimensions[2])
            time.sleep(1)
            self.accounts = dimensions_tab.get_all_accounts_from_drop_menu()
            dimensions_tab.set_accounts([random.choice(self.accounts)])
            time.sleep(1)
            dimensions_tab.set_users_dimension(self.user_dimension[1])
            dimensions_tab.set_user([random.choice(self.user)])
            dimensions_tab.set_reference_data_dimension(self.reference_data_dimension[1])
            time.sleep(1)
            self.sub_venues = dimensions_tab.get_all_sub_venues_from_drop_menu()
            dimensions_tab.set_sub_venue(random.choice(self.sub_venues))

            wizard = MainWizard(self.web_driver_container)
            wizard.click_on_save_changes()
            time.sleep(2)
            main_page.set_name_filter(self.name[2])
            time.sleep(1)
            self.verify("New entity has been create", True, main_page.is_searched_entity_found(self.name[2]))
###############
            main_page.click_on_new_button()
            time.sleep(2)
            values_tab = ValuesTab(self.web_driver_container)
            values_tab.set_name(self.name[3])
            values_tab.set_cum_trading_limits([random.choice(self.cum_trading_limits)])

            dimensions_tab = DimensionsTab(self.web_driver_container)
            dimensions_tab.set_accounts_dimension(self.account_dimensions[2])
            dimensions_tab.set_accounts([random.choice(self.accounts)])
            time.sleep(1)
            dimensions_tab.set_users_dimension(self.user_dimension[1])
            dimensions_tab.set_user([random.choice(self.user)])
            dimensions_tab.set_reference_data_dimension(self.reference_data_dimension[2])
            dimensions_tab.set_listing(self.listing)

            wizard = MainWizard(self.web_driver_container)
            wizard.click_on_save_changes()
            time.sleep(2)
            main_page.set_name_filter(self.name[3])
            time.sleep(1)
            self.verify("New entity has been create", True, main_page.is_searched_entity_found(self.name[3]))

            self.post_conditions()

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
