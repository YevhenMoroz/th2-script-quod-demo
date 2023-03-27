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


class QAP_T3687(CommonTestCase):
    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.rule_name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.condition_name = ['test1', 'test2']
        self.split = ['100', '50']
        self.condition_criteria = 'Venue'
        self.venue = self.data_set.get_venue_by_name("venue_10")
        self.action = ['Reject', 'SendDirect', 'SendCare']

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        main_page = MainPage(self.web_driver_container)
        conditions_tab = ConditionsTab(self.web_driver_container)
        values_tab = ValuesTab(self.web_driver_container)
        wizard = MainWizard(self.web_driver_container)
        side_menu = SideMenu(self.web_driver_container)
        default_result = DefaultResultEntity(self.web_driver_container)

        login_page.login_to_web_admin(self.login, self.password)
        side_menu.click_on_order_management_rules_when_order_management_tab_is_open()

        main_page.click_on_new_button()
        values_tab.set_name(self.rule_name)
        conditions_tab.click_on_plus_button()
        conditions_tab.set_name(self.rule_name)
        conditions_tab.click_on_add_condition_button()
        conditions_tab.set_condition_criteria(self.condition_criteria)
        conditions_tab.set_condition_value(self.venue)

        conditions_tab.click_on_plus_button_at_result()
        conditions_tab.set_action(self.action[0])
        conditions_tab.set_split(self.split[0])
        conditions_tab.click_on_save_checkmark_at_result()
        conditions_tab.click_on_save_checkmark()

        default_result.click_on_edit_button()
        default_result.click_on_plus_button_at_result()
        default_result.set_action(self.action[0])
        default_result.set_split(self.split[0])
        default_result.click_on_save_checkmark_at_result()
        default_result.click_on_save_checkmark()
        wizard.click_on_save_changes()

    def test_context(self):
        main_page = MainPage(self.web_driver_container)
        conditions_tab = ConditionsTab(self.web_driver_container)
        wizard = MainWizard(self.web_driver_container)
        try:
            self.precondition()

            main_page.set_name_filter(self.rule_name)
            time.sleep(1)
            main_page.click_on_more_actions()
            main_page.click_on_edit()

            conditions_tab.click_on_plus_button()
            conditions_tab.set_name(self.condition_name[0])
            conditions_tab.click_on_add_condition_button()
            conditions_tab.set_condition_criteria(self.condition_criteria)
            conditions_tab.set_condition_value(self.venue)

            conditions_tab.click_on_plus_button_at_result()
            conditions_tab.set_action(self.action[1])
            conditions_tab.set_split(self.split[0])
            conditions_tab.click_on_save_checkmark_at_result()
            conditions_tab.click_on_save_checkmark()

            conditions_tab.click_on_plus_button()
            conditions_tab.set_name(self.condition_name[1])
            conditions_tab.click_on_add_condition_button()
            conditions_tab.set_condition_criteria(self.condition_criteria)
            conditions_tab.set_condition_value(self.venue)
            conditions_tab.click_on_plus_button_at_result()
            conditions_tab.set_action(self.action[2])
            conditions_tab.set_split(self.split[0])
            conditions_tab.click_on_save_checkmark_at_result()
            conditions_tab.click_on_save_checkmark()

            conditions_tab.set_name_filter(self.condition_name[1])
            time.sleep(1)
            conditions_tab.click_on_edit_button()
            conditions_tab.click_on_edit_button_at_result()
            conditions_tab.set_split(self.split[1])
            conditions_tab.click_on_save_checkmark_at_result()
            conditions_tab.click_on_plus_button_at_result()
            conditions_tab.set_action(self.action[1])
            conditions_tab.set_split(self.split[1])
            conditions_tab.click_on_save_checkmark_at_result()
            conditions_tab.click_on_save_checkmark()
            wizard.click_on_save_changes()

            main_page.set_name_filter(self.rule_name)
            time.sleep(1)
            main_page.click_on_more_actions()
            main_page.click_on_edit()
            conditions_tab.set_name_filter(self.condition_name[1])
            time.sleep(0.5)
            actual_result = []
            conditions_tab.click_on_edit_button()
            conditions_tab.set_action_filter(self.action[1])
            time.sleep(0.5)
            conditions_tab.click_on_edit_button_at_result()
            actual_result.append(conditions_tab.get_action())
            actual_result.append(conditions_tab.get_split())
            conditions_tab.click_on_cancel_button_at_result()
            conditions_tab.set_action_filter(self.action[2])
            time.sleep(0.5)
            conditions_tab.click_on_edit_button_at_result()
            actual_result.append(conditions_tab.get_action())
            actual_result.append(conditions_tab.get_split())
            conditions_tab.click_on_cancel_button_at_result()

            expected_result = [self.action[1], self.split[1], self.action[2], self.split[1]]

            self.verify("After edited, Conditions have another values", expected_result, actual_result)

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
