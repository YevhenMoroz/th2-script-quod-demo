import time

from quod_qa.web_admin.web_admin_core.pages.login.login_page import LoginPage
from quod_qa.web_admin.web_admin_core.pages.others.routes.routes_page import RoutesPage
from quod_qa.web_admin.web_admin_core.pages.others.routes.routes_wizard import RoutesWizard
from quod_qa.web_admin.web_admin_core.pages.root.side_menu import SideMenu
from quod_qa.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer
from quod_qa.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_1738(CommonTestCase):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container, self.__class__.__name__)
        self.name = "test1738"

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
        routes_wizard.click_on_save_changes()

    def test_context(self):
        self.precondition()
        routes_wizard = RoutesWizard(self.web_driver_container)
        self.verify("Error after click on next button", "Incorrect or missing values",
                    routes_wizard.get_actual_error_after_click_on_next_in_empty_page())
        routes_wizard.set_name_at_values_tab(self.name)
        routes_wizard.click_on_save_changes()
        routes_main_menu = RoutesPage(self.web_driver_container)
        routes_main_menu.set_name_at_filter(self.name)
        time.sleep(2)
        self.verify("Correctly name saved", self.name, routes_main_menu.get_name_value())
        time.sleep(1)
        routes_main_menu.click_on_more_actions()
        routes_main_menu.click_on_delete_at_more_actions()
        routes_main_menu.click_on_ok()
