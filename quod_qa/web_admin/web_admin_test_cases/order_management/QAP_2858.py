import time

from quod_qa.web_admin.web_admin_core.pages.login.login_page import LoginPage
from quod_qa.web_admin.web_admin_core.pages.order_management.execution_strategies.execution_strategies_lit_passive_sub_wizard import \
    ExecutionStrategiesLitPassiveSubWizard
from quod_qa.web_admin.web_admin_core.pages.order_management.execution_strategies.execution_strategies_page import \
    ExecutionStrategiesPage
from quod_qa.web_admin.web_admin_core.pages.order_management.execution_strategies.execution_strategies_wizard import \
    ExecutionStrategiesWizard
from quod_qa.web_admin.web_admin_core.pages.root.side_menu import SideMenu
from quod_qa.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer
from quod_qa.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_2858(CommonTestCase):
    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id)
        self.strategy_type = "Quod LitDark"
        self.parameter_at_passive_lit_block = "PostMode"

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
        time.sleep(1)
        strategies_wizard.set_strategy_type(self.strategy_type)
        strategies_wizard.click_on_lit_passive()
        passive_at_lit_block = ExecutionStrategiesLitPassiveSubWizard(self.web_driver_container)
        passive_at_lit_block.click_on_plus_button()
        passive_at_lit_block.set_parameter(self.parameter_at_passive_lit_block)

    def test_context(self):
        self.precondition()
        passive_at_lit_block = ExecutionStrategiesLitPassiveSubWizard(self.web_driver_container)
        values_at_post_mode_parameter = ["NoPost", "Spraying", "StatMarketShare", "Single"]
        self.verify("Is PostMode values exist", True,
                    passive_at_lit_block.is_post_mode_values_exist(values_at_post_mode_parameter))
