import random
import string
import sys
import time
import traceback

from custom import basic_custom_actions
from test_cases.web_admin.web_admin_core.pages.login.login_page import LoginPage
from test_cases.web_admin.web_admin_core.pages.order_management.execution_strategies.execution_strategies_dark_sub_wizard import \
    ExecutionStrategiesDarkSubWizard
from test_cases.web_admin.web_admin_core.pages.order_management.execution_strategies.execution_strategies_page import \
    ExecutionStrategiesPage
from test_cases.web_admin.web_admin_core.pages.order_management.execution_strategies.execution_strategies_wizard import \
    ExecutionStrategiesWizard
from test_cases.web_admin.web_admin_core.pages.root.side_menu import SideMenu
from test_cases.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_3331(CommonTestCase):
    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id)
        self.login = "adm03"
        self.password = "adm03"
        self.name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.user = "QA1"
        self.strategy_type = "Quod DarkPool"
        self.dark_parameter_1 = "LISPhase"
        self.dark_parameter_2 = "LISResidentTime"
        self.dark_parameter_3 = "LISPools"
        self.venue = "ADX"

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        side_menu.open_execution_strategies_page()
        time.sleep(2)
        main_menu = ExecutionStrategiesPage(self.web_driver_container)
        main_menu.click_on_new_button()
        strategies_wizard = ExecutionStrategiesWizard(self.web_driver_container)
        time.sleep(2)
        strategies_wizard.set_strategy_type(self.strategy_type)
        time.sleep(1)
        strategies_wizard.set_user(self.user)
        time.sleep(1)
        strategies_wizard.set_name(self.name)
        time.sleep(1)
        strategies_wizard.click_on_dark_block()
        time.sleep(2)
        dark_sub_wizard = ExecutionStrategiesDarkSubWizard(self.web_driver_container)
        dark_sub_wizard.click_on_plus_button()
        time.sleep(1)
        dark_sub_wizard.set_parameter(self.dark_parameter_1)
        dark_sub_wizard.set_checkbox()
        time.sleep(1)
        dark_sub_wizard.click_on_checkmark_button()
        time.sleep(1)
        dark_sub_wizard.click_on_plus_button()
        time.sleep(1)
        dark_sub_wizard.set_parameter(self.dark_parameter_2)
        time.sleep(1)
        dark_sub_wizard.set_value("11")
        time.sleep(1)
        dark_sub_wizard.click_on_checkmark_button()
        time.sleep(1)
        dark_sub_wizard.click_on_plus_button()
        time.sleep(1)
        dark_sub_wizard.set_parameter(self.dark_parameter_3)
        time.sleep(1)
        dark_sub_wizard.click_on_plus_at_actions_sub_wizard()
        time.sleep(1)
        dark_sub_wizard.set_venue_at_actions_sub_wizard(self.venue)
        time.sleep(1)
        dark_sub_wizard.click_on_checkmark_at_actions_sub_wizard()
        time.sleep(1)
        dark_sub_wizard.click_on_checkmark_button()
        time.sleep(1)

    def test_context(self):

        try:
            self.precondition()
            strategies_wizard = ExecutionStrategiesWizard(self.web_driver_container)
            strategies_wizard.click_on_go_back_button()
            time.sleep(1)
            strategies_wizard.click_on_save_changes()
            time.sleep(1)
            strategies_page = ExecutionStrategiesPage(self.web_driver_container)
            strategies_page.set_name_at_filter_field(self.name)
            time.sleep(2)
            strategies_page.click_on_more_actions()
            time.sleep(2)
            strategies_page.click_on_edit_at_more_actions()
            time.sleep(2)
            expected_parameter_and_value_at_dark_block = ["LISPhase: ", "Y"]
            actual_parameter_and_value_at_dark_block = [strategies_wizard.get_parameter_name_at_dark_block(),
                                                        strategies_wizard.get_parameter_value_at_dark_block()]
            self.verify("After saved at Dark block", expected_parameter_and_value_at_dark_block,
                        actual_parameter_and_value_at_dark_block)

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
