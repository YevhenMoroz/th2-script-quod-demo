import random
import string
import sys
import time
import traceback

from selenium.common.exceptions import TimeoutException

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.order_management.execution_strategies.execution_strategies_general_sub_wizard import \
    ExecutionStrategiesGeneralSubWizard
from test_framework.web_admin_core.pages.order_management.execution_strategies.execution_strategies_page import \
    ExecutionStrategiesPage
from test_framework.web_admin_core.pages.order_management.execution_strategies.execution_strategies_wizard import \
    ExecutionStrategiesWizard
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T3996(CommonTestCase):
    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.user = self.data_set.get_user("user_11")
        self.strategy_type = self.data_set.get_strategy_type("strategy_type_4")

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.set_login(self.login)
        login_page.set_password(self.password)
        login_page.click_login_button()
        time.sleep(2)
        side_menu = SideMenu(self.web_driver_container)
        side_menu.click_on_execution_strategies_when_order_management_tab_is_open()
        side_menu.wait_for_button_to_become_active()
        main_menu = ExecutionStrategiesPage(self.web_driver_container)
        main_menu.click_on_new_button()
        time.sleep(2)
        strategies_wizard = ExecutionStrategiesWizard(self.web_driver_container)
        strategies_wizard.set_name(self.name)
        strategies_wizard.set_user(self.user)
        strategies_wizard.set_strategy_type(self.strategy_type)
        time.sleep(1)
        strategies_wizard.click_on_general()
        general_block_wizard = ExecutionStrategiesGeneralSubWizard(self.web_driver_container)
        general_block_wizard.click_on_plus_button()
        time.sleep(1)
        general_block_wizard.set_parameter("Custom")
        time.sleep(1)
        general_block_wizard.set_value_at_sub_wizard("333")
        general_block_wizard.click_on_checkmark_button()
        time.sleep(1)
        general_block_wizard.click_on_go_back_button()
        time.sleep(2)
        strategies_wizard.click_on_save_changes()
        time.sleep(2)
        main_menu.set_name_at_filter_field(self.name)
        time.sleep(1)
        main_menu.click_on_enable_disable_button()
        main_menu.click_on_ok_button()
        time.sleep(2)
        main_menu.click_on_enable_disable_button()
        main_menu.click_on_ok_button()
        time.sleep(2)
        main_menu.click_on_more_actions()
        time.sleep(1)
        main_menu.click_on_edit_at_more_actions()
        time.sleep(2)

    def test_context(self):
        try:
            self.precondition()
            strategies_wizard = ExecutionStrategiesWizard(self.web_driver_container)
            expected_value_at_general_tab = ['Custom: ', "333"]
            try:
                actual_value_at_general_tab = [strategies_wizard.get_parameter_name_at_general_block(),
                                               strategies_wizard.get_parameter_value_at_general_block()]
                self.verify("After click on toggle", expected_value_at_general_tab, actual_value_at_general_tab)
            except TimeoutException:
                actual_value_at_general_tab = ["TimeoutException because don't search parameter at general tab"]
                self.verify("After click on toggle", expected_value_at_general_tab, actual_value_at_general_tab)

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
