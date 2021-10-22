import time
import traceback

from custom import basic_custom_actions
from quod_qa.web_admin.web_admin_core.pages.login.login_page import LoginPage
from quod_qa.web_admin.web_admin_core.pages.order_management.execution_strategies.execution_strategies_lit_dark_sub_wizard import \
    ExecutionStrategiesLitDarkSubWizard
from quod_qa.web_admin.web_admin_core.pages.order_management.execution_strategies.execution_strategies_page import \
    ExecutionStrategiesPage
from quod_qa.web_admin.web_admin_core.pages.order_management.execution_strategies.execution_strategies_wizard import \
    ExecutionStrategiesWizard
from quod_qa.web_admin.web_admin_core.pages.root.side_menu import SideMenu
from quod_qa.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer
from quod_qa.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_2968(CommonTestCase):
    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id)
        self.console_error_lvl_id = second_lvl_id
        self.name = "TestSuperStrategy"
        self.user = "QA1"
        self.strategy_type = "Quod LitDark"
        self.parameter = "Visibility"
        self.value = "30"

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
        strategies_wizard.set_user(self.user)
        strategies_wizard.set_strategy_type(self.strategy_type)
        time.sleep(1)
        strategies_wizard.click_on_lit_dark()
        lit_dark_block = ExecutionStrategiesLitDarkSubWizard(self.web_driver_container)
        lit_dark_block.click_on_plus_button()
        lit_dark_block.set_parameter(self.parameter)
        lit_dark_block.set_value(self.value)
        lit_dark_block.click_on_checkmark_button()
        lit_dark_block.click_on_go_back_button()

    def test_context(self):
        try:
            self.precondition()
            strategies_wizard = ExecutionStrategiesWizard(self.web_driver_container)
            expected_parameter_and_value_at_dark_block = ["Visibility: ", self.value]
            actual_parameter_and_value_at_dark_block = [strategies_wizard.get_parameter_name_at_lit_dark_block(),
                                                        strategies_wizard.get_parameter_value_at_lit_dark_block()]
            self.verify("After saved at LIT Dark block", expected_parameter_and_value_at_dark_block,
                        actual_parameter_and_value_at_dark_block)
        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.console_error_lvl_id,
                                              status='FAILED')
            print(traceback.format_exc() + " Search in ->  " + self.__class__.__name__)
