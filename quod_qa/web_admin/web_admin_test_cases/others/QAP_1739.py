import random
import string
import time
import traceback

from custom import basic_custom_actions
from quod_qa.web_admin.web_admin_core.pages.login.login_page import LoginPage
from quod_qa.web_admin.web_admin_core.pages.others.routes.routes_page import RoutesPage
from quod_qa.web_admin.web_admin_core.pages.others.routes.routes_venues_subwizard import RoutesVenuesSubWizard
from quod_qa.web_admin.web_admin_core.pages.others.routes.routes_wizard import RoutesWizard
from quod_qa.web_admin.web_admin_core.pages.root.side_menu import SideMenu
from quod_qa.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer
from quod_qa.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_1739(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id)
        self.name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.first_venue = "EURONEXT AMSTERDAM"
        self.second_venue = "AMERICAN STOCK EXCHANGE"

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.set_login("adm07")
        login_page.set_password("adm07")
        login_page.click_login_button()
        login_page.check_is_login_successful()
        side_menu = SideMenu(self.web_driver_container)
        side_menu.open_routes_page()
        time.sleep(2)
        routes_main_menu = RoutesPage(self.web_driver_container)
        routes_main_menu.click_on_new_button()
        routes_wizard = RoutesWizard(self.web_driver_container)
        time.sleep(2)
        routes_wizard.set_name_at_values_tab(self.name)
        time.sleep(2)
        venues_sub_wizard = RoutesVenuesSubWizard(self.web_driver_container)
        # create two new venues

        venues_sub_wizard.click_on_plus_at_venues_tab()
        venues_sub_wizard.set_venue_at_venues_tab(self.first_venue)
        venues_sub_wizard.click_on_check_mark_at_venues_tab()
        venues_sub_wizard.click_on_plus_at_venues_tab()
        venues_sub_wizard.set_venue_at_venues_tab(self.second_venue)
        venues_sub_wizard.click_on_check_mark_at_venues_tab()
        venues_sub_wizard.set_venue_filter_at_venues_tab(self.second_venue)
        time.sleep(2)
        venues_sub_wizard.click_on_edit_at_venues_tab()

    def test_context(self):
        try:
            self.precondition()
            venues_sub_wizard = RoutesVenuesSubWizard(self.web_driver_container)
            self.verify("New venue", self.second_venue, venues_sub_wizard.get_venue_at_venues_tab())
            venues_sub_wizard.click_on_check_mark_at_venues_tab()
            time.sleep(1)
            routes_wizard = RoutesWizard(self.web_driver_container)
            routes_wizard.click_on_save_changes()
            routes_main_menu = RoutesPage(self.web_driver_container)
            time.sleep(2)
            routes_main_menu.set_name_at_filter(self.name)
            time.sleep(2)
            self.verify("After saved", self.name, routes_main_menu.get_name_value())
            time.sleep(1)
            routes_main_menu.click_on_more_actions()
            time.sleep(1)
            routes_main_menu.click_on_delete_at_more_actions()
        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            print(traceback.format_exc() + " Search in ->  " + self.__class__.__name__)
