import random
import string
import sys
import time
import traceback

from custom import basic_custom_actions
from test_cases.web_admin.web_admin_core.pages.login.login_page import LoginPage
from test_cases.web_admin.web_admin_core.pages.order_management.execution_strategies.execution_strategies_general_sub_wizard import \
    ExecutionStrategiesGeneralSubWizard
from test_cases.web_admin.web_admin_core.pages.order_management.execution_strategies.execution_strategies_lit_aggressive_sub_wizard import \
    ExecutionStrategiesLitAggressiveSubWizard
from test_cases.web_admin.web_admin_core.pages.order_management.execution_strategies.execution_strategies_page import \
    ExecutionStrategiesPage
from test_cases.web_admin.web_admin_core.pages.order_management.execution_strategies.execution_strategies_wizard import \
    ExecutionStrategiesWizard
from test_cases.web_admin.web_admin_core.pages.root.side_menu import SideMenu
from test_cases.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_1567(CommonTestCase):
    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id)
        self.name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.user = "QA1"
        self.strategy_type = "Quod LitDark"
        self.first_parameter = "AllowedAggressiveVenues"
        self.first_venue = "EURONEXT AMSTERDAM"

        self.new_name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.new_user = "QA2"
        self.new_strategy_type = "External CUSTOM1"
        self.new_parameter = "Custom"
        self.new_value = "12"

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
        aggressive_lit_block.click_on_checkmark_button()
        aggressive_lit_block.click_on_go_back_button()
        strategies_wizard.click_on_save_changes()
        time.sleep(2)
        main_menu.set_enabled_at_filter_field("true")
        main_menu.set_name_at_filter_field(self.name)
        time.sleep(2)
        main_menu.click_on_more_actions()
        main_menu.click_on_edit_at_more_actions()
        time.sleep(2)
        strategies_wizard.set_user(self.new_user)
        time.sleep(1)
        strategies_wizard.set_name(self.new_name)
        time.sleep(2)
        strategies_wizard.set_strategy_type(self.new_strategy_type)
        time.sleep(2)
        strategies_wizard.click_on_general()
        general_block = ExecutionStrategiesGeneralSubWizard(self.web_driver_container)
        general_block.click_on_plus_button()
        general_block.set_parameter(self.new_parameter)
        general_block.set_value_at_sub_wizard(self.new_value)
        general_block.click_on_checkmark_button()
        general_block.click_on_go_back_button()

    def test_context(self):
        try:
            self.precondition()
            strategies_wizard = ExecutionStrategiesWizard(self.web_driver_container)
            expected_summary_tab_values = [self.new_name, self.new_user, self.new_strategy_type, "Custom: ",
                                           self.new_value]
            actual_summary_tab_values = [strategies_wizard.get_name(), strategies_wizard.get_user(),
                                         strategies_wizard.get_strategy_type(),
                                         strategies_wizard.get_parameter_name_at_general_block(),
                                         strategies_wizard.get_parameter_value_at_general_block()]
            self.verify("Data on summary tab after edited", expected_summary_tab_values, actual_summary_tab_values)
            strategies_wizard.click_on_save_changes()
            main_menu = ExecutionStrategiesPage(self.web_driver_container)
            main_menu.set_name_at_filter_field(self.new_name)
            expected_pdf_content = [
                self.new_name,
                self.new_user,
                self.new_strategy_type,
                self.new_parameter,
                self.new_value]
            time.sleep(2)
            main_menu.click_on_more_actions()
            self.verify("Data in pdf after edited", True,
                        main_menu.click_download_pdf_entity_button_and_check_pdf(expected_pdf_content))
            time.sleep(2)
            main_menu.click_on_enable_disable_button()
            main_menu.click_on_ok_button()
        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
