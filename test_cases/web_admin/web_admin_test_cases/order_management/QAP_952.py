import sys
import time
import traceback

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


class QAP_952(CommonTestCase):
    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.expected_error = "Incorrect or missing values"
        self.strategy_type = "External AMBUSH"
        self.user = self.data_set.get_user("user_4")
        self.client = self.data_set.get_client("client_4")
        self.default_tif = self.data_set.get_default_tif("default_tif_1")
        self.aggressor_indicator = "True"

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.set_login(self.login)
        login_page.set_password(self.password)
        login_page.click_login_button()
        login_page.check_is_login_successful()
        side_menu = SideMenu(self.web_driver_container)
        side_menu.open_execution_strategies_page()
        side_menu.wait_for_button_to_become_active()
        main_menu = ExecutionStrategiesPage(self.web_driver_container)
        main_menu.click_on_new_button()
        time.sleep(2)
        strategies_wizard = ExecutionStrategiesWizard(self.web_driver_container)
        strategies_wizard.click_on_save_changes()

    def test_context(self):
        try:
            self.precondition()
            strategies_wizard = ExecutionStrategiesWizard(self.web_driver_container)
            self.verify("After click on save in empty wizard", self.expected_error,
                        strategies_wizard.get_error_type_after_empty_saved())
            time.sleep(2)
            strategies_wizard.set_strategy_type(self.strategy_type)
            strategies_wizard.click_on_save_changes()
            self.verify("After click on save without name", self.expected_error,
                        strategies_wizard.get_error_type_after_empty_saved())
            strategies_wizard.set_user(self.user)
            time.sleep(1)
            strategies_wizard.set_client(self.client)
            time.sleep(1)
            strategies_wizard.set_default_tif(self.default_tif)
            time.sleep(1)
            strategies_wizard.set_aggressor_indicator(self.aggressor_indicator)
            time.sleep(1)
            strategies_wizard.click_on_general()
            general_block = ExecutionStrategiesGeneralSubWizard(self.web_driver_container)
            general_block.click_on_plus_button()
            general_block.click_on_checkmark_button()
            self.verify("After click on checkmark at general without parameter", self.expected_error,
                        general_block.get_error_type_after_empty_saved())
        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
