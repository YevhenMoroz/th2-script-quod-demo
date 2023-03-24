import random
import string
import sys
import time
import traceback

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.order_management.order_management_rules.main_page import MainPage
from test_framework.web_admin_core.pages.order_management.order_management_rules.wizard import *
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T3818(CommonTestCase):
    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.venue = self.data_set.get_venue_by_name("venue_10")
        self.condition_name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        side_menu.open_order_management_rules_page()

    def test_context(self):
        main_page = MainPage(self.web_driver_container)
        condition_tab = ConditionsTab(self.web_driver_container)
        wizard = MainWizard(self.web_driver_container)

        try:
            self.precondition()

            main_page.click_on_more_actions()
            main_page.click_on_edit()

            result = condition_tab.is_condition_enabled()

            condition_tab.click_on_toggle_button(True)
            wizard.click_on_save_changes()

            main_page.click_on_more_actions()
            main_page.click_on_edit()

            self.verify("Condition has been changed", True, result != condition_tab.is_condition_enabled())

            condition_tab.click_on_toggle_button(True)
            wizard.click_on_save_changes()

            main_page.click_on_more_actions()
            main_page.click_on_edit()

            self.verify("Condition has been changed", True, result == condition_tab.is_condition_enabled())

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
