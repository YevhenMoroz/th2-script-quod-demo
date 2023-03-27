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


class QAP_T3886(CommonTestCase):
    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.condition_name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.condition_criteria = 'Client'
        self.conditional_logic = 'NOT IN'
        self.action = 'Reject'
        self.client = ['QUODAH', 'CLIENT1']
        self.split = '100'

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        side_menu.open_order_management_rules_page()
    
    def test_context(self):
        main_page = MainPage(self.web_driver_container)
        condition_tab = ConditionsTab(self.web_driver_container)

        try:
            self.precondition()
            
            main_page.click_on_new_button()
            
            condition_tab.click_on_plus_button()
            condition_tab.set_name(self.condition_name)
            condition_tab.click_on_add_condition_button()
            condition_tab.set_condition_criteria(self.condition_criteria)
            condition_tab.set_condition_logic(self.conditional_logic)
            condition_tab.set_condition_value(self.client)
            condition_tab.click_on_plus_button_at_result()
            condition_tab.set_action(self.action)
            condition_tab.set_split(self.split)
            condition_tab.click_on_save_checkmark_at_result()
            condition_tab.click_on_save_checkmark()
            time.sleep(1)
            condition_tab.click_on_edit_button()

            expected_result = self.client
            actual_result = condition_tab.get_condition_value()

            self.verify("Clients has been add", expected_result, actual_result)

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
