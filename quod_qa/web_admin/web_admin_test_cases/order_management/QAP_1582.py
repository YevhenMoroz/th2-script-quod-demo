import time
import traceback

from selenium.common.exceptions import TimeoutException

from custom import basic_custom_actions
from quod_qa.web_admin.web_admin_core.pages.login.login_page import LoginPage
from quod_qa.web_admin.web_admin_core.pages.order_management.execution_strategies.execution_strategies_general_sub_wizard import \
    ExecutionStrategiesGeneralSubWizard
from quod_qa.web_admin.web_admin_core.pages.order_management.execution_strategies.execution_strategies_page import \
    ExecutionStrategiesPage
from quod_qa.web_admin.web_admin_core.pages.order_management.execution_strategies.execution_strategies_wizard import \
    ExecutionStrategiesWizard
from quod_qa.web_admin.web_admin_core.pages.root.side_menu import SideMenu
from quod_qa.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer
from quod_qa.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_1582(CommonTestCase):
    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id)
        self.name = "test1582"
        self.user = "adm01"
        self.strategy_type = "External AMBUSH"

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.set_login("adm02")
        login_page.set_password("adm02")
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
        strategies_wizard.click_on_general()
        general_block_wizard = ExecutionStrategiesGeneralSubWizard(self.web_driver_container)
        general_block_wizard.click_on_plus_button()
        general_block_wizard.set_parameter("Custom")
        general_block_wizard.set_value_at_sub_wizard("333")
        general_block_wizard.click_on_checkmark_button()
        general_block_wizard.click_on_go_back_button()
        strategies_wizard.click_on_save_changes()
        main_menu.set_name_at_filter_field(self.name)
        time.sleep(2)
        main_menu.set_enabled_at_filter_field("true")
        main_menu.click_on_enable_disable_button()
        time.sleep(1)
        main_menu.click_on_ok_button()
        time.sleep(1)
        main_menu.click_on_enable_disable_button()
        time.sleep(1)
        main_menu.click_on_ok_button()
        time.sleep(2)
        main_menu.click_on_more_actions()
        time.sleep(1)
        main_menu.click_on_edit_at_more_actions()

    def test_context(self):
        try:
            self.precondition()
            strategies_wizard = ExecutionStrategiesWizard(self.web_driver_container)
            main_menu = ExecutionStrategiesPage(self.web_driver_container)
            expected_value_at_general_tab = ['Custom: ', "333"]
            try:
                actual_value_at_general_tab = [strategies_wizard.get_parameter_name_at_general_block(),
                                               strategies_wizard.get_parameter_value_at_general_block()]
                self.verify("After click on toggle", expected_value_at_general_tab, actual_value_at_general_tab)
            except TimeoutException:
                actual_value_at_general_tab = ["TimeoutException because don't search parameter at general tab"]
                self.verify("After click on toggle", expected_value_at_general_tab, actual_value_at_general_tab)
            finally:
                time.sleep(1)
                strategies_wizard.click_on_close_button()
                main_menu.set_name_at_filter_field(self.name)
                time.sleep(2)
                main_menu.set_enabled_at_filter_field("true")
                main_menu.click_on_enable_disable_button()
                time.sleep(1)
                main_menu.click_on_ok_button()
        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            print(traceback.format_exc() + " Search in ->  " + self.__class__.__name__)
