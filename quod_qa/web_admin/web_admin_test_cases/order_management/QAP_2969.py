import random
import string
import traceback

from custom import basic_custom_actions
from quod_qa.web_admin.web_admin_core.pages.login.login_page import LoginPage
from quod_qa.web_admin.web_admin_core.pages.order_management.execution_strategies.execution_strategies_dark_sub_wizard import \
    ExecutionStrategiesDarkSubWizard
from quod_qa.web_admin.web_admin_core.pages.order_management.execution_strategies.execution_strategies_lit_general_sub_wizard import \
    ExecutionStrategiesLitGeneralSubWizard
from quod_qa.web_admin.web_admin_core.pages.order_management.execution_strategies.execution_strategies_page import \
    ExecutionStrategiesPage
from quod_qa.web_admin.web_admin_core.pages.order_management.execution_strategies.execution_strategies_wizard import \
    ExecutionStrategiesWizard
from quod_qa.web_admin.web_admin_core.pages.root.side_menu import SideMenu
from quod_qa.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer
from quod_qa.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_2969(CommonTestCase):
    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id)
        self.name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.user = "QA1"
        self.strategy_type = "Quod LitDark"
        self.parameter_at_dark_block = "DarkOpeningBrokerStrategy"
        self.value_at_dark_parameter = "TestSuperStrategy1"

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
        strategies_wizard.set_name(self.name)
        strategies_wizard.set_user(self.user)
        strategies_wizard.set_strategy_type(self.strategy_type)
        strategies_wizard.click_on_dark_block()
        dark_block = ExecutionStrategiesDarkSubWizard(self.web_driver_container)
        dark_block.click_on_plus_button()
        dark_block.set_parameter(self.parameter_at_dark_block)
        dark_block.set_value_by_dropdown_list_at_sub_wizard(self.value_at_dark_parameter)
        dark_block.click_on_checkmark_button()

    def test_context(self):
        try:
            self.precondition()
            strategies_wizard = ExecutionStrategiesWizard(self.web_driver_container)
            dark_block = ExecutionStrategiesDarkSubWizard(self.web_driver_container)
            expected_parameter_at_dark_block = "TestSuperStrategy1"
            self.verify("Saved dark broker strategy", expected_parameter_at_dark_block, dark_block.get_value())
            dark_block.click_on_go_back_button()
            strategies_wizard.click_on_lit_general()
            lit_general = ExecutionStrategiesLitGeneralSubWizard(self.web_driver_container)
            lit_general.click_on_plus_button()
            lit_general.set_parameter("BrokerStrategy")
            lit_general.set_value_by_dropdown_list_at_sub_wizard("test1582")
            lit_general.click_on_checkmark_button()
            expected_parameter_at_lit_general_block = "test1582"
            self.verify("Saved BrokerStrategy", expected_parameter_at_lit_general_block, lit_general.get_value())
            lit_general.click_on_go_back_button()
            expected_parameter_and_value_at_dark_block = ["DarkOpeningBrokerStrategy: ",
                                                          expected_parameter_at_dark_block]
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
            print(traceback.format_exc() + " Search in ->  " + self.__class__.__name__)
