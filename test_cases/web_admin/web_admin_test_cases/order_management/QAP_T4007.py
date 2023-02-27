import random
import string
import sys

import traceback

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.login.login_page import LoginPage

from test_framework.web_admin_core.pages.order_management.order_management_rules.main_page import MainPage
from test_framework.web_admin_core.pages.order_management.order_management_rules.wizard import *
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T4007(CommonTestCase):
    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.venue = 'asd'
        self.condition_criteria = 'Venue'
        self.condition_name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.action = 'Reject'
        self.split = '100'

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        side_menu.click_on_execution_strategies_when_order_management_tab_is_open()
        page = MainPage(self.web_driver_container)
        page.click_on_new_button()

    def test_context(self):
        values_tab = ValuesTab(self.web_driver_container)
        conditions_tab = ConditionsTab(self.web_driver_container)
        wizard = MainWizard(self.web_driver_container)

        try:
            self.precondition()

            wizard.click_on_save_changes()
            time.sleep(1)
            expected_result = 'Incorrect or missing values'
            self.verify("Incorrect or missing values displayed - without any information", expected_result,
                        wizard.get_footer_error_text())

            values_tab.set_name(self.name)

            conditions_tab.click_on_plus_button()
            conditions_tab.set_name(self.condition_name)

            conditions_tab.click_on_plus_button_at_result()
            conditions_tab.set_action(self.action)
            conditions_tab.set_split(self.split)
            conditions_tab.click_on_save_checkmark_at_result()
            conditions_tab.click_on_add_condition_button()
            conditions_tab.set_condition_criteria(self.condition_criteria)
            conditions_tab.set_condition_value(self.venue)
            conditions_tab.click_on_save_checkmark()
            time.sleep(1)
            expected_result = 'Incorrect or missing conditional logic'
            self.verify("Incorrect or missing conditional logic displayed", expected_result,
                        wizard.get_footer_error_text())

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier without name",
                                              self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
