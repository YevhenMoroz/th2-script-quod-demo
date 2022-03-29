import sys
import time
import traceback
import random
import string

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.order_management.order_management_rules.order_management_rules_page import OrderManagementRulesPage
from test_framework.web_admin_core.pages.order_management.order_management_rules.order_management_rules_wizard import OrderManagementRulesWizard
from test_framework.web_admin_core.pages.order_management.order_management_rules.order_management_rules_values_sub_wizard import OrderManagementRulesValuesSubWizard
from test_framework.web_admin_core.pages.order_management.order_management_rules.order_management_rules_conditions_sub_wizard import OrderManagementRulesConditionsSubWizard
from test_framework.web_admin_core.pages.order_management.order_management_rules.order_management_rules_default_result_sub_wizard import OrderManagementRulesDefaultResultSubWizard
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_6725(CommonTestCase):
    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.description = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.condition_name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.default_result_name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.condition_logic_value = "Client"
        self.client = "CLIENT2"
        self.exec_policy = 'DMA'
        self.percentage = "100"

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.set_login(self.login)
        login_page.set_password(self.password)
        login_page.click_login_button()
        time.sleep(2)
        side_menu = SideMenu(self.web_driver_container)
        side_menu.open_order_management_rules_page()
        time.sleep(2)
        order_management_page = OrderManagementRulesPage(self.web_driver_container)
        order_management_page.click_on_new_button()
        order_management_value_tab = OrderManagementRulesValuesSubWizard(self.web_driver_container)
        order_management_value_tab.set_name(self.name)
        order_management_value_tab.set_description(self.description)
        order_management_value_tab.set_client(self.client)
        order_management_conditions_tab = OrderManagementRulesConditionsSubWizard(self.web_driver_container)
        order_management_conditions_tab.click_on_plus()
        order_management_conditions_tab.set_name(self.condition_name)
        time.sleep(1)
        order_management_conditions_tab.click_on_add_condition()
        time.sleep(1)
        order_management_conditions_tab.set_right_side_list_at_conditional_logic(self.condition_logic_value)
        order_management_conditions_tab.set_right_side_at_conditional_logic(self.client)

        order_management_conditions_tab.click_on_plus_at_results_sub_wizard()
        time.sleep(1)
        order_management_conditions_tab.set_exec_policy(self.exec_policy)
        time.sleep(1)
        order_management_conditions_tab.set_percentage(self.percentage)
        time.sleep(1)
        order_management_conditions_tab.click_on_checkmark_at_results_sub_wizard()
        time.sleep(1)
        order_management_conditions_tab.click_on_checkmark()
        time.sleep(1)
        order_management_default_result = OrderManagementRulesDefaultResultSubWizard(self.web_driver_container)
        order_management_default_result.set_default_result_name(self.default_result_name)
        time.sleep(1)
        order_management_default_result.click_on_plus()
        time.sleep(1)
        order_management_default_result.set_exec_policy(self.exec_policy)
        time.sleep(1)
        order_management_default_result.set_percentage(self.percentage)
        time.sleep(1)
        order_management_default_result.click_on_checkmark()
        order_management_wizard = OrderManagementRulesWizard(self.web_driver_container)
        order_management_wizard.click_on_save_changes()

    def test_context(self):
        try:
            self.precondition()

            order_management_page = OrderManagementRulesPage(self.web_driver_container)
            order_management_page.set_name_filter(self.name)
            time.sleep(1)
            order_management_page.click_on_more_actions()
            time.sleep(1)
            order_management_page.click_on_edit_at_more_actions()

            order_management_conditions_tab = OrderManagementRulesConditionsSubWizard(self.web_driver_container)
            order_management_conditions_tab.click_on_enabled_disable(True)
            self.verify("Condition btn has been disable", False,
                        order_management_conditions_tab.is_condition_button_enable_disable())
            time.sleep(2)
            order_management_conditions_tab.click_on_enabled_disable(True)
            self.verify("Condition btn has been enable", True,
                        order_management_conditions_tab.is_condition_button_enable_disable())

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)