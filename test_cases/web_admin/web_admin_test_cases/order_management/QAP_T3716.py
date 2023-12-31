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


class QAP_T3716(CommonTestCase):
    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.action = 'SendDirect'
        self.split = "100"
        self.route = 'ESDEMO'

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        side_menu.click_on_order_management_rules_tab()
        page = MainPage(self.web_driver_container)
        page.click_on_new_button()

    def test_context(self):
        conditions_tab = ConditionsTab(self.web_driver_container)
        default_result = DefaultResultEntity(self.web_driver_container)

        try:
            self.precondition()

            conditions_tab.click_on_plus_button()
            conditions_tab.click_on_plus_button_at_result()
            conditions_tab.set_action(self.action)
            conditions_tab.set_split(self.split)
            conditions_tab.set_route(self.route)
            conditions_tab.click_on_save_checkmark_at_result()
            time.sleep(0.5)
            conditions_tab.click_on_edit_button_at_result()
            self.verify("Route field contains correct data", self.route, conditions_tab.get_route())
            conditions_tab.click_on_cancel_button()

            default_result.click_on_edit_button()
            default_result.click_on_plus_button_at_result()
            default_result.set_action(self.action)
            default_result.set_split(self.split)
            default_result.set_route(self.route)
            default_result.click_on_save_checkmark_at_result()
            time.sleep(0.5)
            default_result.click_on_edit_button_at_result()
            self.verify("Route field contains correct data for Default Result", self.route, conditions_tab.get_route())

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier without name",
                                              self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
