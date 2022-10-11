import random
import string
import sys
import time
import traceback

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.order_management.execution_strategies.execution_strategies_dark_sub_wizard import \
    ExecutionStrategiesDarkSubWizard
from test_framework.web_admin_core.pages.order_management.execution_strategies.execution_strategies_lit_general_sub_wizard import \
    ExecutionStrategiesLitGeneralSubWizard
from test_framework.web_admin_core.pages.order_management.execution_strategies.execution_strategies_page import \
    ExecutionStrategiesPage
from test_framework.web_admin_core.pages.order_management.execution_strategies.execution_strategies_wizard import \
    ExecutionStrategiesWizard
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T3863(CommonTestCase):
    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.user = self.data_set.get_user("user_8")
        self.strategy_type = self.data_set.get_strategy_type("strategy_type_3")
        self.parameter_at_dark_block = "DarkBrokerStrategies"
        self.first_strategy = "TestSuperStrategy1"
        self.first_value = "2"
        self.second_strategy = "test1582"
        self.second_value = "1"

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.set_login(self.login)
        login_page.set_password(self.password)
        login_page.click_login_button()
        login_page.check_is_login_successful()
        side_menu = SideMenu(self.web_driver_container)
        side_menu.open_execution_strategies_page()
        side_menu.wait_for_button_to_become_active()
        main_menu = ExecutionStrategiesPage(self.web_driver_container)
        main_menu.click_on_new_button()
        time.sleep(2)
        strategies_wizard = ExecutionStrategiesWizard(self.web_driver_container)
        strategies_wizard.set_name(self.name)
        time.sleep(2)
        strategies_wizard.set_user(self.user)
        strategies_wizard.set_strategy_type(self.strategy_type)
        strategies_wizard.click_on_dark_block()
        dark_block = ExecutionStrategiesDarkSubWizard(self.web_driver_container)
        dark_block.click_on_plus_button()
        dark_block.set_parameter(self.parameter_at_dark_block)
        dark_block.click_on_plus_at_actions_sub_wizard()
        time.sleep(1)
        dark_block.set_strategy_at_actions_sub_wizard(self.first_strategy)
        dark_block.set_value_at_actions_sub_wizard(self.first_value)
        dark_block.click_on_checkmark_at_actions_sub_wizard()
        dark_block.click_on_plus_at_actions_sub_wizard()
        time.sleep(1)
        dark_block.set_strategy_at_actions_sub_wizard(self.second_strategy)
        dark_block.set_value_at_actions_sub_wizard(self.second_value)
        dark_block.click_on_checkmark_at_actions_sub_wizard()
        dark_block.click_on_checkmark_button()

    def test_context(self):
        try:
            self.precondition()
            strategies_wizard = ExecutionStrategiesWizard(self.web_driver_container)
            dark_block = ExecutionStrategiesDarkSubWizard(self.web_driver_container)
            expected_parameter_at_dark_block = "TestSuperStrategy1=2/test1582=1"
            self.verify("Saved dark broker strategy", expected_parameter_at_dark_block, dark_block.get_value())
            dark_block.click_on_go_back_button()
            time.sleep(2)
            strategies_wizard.click_on_lit_general()
            lit_general = ExecutionStrategiesLitGeneralSubWizard(self.web_driver_container)
            lit_general.click_on_plus_button()
            lit_general.set_parameter("BrokerStrategy")
            lit_general.set_value_by_dropdown_list_at_sub_wizard("TestSuperStrategy1")
            lit_general.click_on_checkmark_button()
            expected_parameter_at_lit_general_block = "TestSuperStrategy1"
            self.verify("Saved BrokerStrategy", expected_parameter_at_lit_general_block, lit_general.get_value())
            lit_general.click_on_go_back_button()
            time.sleep(2)
            expected_parameter_and_value_at_dark_block = ["DarkBrokerStrategies: ", expected_parameter_at_dark_block]
            actual_parameter_and_value_at_dark_block = [strategies_wizard.get_parameter_name_at_dark_block(),
                                                        strategies_wizard.get_parameter_value_at_dark_block()]
            self.verify("At Dark block", expected_parameter_and_value_at_dark_block,
                        actual_parameter_and_value_at_dark_block)
            expected_parameter_and_value_at_lit_general_block = ["BrokerStrategy: ",
                                                                 expected_parameter_at_lit_general_block]
            actual_parameter_and_value_at_lit_general_block = [
                strategies_wizard.get_parameter_name_at_lit_general_block(),
                strategies_wizard.get_parameter_value_at_lit_general_block()]
            self.verify("At Lit General block", expected_parameter_and_value_at_lit_general_block,
                        actual_parameter_and_value_at_lit_general_block)

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
