import sys
import time
import traceback
import string
import random

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.order_management.execution_strategies.execution_strategies_lit_general_sub_wizard import \
    ExecutionStrategiesLitGeneralSubWizard
from test_framework.web_admin_core.pages.order_management.execution_strategies.execution_strategies_page import \
    ExecutionStrategiesPage
from test_framework.web_admin_core.pages.order_management.execution_strategies.execution_strategies_wizard import \
    ExecutionStrategiesWizard
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T3923(CommonTestCase):
    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.user = self.data_set.get_user("user_8")
        self.strategy_type = self.data_set.get_strategy_type("strategy_type_1")
        self.parameter = "SprayModify"
        self.first_value = "Single"
        self.second_value = "Spray"

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.set_login(self.login)
        login_page.set_password(self.password)
        login_page.click_login_button()
        login_page.check_is_login_successful()
        side_menu = SideMenu(self.web_driver_container)
        side_menu.open_execution_strategies_page()
        main_menu = ExecutionStrategiesPage(self.web_driver_container)
        main_menu.click_on_new_button()
        strategies_wizard = ExecutionStrategiesWizard(self.web_driver_container)
        strategies_wizard.set_name(self.name)
        strategies_wizard.set_strategy_type(self.strategy_type)
        strategies_wizard.set_user(self.user)
        strategies_wizard.click_on_lit_general()
        general_at_lit_block = ExecutionStrategiesLitGeneralSubWizard(self.web_driver_container)
        general_at_lit_block.click_on_plus_button()
        general_at_lit_block.set_parameter(self.parameter)
        general_at_lit_block.set_value_by_dropdown_list_at_sub_wizard(self.first_value)
        general_at_lit_block.click_on_checkmark_button()
        general_at_lit_block.click_on_edit_button()
        general_at_lit_block.set_value_by_dropdown_list_at_sub_wizard(self.second_value)
        general_at_lit_block.set_visible_checkbox()
        general_at_lit_block.click_on_checkmark_button()
        general_at_lit_block.click_on_go_back_button()

    def test_context(self):
        try:
            self.precondition()
            main_menu = ExecutionStrategiesPage(self.web_driver_container)
            strategies_wizard = ExecutionStrategiesWizard(self.web_driver_container)
            expected_parameter_and_value_at_lit_general_block = ["SprayModify: ", self.second_value]
            actual_parameter_and_value_at_lit_general_block = [
                strategies_wizard.get_parameter_name_at_lit_general_block(),
                strategies_wizard.get_parameter_value_at_lit_general_block()]
            self.verify("After saved at Lit General block", expected_parameter_and_value_at_lit_general_block,
                        actual_parameter_and_value_at_lit_general_block)
            strategies_wizard.click_on_save_changes()
            main_menu.set_name_at_filter_field(self.name)
            time.sleep(1)
            main_menu.click_on_enable_disable_button()
            main_menu.click_on_ok_button()
        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
