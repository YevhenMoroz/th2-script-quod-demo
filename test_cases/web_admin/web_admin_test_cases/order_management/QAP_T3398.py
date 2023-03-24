import sys
import time
import traceback
import random
import string

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.order_management.order_management_rules.main_page import MainPage
from test_framework.web_admin_core.pages.order_management.order_management_rules.wizard import *
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T3398(CommonTestCase):
    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.name = 'QAPT3398'
        self.description = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.condition_name = ['Cond1', 'Cond2']
        self.condition_criteria = "Client"
        self.client = self.data_set.get_client("client_2")
        self.action = 'Reject'
        self.percentage = '100'

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.set_login(self.login)
        login_page.set_password(self.password)
        login_page.click_login_button()
        side_menu = SideMenu(self.web_driver_container)
        side_menu.click_on_order_management_rules_when_order_management_tab_is_open()
        main_page = MainPage(self.web_driver_container)
        main_page.set_name_filter(self.name)
        time.sleep(1)
        if main_page.is_searched_entity_found(self.name):
            main_page.click_on_more_actions()
            main_page.click_on_edit()
        else:
            main_page.click_on_new_button()

            values_tab = ValuesTab(self.web_driver_container)
            values_tab.set_name(self.name)
            values_tab.set_description(self.description)
            conditions_tab = ConditionsTab(self.web_driver_container)
            conditions_tab.click_on_plus_button()
            conditions_tab.set_name(self.condition_name[0])
            conditions_tab.click_on_add_condition_button()
            conditions_tab.set_condition_criteria(self.condition_criteria)
            conditions_tab.set_condition_value(self.client)

            conditions_tab.click_on_plus_button_at_result()
            conditions_tab.set_action(self.action)
            conditions_tab.set_split(self.percentage)
            conditions_tab.click_on_save_checkmark_at_result()
            conditions_tab.click_on_save_checkmark()

            values_tab.set_name(self.name)
            values_tab.set_description(self.description)
            conditions_tab.click_on_plus_button()
            conditions_tab.set_name(self.condition_name[1])
            conditions_tab.click_on_add_condition_button()
            conditions_tab.set_condition_criteria(self.condition_criteria)
            conditions_tab.set_condition_value(self.client)

            conditions_tab.click_on_plus_button_at_result()
            conditions_tab.set_action(self.action)
            conditions_tab.set_split(self.percentage)
            conditions_tab.click_on_save_checkmark_at_result()
            conditions_tab.click_on_save_checkmark()

            default_result = DefaultResultEntity(self.web_driver_container)
            default_result.click_on_edit_button()
            default_result.click_on_plus_button_at_result()
            default_result.set_action(self.action)
            default_result.set_split(self.percentage)
            default_result.click_on_save_checkmark_at_result()
            default_result.click_on_save_checkmark()

            wizard = MainWizard(self.web_driver_container)
            wizard.click_on_save_changes()

            main_page.set_name_filter(self.name)
            time.sleep(1)
            main_page.click_on_more_actions()
            main_page.click_on_edit()

    def test_context(self):
        try:
            self.precondition()

            conditions_tab = ConditionsTab(self.web_driver_container)
            conditions_tab.click_on_toggle_button(True)
            time.sleep(3)
            self.verify(f"Condition {self.condition_name[0]} has been disable", False,
                        conditions_tab.is_condition_enabled())

            conditions_tab.click_on_toggle_button(True)
            time.sleep(3)
            self.verify(f"Condition {self.condition_name[0]} has been enable", True,
                        conditions_tab.is_condition_enabled())

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
