import random
import string
import sys
import time
import traceback

from custom import basic_custom_actions
from test_cases.web_admin.web_admin_core.pages.login.login_page import LoginPage
from test_cases.web_admin.web_admin_core.pages.order_management.execution_strategies.execution_strategies_dark_sub_wizard import \
    ExecutionStrategiesDarkSubWizard
from test_cases.web_admin.web_admin_core.pages.order_management.execution_strategies.execution_strategies_lit_dark_sub_wizard import \
    ExecutionStrategiesLitDarkSubWizard
from test_cases.web_admin.web_admin_core.pages.order_management.execution_strategies.execution_strategies_page import \
    ExecutionStrategiesPage
from test_cases.web_admin.web_admin_core.pages.order_management.execution_strategies.execution_strategies_wizard import \
    ExecutionStrategiesWizard
from test_cases.web_admin.web_admin_core.pages.root.side_menu import SideMenu
from test_cases.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_2961(CommonTestCase):
    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id)
        self.name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.user = "QA1"
        self.strategy_type = "Quod LitDark"
        self.parameter_at_lit_dark_block = "Max Dark Percentage"
        self.value = "120"

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.set_login("adm03")
        login_page.set_password("adm03")
        login_page.click_login_button()
        login_page.check_is_login_successful()
        side_menu = SideMenu(self.web_driver_container)
        side_menu.open_execution_strategies_page()
        main_menu = ExecutionStrategiesPage(self.web_driver_container)
        main_menu.click_on_new_button()
        strategies_wizard = ExecutionStrategiesWizard(self.web_driver_container)
        time.sleep(1)
        strategies_wizard.set_name(self.name)
        time.sleep(1)
        strategies_wizard.set_user(self.user)
        strategies_wizard.set_strategy_type(self.strategy_type)
        strategies_wizard.click_on_lit_dark()
        lit_dark_block = ExecutionStrategiesLitDarkSubWizard(self.web_driver_container)
        lit_dark_block.click_on_plus_button()
        lit_dark_block.set_parameter(self.parameter_at_lit_dark_block)
        lit_dark_block.set_value(self.value)
        lit_dark_block.click_on_checkmark_button()
        lit_dark_block.click_on_go_back_button()
        strategies_wizard.click_on_save_changes()
        main_menu.set_name_at_filter_field(self.name)
        time.sleep(2)
        main_menu.click_on_more_actions()
        main_menu.click_on_edit_at_more_actions()

    def test_context(self):
        try:
            self.precondition()
            main_menu = ExecutionStrategiesPage(self.web_driver_container)
            strategies_wizard = ExecutionStrategiesWizard(self.web_driver_container)
            expected_parameter_and_value_at_dark_block = ["MaxDarkPercentage: ", self.value]
            actual_parameter_and_value_at_dark_block = [strategies_wizard.get_parameter_name_at_lit_dark_block(),
                                                        strategies_wizard.get_parameter_value_at_lit_dark_block()]
            self.verify("After saved at Lit Dark block", expected_parameter_and_value_at_dark_block,
                        actual_parameter_and_value_at_dark_block)
            strategies_wizard.click_on_save_changes()
            main_menu.set_enabled_at_filter_field("true")
            main_menu.set_name_at_filter_field(self.name)
            time.sleep(2)
            main_menu.click_on_enable_disable_button()
            main_menu.click_on_ok_button()
        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
