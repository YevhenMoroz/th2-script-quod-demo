import random
import string
import time

from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.markets.venue_lists.main_page import VenueListsPage
from test_framework.web_admin_core.pages.markets.venue_lists.wizard import VenuesListsWizard
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T3450(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")

        self.name = "QAP-T3450"
        self.description = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.venue_list = ["USA", "BATS Dark Pool", "BINANCE"]

        self.new_name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.new_description = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.new_venue_list = ["COINBASE", "Dubai Financial Exchange"]

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        time.sleep(2)
        side_menu = SideMenu(self.web_driver_container)
        side_menu.open_venue_list_page()
        time.sleep(2)
        main_page = VenueListsPage(self.web_driver_container)
        main_page.set_name_filter(self.name)
        time.sleep(1)

        if not main_page.is_searched_venue_list_found(self.name):
            main_page.click_on_new()
            time.sleep(2)
            wizard_page = VenuesListsWizard(self.web_driver_container)
            wizard_page.set_name(self.name)
            wizard_page.set_description(self.description)
            wizard_page.set_venue_list(self.venue_list)
            wizard_page.click_on_save_changes()
            time.sleep(2)
            main_page.set_name_filter(self.name)
            time.sleep(1)

        main_page.click_on_more_actions()
        time.sleep(1)
        main_page.click_on_edit()
        time.sleep(2)

    def post_conditions(self):
        wizard_page = VenuesListsWizard(self.web_driver_container)
        wizard_page.set_name(self.name)
        wizard_page.set_description(self.description)
        wizard_page.set_venue_list(self.venue_list)
        wizard_page.set_venue_list(self.new_venue_list)
        wizard_page.click_on_save_changes()

    def test_context(self):
        main_page = VenueListsPage(self.web_driver_container)
        wizard_page = VenuesListsWizard(self.web_driver_container)

        self.precondition()

        wizard_page.set_name(self.new_name)
        wizard_page.set_description(self.new_description)
        wizard_page.set_venue_list(self.venue_list)
        wizard_page.set_venue_list(self.new_venue_list)
        wizard_page.click_on_save_changes()
        time.sleep(2)
        main_page.set_name_filter(self.new_name)
        time.sleep(1)
        main_page.click_on_more_actions()
        time.sleep(1)
        main_page.click_on_edit()
        time.sleep(2)

        actual_result = [wizard_page.get_name(), wizard_page.get_description()]
        for i in wizard_page.get_venue_list().split(","):
            actual_result.append(str(i).strip())
        excepted_result = [self.new_name, self.new_description]
        for i in self.new_venue_list:
            excepted_result.append(i)

        self.verify("Values saved correctly", actual_result, excepted_result)

        self.post_conditions()
