import sys
import string
import random
import time
import traceback

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.order_management.execution_strategies.execution_strategies_lit_passive_sub_wizard import \
    ExecutionStrategiesLitPassiveSubWizard
from test_framework.web_admin_core.pages.order_management.execution_strategies.execution_strategies_page import \
    ExecutionStrategiesPage
from test_framework.web_admin_core.pages.order_management.execution_strategies.execution_strategies_wizard import \
    ExecutionStrategiesWizard
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T3116(CommonTestCase):
    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.user = self.data_set.get_user("user_8")
        self.strategy_type = self.data_set.get_strategy_type("strategy_type_1")
        self.parameter_at_passive_lit_block = ["PostMode", "VenueWeights"]
        self.venue = ["ADX", "MADRID"]
        self.post_mode = "Spraying"
        self.value = ["11", "22"]

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
            main_page.click_on_new_button()
            strategies_wizard = ExecutionStrategiesWizard(self.web_driver_container)
            strategies_wizard.set_user(self.user)
            strategies_wizard.set_name(self.name)
            strategies_wizard.set_strategy_type(self.strategy_type)
            strategies_wizard.click_on_lit_passive()
            passive_at_lit_block = ExecutionStrategiesLitPassiveSubWizard(self.web_driver_container)
            passive_at_lit_block.click_on_plus_button()
            passive_at_lit_block.set_parameter(self.parameter_at_passive_lit_block[0])
            passive_at_lit_block.set_value_by_dropdown_list_at_sub_wizard(self.post_mode)
            passive_at_lit_block.click_on_checkmark_button()

            passive_at_lit_block.click_on_plus_button()
            passive_at_lit_block.set_parameter(self.parameter_at_passive_lit_block[1])
            passive_at_lit_block.click_on_plus_at_actions_sub_wizard()
            passive_at_lit_block.set_value_at_actions_sub_wizard(self.venue[0])
            passive_at_lit_block.set_value(self.value[0])
            passive_at_lit_block.click_on_checkmark_at_actions_sub_wizard()
            passive_at_lit_block.click_on_plus_at_actions_sub_wizard()
            passive_at_lit_block.set_value_at_actions_sub_wizard(self.venue[1])
            passive_at_lit_block.set_value(self.value[1])
            passive_at_lit_block.click_on_checkmark_at_actions_sub_wizard()
            passive_at_lit_block.click_on_checkmark_button()
            passive_at_lit_block.click_on_go_back_button()

            strategies_wizard.click_on_save_changes()
            main_page.set_name_at_filter_field(self.name)
            time.sleep(1)

            self.verify("New Execution Strategy is saved", True, main_page.is_searched_execution_strategy_found(self.name))

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
