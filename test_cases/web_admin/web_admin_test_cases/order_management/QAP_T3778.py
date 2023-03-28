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


class QAP_T3778(CommonTestCase):
    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.description = 'test' + ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.condition_name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.condition_criteria = 'Venue'
        self.venue = 'BINANCE'
        self.action = 'Reject'
        self.split = '100'

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        side_menu.click_on_order_management_rules_when_order_management_tab_is_open()

    def create_new_rule(self):
        main_page = MainPage(self.web_driver_container)
        values_tab = ValuesTab(self.web_driver_container)
        condition_tab = ConditionsTab(self.web_driver_container)
        default_result = DefaultResultEntity(self.web_driver_container)
        wizard = MainWizard(self.web_driver_container)

        main_page.click_on_new_button()
        values_tab.set_name(self.name)
        values_tab.set_description(self.description)
        condition_tab.click_on_plus_button()
        condition_tab.set_name(self.condition_name)
        condition_tab.click_on_add_condition_button()
        condition_tab.set_condition_criteria(self.condition_criteria)
        condition_tab.set_condition_value(self.venue)
        condition_tab.click_on_plus_button_at_result()
        condition_tab.set_action(self.action)
        condition_tab.set_split(self.split)
        condition_tab.click_on_save_checkmark_at_result()
        condition_tab.click_on_save_checkmark()

        default_result.click_on_edit_button()
        default_result.click_on_plus_button_at_result()
        default_result.set_action(self.action)
        default_result.set_split(self.split)
        default_result.click_on_save_checkmark_at_result()
        default_result.click_on_save_checkmark()
        wizard.click_on_save_changes()

    def test_context(self):
        main_page = MainPage(self.web_driver_container)
        condition_tab = ConditionsTab(self.web_driver_container)

        try:
            self.precondition()

            self.create_new_rule()
            main_page.set_name_filter(self.name)
            time.sleep(1)
            main_page.click_on_toggle_button(True)
            time.sleep(10)
            self.create_new_rule()
            main_page.set_name_filter(self.name)
            time.sleep(1)
            actual_result = main_page.get_all_names()
            self.verify("The same entities created", 2, len(actual_result))

            main_page.set_enabled_filter('true')
            time.sleep(0.5)
            main_page.click_on_more_actions()
            main_page.click_on_edit()
            condition_tab.click_on_edit_button()
            time.sleep(0.5)

            self.verify("Enabled entity can be edit", self.condition_name, condition_tab.get_name())

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
