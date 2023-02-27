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


class QAP_T4003(CommonTestCase):
    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.condition_criteria = ['Venue', 'Client']
        self.venue = self.data_set.get_venue_by_name("venue_10")
        self.client = 'CLIENT1'
        self.condition_name = [''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6)) for _ in range(2)]
        self.default_result_name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.action = 'Reject'
        self.split = '100'

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        side_menu.click_on_order_management_rules_when_order_management_tab_is_open()

        page = MainPage(self.web_driver_container)
        values_tab = ValuesTab(self.web_driver_container)
        conditions_tab = ConditionsTab(self.web_driver_container)
        default_result = DefaultResultEntity(self.web_driver_container)
        wizard = MainWizard(self.web_driver_container)

        page.click_on_new_button()
        values_tab.set_name(self.name)
        conditions_tab.click_on_plus_button()
        conditions_tab.set_name(self.condition_name[0])
        conditions_tab.set_condition_criteria(self.condition_criteria[0])
        conditions_tab.set_condition_value(self.venue)
        conditions_tab.click_on_plus_button_at_result()
        conditions_tab.set_action(self.action)
        conditions_tab.set_split(self.split)
        conditions_tab.click_on_save_checkmark_at_result()
        conditions_tab.click_on_save_checkmark()
        default_result.click_on_edit_button()
        default_result.click_on_plus_button_at_result()
        default_result.set_action(self.action)
        default_result.set_split(self.split)
        default_result.click_on_save_checkmark_at_result()
        default_result.click_on_save_checkmark()
        wizard.click_on_save_changes()

    def test_context(self):
        wizard = MainWizard(self.web_driver_container)
        page = MainPage(self.web_driver_container)
        conditions_tab = ConditionsTab(self.web_driver_container)
        default_resul = DefaultResultEntity(self.web_driver_container)

        try:
            self.precondition()

            page.set_name_filter(self.name)
            time.sleep(1)
            page.click_on_more_actions()
            page.click_on_edit()

            conditions_tab.click_on_plus_button()
            conditions_tab.set_name(self.condition_name[1])
            conditions_tab.set_condition_criteria(self.condition_criteria[1])
            conditions_tab.set_condition_value(self.client)
            conditions_tab.click_on_plus_button_at_result()
            conditions_tab.set_action(self.action)
            conditions_tab.set_split(self.split)
            conditions_tab.click_on_save_checkmark_at_result()
            conditions_tab.click_on_save_checkmark()

            default_resul.click_on_edit_button()
            default_resul.set_name(self.default_result_name)
            default_resul.click_on_save_checkmark()
            wizard.click_on_save_changes()

            page.set_name_filter(self.name)
            time.sleep(1)
            page.click_on_more_actions()
            page.click_on_edit()

            conditions_tab.set_name_filter(self.condition_name[1])
            time.sleep(1)
            conditions_tab.click_on_edit_button()
            conditions_tab.click_on_edit_button_at_result()
            expected_result = [self.condition_name[1], self.condition_criteria[1], self.client, self.action, self.split]
            actual_result = [conditions_tab.get_name(), conditions_tab.get_condition_criteria(),
                             conditions_tab.get_condition_value(), conditions_tab.get_action(),
                             conditions_tab.get_split()]
            self.verify("New Condition saved correct", expected_result, actual_result)

            conditions_tab.click_on_cancel_button_at_result()
            conditions_tab.click_on_cancel_button()

            default_resul.click_on_edit_button()

            self.verify("Default result name changed", self.default_result_name, default_resul.get_name())

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
