import random
import string
import sys
import time
import traceback

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.order_management.execution_strategies.execution_strategies_dark_sub_wizard import \
    ExecutionStrategiesDarkSubWizard
from test_framework.web_admin_core.pages.order_management.execution_strategies.execution_strategies_page import \
    ExecutionStrategiesPage
from test_framework.web_admin_core.pages.order_management.execution_strategies.execution_strategies_wizard import \
    ExecutionStrategiesWizard
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T3820(CommonTestCase):
    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.user = self.data_set.get_user("user_8")
        self.strategy_type = self.data_set.get_strategy_type("strategy_type_5")
        self.dark_parameter_1 = "LISPhase"
        self.dark_parameter_2 = "LISResidentTime"
        self.dark_parameter_3 = "LISPools"
        self.venue = self.data_set.get_venue_by_name("venue_6")
        self.venue_2 = self.data_set.get_venue_by_name("venue_7")

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        side_menu.click_on_execution_strategies_when_order_management_tab_is_open()
        side_menu.wait_for_button_to_become_active()
        main_menu = ExecutionStrategiesPage(self.web_driver_container)
        main_menu.click_on_new_button()
        strategies_wizard = ExecutionStrategiesWizard(self.web_driver_container)
        strategies_wizard.set_strategy_type(self.strategy_type)
        strategies_wizard.set_user(self.user)
        strategies_wizard.set_name(self.name)
        strategies_wizard.click_on_dark_block()
        dark_sub_wizard = ExecutionStrategiesDarkSubWizard(self.web_driver_container)
        dark_sub_wizard.click_on_plus_button()
        dark_sub_wizard.set_parameter(self.dark_parameter_1)
        dark_sub_wizard.set_checkbox()
        dark_sub_wizard.click_on_checkmark_button()
        dark_sub_wizard.click_on_plus_button()
        dark_sub_wizard.set_parameter(self.dark_parameter_2)
        dark_sub_wizard.set_value("5000")
        dark_sub_wizard.click_on_checkmark_button()
        dark_sub_wizard.click_on_plus_button()
        dark_sub_wizard.set_parameter(self.dark_parameter_3)
        dark_sub_wizard.click_on_plus_at_actions_sub_wizard()
        dark_sub_wizard.set_venue_at_actions_sub_wizard(self.venue)
        dark_sub_wizard.click_on_checkmark_at_actions_sub_wizard()
        dark_sub_wizard.click_on_checkmark_button()
        strategies_wizard = ExecutionStrategiesWizard(self.web_driver_container)
        strategies_wizard.click_on_go_back_button()
        strategies_wizard.click_on_save_changes()

    def test_context(self):

        try:
            self.precondition()

            strategies_page = ExecutionStrategiesPage(self.web_driver_container)
            strategies_page.set_name_at_filter_field(self.name)
            time.sleep(1)
            strategies_page.click_on_more_actions()
            strategies_page.click_on_edit_at_more_actions()
            expected_parameter_and_value_at_dark_block = ["LISPhase: Y", "LISResidentTime: 5000", "LISPools: ADX"]
            strategies_wizard = ExecutionStrategiesWizard(self.web_driver_container)
            parameters = strategies_wizard.get_all_parameters_names_from_dark_block()
            values = strategies_wizard.get_all_parameters_values_from_dark_block()
            actual_parameter_and_value_at_dark_block = [a+" "+str(b) for a, b in zip(parameters, values)]

            self.verify("After saved at Dark block", expected_parameter_and_value_at_dark_block,
                        actual_parameter_and_value_at_dark_block)

            strategies_wizard.click_on_dark_block()
            dark_sub_wizard = ExecutionStrategiesDarkSubWizard(self.web_driver_container)
            dark_sub_wizard.set_parameter_filter(self.dark_parameter_1)
            dark_sub_wizard.click_on_edit_button()
            dark_sub_wizard.set_checkbox()
            dark_sub_wizard.click_on_checkmark_button()

            time.sleep(1)
            dark_sub_wizard.set_parameter_filter(self.dark_parameter_2)
            dark_sub_wizard.click_on_edit_button()
            dark_sub_wizard.set_value("1000")
            dark_sub_wizard.click_on_checkmark_button()

            time.sleep(1)
            dark_sub_wizard.set_parameter_filter(self.dark_parameter_3)
            dark_sub_wizard.click_on_edit_button()
            dark_sub_wizard.click_on_delete_at_actions_sub_wizard()
            dark_sub_wizard.click_on_plus_at_actions_sub_wizard()
            dark_sub_wizard.set_venue_at_actions_sub_wizard(self.venue_2)
            dark_sub_wizard.click_on_checkmark_at_actions_sub_wizard()
            dark_sub_wizard.click_on_checkmark_button()
            strategies_wizard = ExecutionStrategiesWizard(self.web_driver_container)
            strategies_wizard.click_on_go_back_button()
            strategies_wizard.click_on_save_changes()

            strategies_page.set_name_at_filter_field(self.name)
            time.sleep(1)
            strategies_page.click_on_more_actions()
            strategies_page.click_on_edit_at_more_actions()
            expected_parameter_and_value_at_dark_block = ["LISPhase: N", "LISResidentTime: 1000", f"LISPools: {self.venue_2}"]
            strategies_wizard = ExecutionStrategiesWizard(self.web_driver_container)
            parameters = strategies_wizard.get_all_parameters_names_from_dark_block()
            values = strategies_wizard.get_all_parameters_values_from_dark_block()
            actual_parameter_and_value_at_dark_block = [a + " " + str(b) for a, b in zip(parameters, values)]
            self.verify("After saved at Dark block", expected_parameter_and_value_at_dark_block,
                        actual_parameter_and_value_at_dark_block)

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
