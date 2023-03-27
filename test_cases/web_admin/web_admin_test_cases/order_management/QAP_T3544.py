import sys
import time
import traceback

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.order_management.execution_strategies.execution_strategies_page import \
    ExecutionStrategiesPage
from test_framework.web_admin_core.pages.order_management.execution_strategies.execution_strategies_wizard import \
    ExecutionStrategiesWizard
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T3544(CommonTestCase):
    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.user = self.data_set.get_user("user_8")
        self.strategy_type = self.data_set.get_strategy_type("strategy_type_9")

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

    def test_context(self):
        try:
            self.precondition()
            try:
                strategies_wizard = ExecutionStrategiesWizard(self.web_driver_container)
                time.sleep(2)
                strategies_wizard.set_strategy_type(self.strategy_type)
                strategies_wizard.click_on_lit_general()
                self.verify("General block is displayed", True, True)
            except Exception:
                self.verify("General block doesn't displayed", True, Exception.__class__.__name__)

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
