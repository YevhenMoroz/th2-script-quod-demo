import sys
import time
import traceback

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.order_management.execution_strategies.execution_strategies_page import \
    ExecutionStrategiesPage
from test_framework.web_admin_core.pages.order_management.execution_strategies.execution_strategies_wizard import \
    ExecutionStrategiesWizard
from test_framework.web_admin_core.pages.order_management.execution_strategies.execution_strategies_dark_sub_wizard import \
    ExecutionStrategiesDarkSubWizard
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T11085(CommonTestCase):
    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.strategy_type = self.data_set.get_strategy_type("strategy_type_5")
        self.strategy_name = self.data_set.get_default_execution_strategy("default_execution_strategy_1")
        self.dark_subwizard_values = ['N', 'Y', 'N', 'N', '700', '0', 'RoundRobin', 'Neutral', 'DAY', '0']

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
            main_page.set_strategy_type_at_filter_field(self.strategy_type)
            main_page.set_name_at_filter_field(self.strategy_name)
            time.sleep(2)
            main_page.click_on_more_actions()
            main_page.click_on_edit_at_more_actions()
            strategies_wizard = ExecutionStrategiesWizard(self.web_driver_container)
            
            strategies_wizard.click_on_dark_block()
            execution_strategies_dark = ExecutionStrategiesDarkSubWizard(self.web_driver_container)
            actual_dark_subwizard_values = execution_strategies_dark.get_all_values_of_parameters_in_sub_wizard()
            self.verify("DarkSubWizard parameters' values", self.dark_subwizard_values, actual_dark_subwizard_values)
            execution_strategies_dark.click_on_go_back_button()

        except Exception:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            basic_custom_actions.create_event("TEST FAILED", self.test_case_id,
                                              'FAILED', f'{traceback.extract_tb(exc_traceback, limit=2)}, {sys.stdout}')
            print(" Search in ->  " + self.__class__.__name__)
