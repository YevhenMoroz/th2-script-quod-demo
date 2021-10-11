import time
import traceback

from custom import basic_custom_actions
from quod_qa.web_admin.web_admin_core.pages.login.login_page import LoginPage
from quod_qa.web_admin.web_admin_core.pages.order_management.execution_strategies.execution_strategies_lit_general_sub_wizard import \
    ExecutionStrategiesLitGeneralSubWizard
from quod_qa.web_admin.web_admin_core.pages.order_management.execution_strategies.execution_strategies_page import \
    ExecutionStrategiesPage
from quod_qa.web_admin.web_admin_core.pages.order_management.execution_strategies.execution_strategies_wizard import \
    ExecutionStrategiesWizard
from quod_qa.web_admin.web_admin_core.pages.root.side_menu import SideMenu
from quod_qa.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer
from quod_qa.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_2431(CommonTestCase):
    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id)
        self.console_error_lvl_id = second_lvl_id
        self.name = "TestSuperStrategy"
        self.user = "QA1"
        self.strategy_type = "Quod MultiListing"
        self.parameter = "SprayModify"
        self.first_value = "Single"
        self.second_value = "Spray"

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
        strategies_wizard.set_strategy_type(self.strategy_type)
        time.sleep(1)
        strategies_wizard.set_user(self.user)
        strategies_wizard.click_on_lit_general()
        general_at_lit_block = ExecutionStrategiesLitGeneralSubWizard(self.web_driver_container)
        general_at_lit_block.click_on_plus_button()
        general_at_lit_block.set_parameter(self.parameter)
        general_at_lit_block.set_value_by_dropdown_list_at_sub_wizard(self.first_value)
        general_at_lit_block.click_on_checkmark_button()
        general_at_lit_block.click_on_edit_button()
        time.sleep(2)
        general_at_lit_block.set_value_by_dropdown_list_at_sub_wizard(self.second_value)
        time.sleep(2)
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
            time.sleep(2)
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
