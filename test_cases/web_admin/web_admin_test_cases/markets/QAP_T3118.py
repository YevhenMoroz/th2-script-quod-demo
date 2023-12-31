import time

from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.markets.routes.main_page import RoutesPage
from test_framework.web_admin_core.pages.markets.routes.strategy_type_subwizard import \
    RoutesStrategyTypeSubWizard
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T3118(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.strategy_type = "Lit and Dark SOR"
        self.default_scenario = 'Quod Financial Lit and Dark SOR'

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        time.sleep(2)
        side_menu = SideMenu(self.web_driver_container)
        side_menu.open_routes_page()

    def test_context(self):
        self.precondition()

        routes_main_menu = RoutesPage(self.web_driver_container)
        routes_main_menu.click_on_new_button()
        strategy_type_sub_wizard = RoutesStrategyTypeSubWizard(self.web_driver_container)
        strategy_type_sub_wizard.set_strategy_type_at_strategy_type_tab(self.strategy_type)
        strategy_type_sub_wizard.click_on_default_scenario()
        strategy_type_sub_wizard.set_default_scenario_at_strategy_type_tab(self.default_scenario)

        self.verify("Default Scenario has been select", self.default_scenario,
                    strategy_type_sub_wizard.get_default_scenario_at_strategy_type_tab())
