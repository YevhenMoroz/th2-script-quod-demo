import sys
import string
import random
import time
import traceback

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.order_management.execution_strategies.execution_strategies_lit_dark_sub_wizard import \
    ExecutionStrategiesLitDarkSubWizard
from test_framework.web_admin_core.pages.order_management.execution_strategies.execution_strategies_page import \
    ExecutionStrategiesPage
from test_framework.web_admin_core.pages.order_management.execution_strategies.execution_strategies_wizard import \
    ExecutionStrategiesWizard
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T7930(CommonTestCase):
    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.user = self.data_set.get_user("user_8")
        self.strategy_type = self.data_set.get_strategy_type("strategy_type_3")
        self.parameter = 'DarkPoolMode'
        self.parameter_mode = 'RoundRobin'
        self.second_parameter = 'DarkLimitPx'
        self.qty = random.randint(10, 100)

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.set_login(self.login)
        login_page.set_password(self.password)
        login_page.click_login_button()
        login_page.check_is_login_successful()
        side_menu = SideMenu(self.web_driver_container)
        side_menu.open_execution_strategies_page()
        side_menu.wait_for_button_to_become_active()

    def test_context(self):
        try:
            self.precondition()

            main_page = ExecutionStrategiesPage(self.web_driver_container)
            main_page.click_on_new_button()
            strategies_wizard = ExecutionStrategiesWizard(self.web_driver_container)
            strategies_wizard.set_user(self.user)
            strategies_wizard.set_name(self.name)
            strategies_wizard.set_strategy_type(self.strategy_type)
            strategies_wizard.click_on_dark_block()
            lit_dark_block = ExecutionStrategiesLitDarkSubWizard(self.web_driver_container)
            lit_dark_block.click_on_plus_button()
            lit_dark_block.set_parameter(self.parameter)
            lit_dark_block.set_value_by_dropdown_list_at_sub_wizard(self.parameter_mode)
            lit_dark_block.click_on_checkmark_button()
            lit_dark_block.click_on_go_back_button()
            strategies_wizard.click_on_save_changes()

            main_page.set_name_at_filter_field(self.name)
            time.sleep(1)
            main_page.click_on_more_actions()
            main_page.click_on_edit_at_more_actions()
            strategies_wizard.click_on_dark_block()
            lit_dark_block.click_on_delete_button()

            lit_dark_block.click_on_plus_button()
            lit_dark_block.set_parameter(self.parameter)
            lit_dark_block.set_value_by_dropdown_list_at_sub_wizard(self.parameter_mode)
            lit_dark_block.click_on_checkmark_button()

            lit_dark_block.click_on_plus_button()
            lit_dark_block.set_parameter(self.second_parameter)
            lit_dark_block.set_value(self.qty)
            lit_dark_block.click_on_checkmark_button()

            lit_dark_block.click_on_go_back_button()
            strategies_wizard.click_on_save_changes()

            main_page.set_name_at_filter_field(self.name)
            time.sleep(1)
            main_page.click_on_more_actions()
            main_page.click_on_edit_at_more_actions()

            expected_parameter_and_value_at_dark_block = [f"{self.parameter}: ", f"{self.parameter_mode}",
                                                          f"{self.second_parameter}: ", f"{self.qty}"]
            strategies_wizard = ExecutionStrategiesWizard(self.web_driver_container)
            actual_parameter_and_value_at_dark_block = [strategies_wizard.get_parameter_name_at_dark_block(),
                                                        strategies_wizard.get_parameter_value_at_dark_block()]
            self.verify("After edit", expected_parameter_and_value_at_dark_block,
                        actual_parameter_and_value_at_dark_block)

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
