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


class QAP_T3995(CommonTestCase):
    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.condition_name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.default_result_name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.action = 'Reject'
        self.split = '100'
        self.order_quantity = '1'

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        side_menu.open_order_management_rules_page()
        page = MainPage(self.web_driver_container)
        page.click_on_new_button()

    def test_context(self):
        condition_tab = ConditionsTab(self.web_driver_container)
        default_result = DefaultResultEntity(self.web_driver_container)
        values_tab = ValuesTab(self.web_driver_container)
        wizard = MainWizard(self.web_driver_container)

        try:
            self.precondition()

            values_tab.set_name(self.name)
            condition_tab.click_on_plus_button()
            condition_tab.set_name(self.condition_name)
            condition_tab.click_on_add_condition_button()
            condition_tab.set_condition_value(self.order_quantity)
            condition_tab.click_on_plus_button_at_result()
            condition_tab.set_action(self.action)
            condition_tab.set_split(self.split)
            condition_tab.click_on_save_checkmark_at_result()
            condition_tab.click_on_save_checkmark()

            wizard.click_on_save_changes()
            time.sleep(1)
            expected_result = "Default result is required"
            self.verify("Rule not saved, warning appears", expected_result, wizard.get_footer_error_text())

            default_result.click_on_edit_button()
            default_result.set_name(self.default_result_name)
            default_result.click_on_save_checkmark()
            time.sleep(1)
            expected_result = "No results have added"
            self.verify("Rule not saved, warning appears", expected_result, wizard.get_footer_error_text())

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier without name",
                                              self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
