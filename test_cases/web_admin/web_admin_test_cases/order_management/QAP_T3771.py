import random
import string
import sys
import time
import traceback

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.order_management.execution_strategies.execution_strategies_lit_aggressive_sub_wizard import \
    ExecutionStrategiesLitAggressiveSubWizard
from test_framework.web_admin_core.pages.order_management.execution_strategies.execution_strategies_lit_general_sub_wizard import \
    ExecutionStrategiesLitGeneralSubWizard
from test_framework.web_admin_core.pages.order_management.execution_strategies.execution_strategies_lit_passive_sub_wizard import \
    ExecutionStrategiesLitPassiveSubWizard
from test_framework.web_admin_core.pages.order_management.execution_strategies.execution_strategies_lit_sweeping_sub_wizard import \
    ExecutionStrategiesLitSweepingSubWizard
from test_framework.web_admin_core.pages.order_management.execution_strategies.execution_strategies_page import \
    ExecutionStrategiesPage
from test_framework.web_admin_core.pages.order_management.execution_strategies.execution_strategies_wizard import \
    ExecutionStrategiesWizard
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T3771(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.strategy_type = self.data_set.get_strategy_type("strategy_type_1")
        self.user = self.data_set.get_user("user_9")
        self.client = self.data_set.get_client("client_1")
        self.parameters = {"1": "StatMarketShareCalcType", "2": "PostMode", "3": "StatMarketShareTimeHorizon",
                           "4": "CrossCurrency", "5": "StatHitRatioCalcType", "6": "MinimumPercentage"}
        self.parameter_values = {"1": "DAY", "2": "Single", "3": "22", "4": "Default", "5": "DAY", "6": "12"}

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        time.sleep(2)
        side_menu.open_execution_strategies_page()
        side_menu.wait_for_button_to_become_active()
        execution_strategies_main_menu = ExecutionStrategiesPage(self.web_driver_container)
        execution_strategies_main_menu.click_on_new_button()
        execution_strategies_wizard = ExecutionStrategiesWizard(self.web_driver_container)
        time.sleep(1)
        execution_strategies_wizard.set_name(self.name)
        time.sleep(1)
        execution_strategies_wizard.set_strategy_type(self.strategy_type)
        time.sleep(1)
        execution_strategies_wizard.set_client(self.client)
        execution_strategies_wizard.click_on_lit_passive()
        time.sleep(2)
        execution_strategies_lit_passive = ExecutionStrategiesLitPassiveSubWizard(self.web_driver_container)
        execution_strategies_lit_passive.click_on_plus_button()
        execution_strategies_lit_passive.set_parameter(self.parameters["1"])
        execution_strategies_lit_passive.set_value_by_dropdown_list_at_sub_wizard(self.parameter_values["1"])
        execution_strategies_lit_passive.click_on_checkmark_button()
        execution_strategies_lit_passive = ExecutionStrategiesLitPassiveSubWizard(self.web_driver_container)
        execution_strategies_lit_passive.click_on_plus_button()
        execution_strategies_lit_passive.set_parameter(self.parameters["2"])
        execution_strategies_lit_passive.set_value_by_dropdown_list_at_sub_wizard(self.parameter_values["2"])
        execution_strategies_lit_passive.click_on_checkmark_button()
        execution_strategies_lit_passive = ExecutionStrategiesLitPassiveSubWizard(self.web_driver_container)
        execution_strategies_lit_passive.click_on_plus_button()
        execution_strategies_lit_passive.set_parameter(self.parameters["3"])
        execution_strategies_lit_passive.set_value(self.parameter_values["3"])
        execution_strategies_lit_passive.click_on_checkmark_button()
        execution_strategies_lit_passive.click_on_go_back_button()
        time.sleep(2)

    def test_context(self):
        try:
            self.precondition()
            execution_strategies_main_menu = ExecutionStrategiesPage(self.web_driver_container)
            execution_strategies_wizard = ExecutionStrategiesWizard(self.web_driver_container)
            expected_parameter_and_value_at_lit_passive_block = [
                f'{self.parameters["1"]}: ', self.parameter_values["1"]]
            actual_parameter_and_value_at_lit_passive_block = [
                execution_strategies_wizard.get_parameter_name_at_lit_passive_block(),
                execution_strategies_wizard.get_parameter_value_at_lit_passive_block()]
            self.verify("Check that new entity at lit passive saved correctly",
                        expected_parameter_and_value_at_lit_passive_block,
                        actual_parameter_and_value_at_lit_passive_block)
            time.sleep(2)

            execution_strategies_wizard.click_on_lit_general()
            execution_strategies_lit_general = ExecutionStrategiesLitGeneralSubWizard(self.web_driver_container)
            execution_strategies_lit_general.click_on_plus_button()
            execution_strategies_lit_general.set_parameter(self.parameters["4"])
            execution_strategies_lit_general.set_value_by_dropdown_list_at_sub_wizard(self.parameter_values["4"])
            execution_strategies_lit_general.click_on_checkmark_button()
            execution_strategies_lit_general.click_on_go_back_button()
            time.sleep(2)
            execution_strategies_wizard.click_on_lit_aggressive()
            execution_strategies_lit_aggressive = ExecutionStrategiesLitAggressiveSubWizard(self.web_driver_container)
            execution_strategies_lit_aggressive.click_on_plus_button()
            execution_strategies_lit_aggressive.set_parameter(self.parameters["5"])
            execution_strategies_lit_aggressive.set_value_by_dropdown_list_at_sub_wizard(self.parameter_values["5"])
            execution_strategies_lit_aggressive.click_on_checkmark_button()
            execution_strategies_lit_aggressive.click_on_go_back_button()
            time.sleep(2)
            execution_strategies_wizard.click_on_lit_sweeping()
            execution_strategies_lit_sweeping = ExecutionStrategiesLitSweepingSubWizard(self.web_driver_container)
            execution_strategies_lit_sweeping.click_on_plus_button()
            execution_strategies_lit_sweeping.set_parameter(self.parameters["6"])
            execution_strategies_lit_sweeping.set_value(self.parameter_values["6"])
            execution_strategies_lit_sweeping.click_on_checkmark_button()
            execution_strategies_lit_sweeping.click_on_go_back_button()
            time.sleep(2)
            execution_strategies_wizard.click_on_save_changes()
            side_menu = SideMenu(self.web_driver_container)
            side_menu.wait_for_button_to_become_active()
            execution_strategies_main_menu.set_name_at_filter_field(self.name)
            time.sleep(2)
            execution_strategies_main_menu.click_on_more_actions()
            execution_strategies_main_menu.click_on_edit_at_more_actions()
            expected_parameter_and_value_at_lit_general_block = [f'{self.parameters["4"]}: ', self.parameter_values["4"]]
            actual_parameter_and_value_at_lit_general_block = [
                execution_strategies_wizard.get_parameter_name_at_lit_general_block(),
                execution_strategies_wizard.get_parameter_value_at_lit_general_block()]

            self.verify("Check that values correctly saved  in Lit General block after click on save changes button",
                        expected_parameter_and_value_at_lit_general_block,
                        actual_parameter_and_value_at_lit_general_block)

            expected_parameter_and_value_at_lit_aggressive_block = [f'{self.parameters["5"]}: ', self.parameter_values["5"]]
            actual_parameter_and_value_at_lit_aggressive_block = [
                execution_strategies_wizard.get_parameter_name_at_lit_aggressive_block(),
                execution_strategies_wizard.get_parameter_value_at_lit_aggressive_block()]

            self.verify("Check that values correctly saved  in Lit Aggressive block after click on save changes button",
                        expected_parameter_and_value_at_lit_aggressive_block,
                        actual_parameter_and_value_at_lit_aggressive_block)

            expected_parameter_and_value_at_sweeping_block = [f'{self.parameters["6"]}: ', self.parameter_values["6"]]
            actual_parameter_and_value_at_sweeping_block = [
                execution_strategies_wizard.get_parameter_name_at_lit_sweeping_block(),
                execution_strategies_wizard.get_parameter_value_at_lit_sweeping_block()]

            self.verify("Check that values correctly saved  in Lit Sweeping block after click on save changes button",
                        expected_parameter_and_value_at_sweeping_block,
                        actual_parameter_and_value_at_sweeping_block)
        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
