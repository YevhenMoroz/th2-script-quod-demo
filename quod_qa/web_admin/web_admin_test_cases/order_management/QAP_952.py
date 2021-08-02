import time
import traceback

from custom import basic_custom_actions
from quod_qa.web_admin.web_admin_core.pages.login.login_page import LoginPage
from quod_qa.web_admin.web_admin_core.pages.order_management.execution_strategies.execution_strategies_general_sub_wizard import \
    ExecutionStrategiesGeneralSubWizard
from quod_qa.web_admin.web_admin_core.pages.order_management.execution_strategies.execution_strategies_page import \
    ExecutionStrategiesPage
from quod_qa.web_admin.web_admin_core.pages.order_management.execution_strategies.execution_strategies_wizard import \
    ExecutionStrategiesWizard
from quod_qa.web_admin.web_admin_core.pages.root.side_menu import SideMenu
from quod_qa.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer
from quod_qa.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_952(CommonTestCase):
    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id)
        self.console_error_lvl_id = second_lvl_id
        self.expected_error = "Incorrect or missing values"
        self.strategy_type = "Quod LitDark"
        self.user = "adm01"
        self.client = "BROKER"
        self.default_tif = "Day"
        self.aggressor_indicator = "True"

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.set_login("adm07")
        login_page.set_password("adm07")
        login_page.click_login_button()
        login_page.check_is_login_successful()
        side_menu = SideMenu(self.web_driver_container)
        side_menu.open_execution_strategies_page()
        main_menu = ExecutionStrategiesPage(self.web_driver_container)
        main_menu.click_on_new_button()
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
            strategies_wizard.set_client(self.client)
            strategies_wizard.set_default_tif(self.default_tif)
            strategies_wizard.set_aggressor_indicator(self.aggressor_indicator)
            strategies_wizard.click_on_general()
            general_block = ExecutionStrategiesGeneralSubWizard(self.web_driver_container)
            general_block.click_on_plus_button()
            general_block.click_on_checkmark_button()
            self.verify("After click on checkmark at general without parameter", self.expected_error,
                        general_block.get_error_type_after_empty_saved())
        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.console_error_lvl_id,
                                              status='FAILED')
            print(traceback.format_exc() + " Search in ->  " + self.__class__.__name__)
