import time
import traceback

from custom import basic_custom_actions
from quod_qa.web_admin.web_admin_core.pages.login.login_page import LoginPage
from quod_qa.web_admin.web_admin_core.pages.order_management.execution_strategies.execution_strategies_lit_aggressive_sub_wizard import \
    ExecutionStrategiesLitAggressiveSubWizard
from quod_qa.web_admin.web_admin_core.pages.order_management.execution_strategies.execution_strategies_lit_dark_sub_wizard import \
    ExecutionStrategiesLitDarkSubWizard
from quod_qa.web_admin.web_admin_core.pages.order_management.execution_strategies.execution_strategies_lit_passive_sub_wizard import \
    ExecutionStrategiesLitPassiveSubWizard
from quod_qa.web_admin.web_admin_core.pages.order_management.execution_strategies.execution_strategies_page import \
    ExecutionStrategiesPage
from quod_qa.web_admin.web_admin_core.pages.order_management.execution_strategies.execution_strategies_wizard import \
    ExecutionStrategiesWizard
from quod_qa.web_admin.web_admin_core.pages.root.side_menu import SideMenu
from quod_qa.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer
from quod_qa.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_2430(CommonTestCase):
    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id)
        self.console_error_lvl_id = second_lvl_id
        self.name = "TestSuperStrategy"
        self.user = "QA1"
        self.strategy_type = "Quod LitDark"
        self.first_parameter = "AllowedAggressiveVenues"
        self.second_parameter = "AllowedPassiveVenues"
        self.third_parameter = "InitialDarkAllowedVenues"
        self.first_venue = "DARK POOL 1"
        self.second_venue = "EURONEXT AMSTERDAM"
        self.third_venue = "BATS Dark Pool"

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.set_login("adm07")
        login_page.set_password("adm07")
        login_page.click_login_button()
        login_page.check_is_login_successful()
        side_menu = SideMenu(self.web_driver_container)
        side_menu.open_execution_strategies_page()
        main_menu = ExecutionStrategiesPage(self.web_driver_container)
        main_menu.click_on_new_button()
        strategies_wizard = ExecutionStrategiesWizard(self.web_driver_container)
        time.sleep(2)
        strategies_wizard.set_name(self.name)
        time.sleep(2)
        strategies_wizard.set_user(self.user)
        time.sleep(2)
        strategies_wizard.set_strategy_type(self.strategy_type)
        strategies_wizard.click_on_lit_aggressive()
        aggressive_lit_block = ExecutionStrategiesLitAggressiveSubWizard(self.web_driver_container)
        aggressive_lit_block.click_on_plus_button()
        aggressive_lit_block.set_parameter(self.first_parameter)
        aggressive_lit_block.click_on_plus_at_actions_sub_wizard()
        aggressive_lit_block.set_venue_at_actions_sub_wizard(self.first_venue)
        aggressive_lit_block.click_on_checkmark_at_actions_sub_wizard()
        aggressive_lit_block.click_on_plus_at_actions_sub_wizard()
        aggressive_lit_block.set_venue_at_actions_sub_wizard(self.second_venue)
        aggressive_lit_block.click_on_checkmark_at_actions_sub_wizard()
        aggressive_lit_block.click_on_plus_at_actions_sub_wizard()
        aggressive_lit_block.set_venue_at_actions_sub_wizard(self.third_venue)
        aggressive_lit_block.click_on_checkmark_at_actions_sub_wizard()
        aggressive_lit_block.click_on_checkmark_button()
        aggressive_lit_block.click_on_go_back_button()

    def test_context(self):
        try:
            self.precondition()
            main_menu = ExecutionStrategiesPage(self.web_driver_container)
            aggressive_lit_block = ExecutionStrategiesLitAggressiveSubWizard(self.web_driver_container)
            strategies_wizard = ExecutionStrategiesWizard(self.web_driver_container)
            expected_parameter_and_value_at_lit_passive_block = ["AllowedAggressiveVenues: ",
                                                                 "DARK POOL 1/EURONEXT AMSTERDAM/BATS Dark Pool"]
            actual_parameter_and_value_at_lit_passive_block = [
                strategies_wizard.get_parameter_name_at_lit_aggressive_block(),
                strategies_wizard.get_parameter_value_at_lit_aggressive_block()]
            self.verify("After saved AllowedAggressiveVenues parameter",
                        expected_parameter_and_value_at_lit_passive_block,
                        actual_parameter_and_value_at_lit_passive_block)
            strategies_wizard.click_on_lit_passive()
            aggressive_lit_block.click_on_plus_button()
            aggressive_lit_block.set_parameter(self.second_parameter)
            aggressive_lit_block.click_on_plus_at_actions_sub_wizard()
            aggressive_lit_block.set_venue_at_actions_sub_wizard(self.first_venue)
            aggressive_lit_block.click_on_checkmark_at_actions_sub_wizard()
            aggressive_lit_block.click_on_plus_at_actions_sub_wizard()
            aggressive_lit_block.set_venue_at_actions_sub_wizard(self.second_venue)
            aggressive_lit_block.click_on_checkmark_at_actions_sub_wizard()
            aggressive_lit_block.click_on_plus_at_actions_sub_wizard()
            aggressive_lit_block.set_venue_at_actions_sub_wizard(self.third_venue)
            aggressive_lit_block.click_on_checkmark_at_actions_sub_wizard()
            aggressive_lit_block.click_on_checkmark_button()
            aggressive_lit_block.click_on_go_back_button()
            expected_parameter_and_value_at_lit_passive_block_second = ["AllowedPassiveVenues: ",
                                                                        "DARK POOL 1/EURONEXT AMSTERDAM/BATS Dark Pool"]
            actual_parameter_and_value_at_lit_passive_block_second = [
                strategies_wizard.get_parameter_name_at_lit_passive_block(),
                strategies_wizard.get_parameter_value_at_lit_passive_block()]

            self.verify("After saved AllowedPassiveVenues parameter",
                        expected_parameter_and_value_at_lit_passive_block_second,
                        actual_parameter_and_value_at_lit_passive_block_second)
            strategies_wizard.click_on_lit_dark()
            dark_lit_block = ExecutionStrategiesLitDarkSubWizard(self.web_driver_container)
            dark_lit_block.click_on_plus_button()
            dark_lit_block.set_parameter(self.third_parameter)
            dark_lit_block.click_on_plus_at_actions_sub_wizard()
            dark_lit_block.set_venue_at_actions_sub_wizard(self.first_venue)
            dark_lit_block.click_on_checkmark_at_actions_sub_wizard()
            dark_lit_block.click_on_plus_at_actions_sub_wizard()
            dark_lit_block.set_venue_at_actions_sub_wizard(self.second_venue)
            dark_lit_block.click_on_checkmark_at_actions_sub_wizard()
            dark_lit_block.click_on_plus_at_actions_sub_wizard()
            dark_lit_block.set_venue_at_actions_sub_wizard(self.third_venue)
            dark_lit_block.click_on_checkmark_at_actions_sub_wizard()
            dark_lit_block.click_on_checkmark_button()
            dark_lit_block.click_on_go_back_button()
            expected_parameter_and_value_at_lit_passive_block_third = ["InitialDarkAllowedVenues: ",
                                                                       "DARK POOL 1/EURONEXT AMSTERDAM/BATS Dark Pool"]
            actual_parameter_and_value_at_lit_passive_block_third = [
                strategies_wizard.get_parameter_name_at_lit_dark_block(),
                strategies_wizard.get_parameter_value_at_lit_dark_block()]

            self.verify("After saved InitialDarkAllowedVenues parameter",
                        expected_parameter_and_value_at_lit_passive_block_third,
                        actual_parameter_and_value_at_lit_passive_block_third)
            strategies_wizard.click_on_save_changes()
            main_menu.set_enabled_at_filter_field("true")
            main_menu.set_name_at_filter_field(self.name)
            time.sleep(2)
            main_menu.click_on_enable_disable_button()
            main_menu.click_on_ok_button()
        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.console_error_lvl_id,
                                              status='FAILED')
            print(traceback.format_exc() + " Search in ->  " + self.__class__.__name__)
