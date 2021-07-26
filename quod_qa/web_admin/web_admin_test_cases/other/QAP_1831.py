import time

from quod_qa.web_admin.web_admin_core.pages.login.login_page import LoginPage
from quod_qa.web_admin.web_admin_core.pages.others.routes.routes_page import RoutesPage
from quod_qa.web_admin.web_admin_core.pages.others.routes.routes_strategy_type_subwizard import \
    RoutesStrategyTypeSubWizard
from quod_qa.web_admin.web_admin_core.pages.others.routes.routes_wizard import RoutesWizard
from quod_qa.web_admin.web_admin_core.pages.root.side_menu import SideMenu
from quod_qa.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer
from quod_qa.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_1831(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer,second_lvl_id):
        super().__init__(web_driver_container, self.__class__.__name__,second_lvl_id)
        self.name = "qap 1831"
        self.default_scenario = "Custom one"

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.set_login("adm07")
        login_page.set_password("adm07")
        login_page.click_login_button()
        login_page.check_is_login_successful()
        side_menu = SideMenu(self.web_driver_container)
        side_menu.open_routes_page()
        time.sleep(2)
        routes_main_menu = RoutesPage(self.web_driver_container)
        routes_main_menu.click_on_new_button()
        routes_wizard = RoutesWizard(self.web_driver_container)
        time.sleep(2)
        routes_wizard.set_name_at_values_tab(self.name)
        strategy_type_sub_wizard = RoutesStrategyTypeSubWizard(self.web_driver_container)
        strategy_type_tuple = ("Custom one", "External CUSTOM1")
        strategy_type_sub_wizard.click_on_strategy_type_at_strategy_type_tab()
        strategy_type_sub_wizard.set_strategy_type_at_strategy_type_tab(strategy_type_tuple)
        strategy_type_sub_wizard.set_default_scenario_at_strategy_type_tab(self.default_scenario)
        routes_wizard.click_on_save_changes()
        routes_main_menu.set_name_at_filter(self.name)
        time.sleep(1)

    def test_context(self):
        self.precondition()
        routes_main_menu = RoutesPage(self.web_driver_container)
        self.verify("New Default Scenario after saved", self.default_scenario,
                    routes_main_menu.get_default_strategy_type_value())

        routes_main_menu.click_on_more_actions()

        expected_pdf_content = 'Route: "qap 1831"Values    Name: qap 1831    Client ID:     ES Instance:     ' \
                               'Description:     Support Contra Firm Commission: false    Counterpart: ' \
                               'List of RouteVenuesSymbolsStrategy Type    Default: Custom one1.   Custom one 2.   ' \
                               'External CUSTOM1 '
        self.verify(f"Is PDF contains {expected_pdf_content}", True,
                    routes_main_menu.click_download_pdf_entity_button_and_check_pdf(expected_pdf_content))
        routes_main_menu.click_on_more_actions()
        routes_main_menu.click_on_delete_at_more_actions()
        time.sleep(2)
        routes_main_menu.click_on_ok()
