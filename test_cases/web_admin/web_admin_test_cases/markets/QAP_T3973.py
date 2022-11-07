import random
import string
import sys
import time
import traceback

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.markets.routes.main_page import RoutesPage
from test_framework.web_admin_core.pages.markets.routes.wizard import RoutesWizard
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T3973(CommonTestCase):
    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.set_login(self.login)
        login_page.set_password(self.password)
        login_page.click_login_button()
        login_page.check_is_login_successful()
        side_menu = SideMenu(self.web_driver_container)
        side_menu.open_routes_page()
        time.sleep(2)
        routes_main_menu = RoutesPage(self.web_driver_container)
        routes_main_menu.click_on_new_button()
        time.sleep(2)
        routes_wizard = RoutesWizard(self.web_driver_container)
        routes_wizard.click_on_save_changes()

    def test_context(self):
        try:
            self.precondition()
            routes_wizard = RoutesWizard(self.web_driver_container)
            self.verify("Error after click on next button", "Incorrect or missing values",
                        routes_wizard.get_actual_error_after_click_on_next_in_empty_page())
            time.sleep(3)
            routes_wizard.set_name_at_values_tab(self.name)
            time.sleep(2)
            routes_wizard.click_on_save_changes()
            time.sleep(2)
            routes_main_menu = RoutesPage(self.web_driver_container)
            routes_main_menu.set_name_at_filter(self.name)
            time.sleep(2)
            self.verify("Correctly name saved", self.name, routes_main_menu.get_name_value())
            time.sleep(1)
            routes_main_menu.click_on_more_actions()
            routes_main_menu.click_on_delete_at_more_actions()
        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
