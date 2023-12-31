import sys
import time
import random
import string
import traceback

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.order_management.execution_strategies.execution_strategies_lit_passive_sub_wizard \
    import ExecutionStrategiesLitPassiveSubWizard
from test_framework.web_admin_core.pages.order_management.execution_strategies.execution_strategies_page import \
    ExecutionStrategiesPage
from test_framework.web_admin_core.pages.order_management.execution_strategies.execution_strategies_wizard import \
    ExecutionStrategiesWizard
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T4814(CommonTestCase):
    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.user = self.data_set.get_user("user_8")
        self.strategy_type = self.data_set.get_strategy_type("strategy_type_3")

        self.parameter = "SynthesiseMultiDay"

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        side_menu.click_on_execution_strategies_tab()
        side_menu.wait_for_button_to_become_active()

    def test_context(self):
        try:
            self.precondition()

            main_menu = ExecutionStrategiesPage(self.web_driver_container)

            main_menu.click_on_new_button()

            strategies_wizard = ExecutionStrategiesWizard(self.web_driver_container)
            strategies_wizard.set_name(self.name)
            strategies_wizard.set_strategy_type(self.strategy_type)

            strategies_wizard.set_user(self.user)
            strategies_wizard.click_on_lit_passive()

            passive_block = ExecutionStrategiesLitPassiveSubWizard(self.web_driver_container)
            passive_block.click_on_plus_button()
            passive_block.set_parameter(self.parameter)
            passive_block.set_checkbox()
            passive_block.click_on_checkmark_button()
            passive_block.click_on_go_back_button()

            expected_result = [self.parameter, "Y"]
            actual_result = [str(strategies_wizard.get_parameter_name_at_lit_passive_block())[:len(self.parameter)],
                             strategies_wizard.get_parameter_value_at_lit_passive_block()]
            self.verify("The selected parameter is displayed on the main creating page", expected_result, actual_result)

            strategies_wizard.click_on_save_changes()
            main_menu.set_name_at_filter_field(self.name)
            time.sleep(1)

            self.verify("New Execution Strategy create and found", True,
                        main_menu.is_searched_execution_strategy_found(self.name))
        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
