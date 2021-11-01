import time
import traceback

from custom import basic_custom_actions
from quod_qa.web_admin.web_admin_core.pages.login.login_page import LoginPage
from quod_qa.web_admin.web_admin_core.pages.order_management.execution_strategies.execution_strategies_page import \
    ExecutionStrategiesPage
from quod_qa.web_admin.web_admin_core.pages.root.side_menu import SideMenu
from quod_qa.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer
from quod_qa.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_4264(CommonTestCase):
    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id)
        self.name = "Default"

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.set_login("adm03")
        login_page.set_password("adm03")
        login_page.click_login_button()
        login_page.check_is_login_successful()
        side_menu = SideMenu(self.web_driver_container)
        side_menu.open_execution_strategies_page()
        time.sleep(2)
        main_menu = ExecutionStrategiesPage(self.web_driver_container)
        main_menu.set_name_at_filter_field(self.name)
        time.sleep(1)

    def test_context(self):
        try:
            self.precondition()
            main_menu = ExecutionStrategiesPage(self.web_driver_container)
            try:
                main_menu.click_on_enabled_filter()
                time.sleep(2)
                main_menu.set_enabled_at_filter_field("true")
                time.sleep(2)
                main_menu.click_on_more_actions()
                self.verify("Default strategy is enabled and has checkmark in main page", True, True)
            except Exception:
                self.verify("Default strategy is disabled", True, False)

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            print(traceback.format_exc() + " Search in ->  " + self.__class__.__name__)
