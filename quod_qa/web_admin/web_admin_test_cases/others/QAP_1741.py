import time

from quod_qa.web_admin.web_admin_core.pages.login.login_page import LoginPage
from quod_qa.web_admin.web_admin_core.pages.others.routes.routes_page import RoutesPage
from quod_qa.web_admin.web_admin_core.pages.others.routes.routes_wizard import RoutesWizard
from quod_qa.web_admin.web_admin_core.pages.root.side_menu import SideMenu
from quod_qa.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer
from quod_qa.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_1741(CommonTestCase):
    def __init__(self, web_driver_container: WebDriverContainer,second_lvl_id):
        super().__init__(web_driver_container, self.__class__.__name__,second_lvl_id)
        self.name = "newName"
        self.new_name = "qap 1741"

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
        routes_wizard.set_name_at_values_tab(self.name)
        routes_wizard.click_on_save_changes()
        time.sleep(1)
        routes_main_menu.set_name_at_filter(self.name)
        routes_main_menu.click_on_more_actions()
        routes_main_menu.click_on_edit_at_more_actions()
        routes_wizard.set_name_at_values_tab(self.new_name)
        routes_wizard.click_on_save_changes()
        routes_main_menu.set_name_at_filter(self.new_name)
        time.sleep(2)

    def test_context(self):
        self.precondition()
        routes_main_menu = RoutesPage(self.web_driver_container)
        routes_wizard = RoutesWizard(self.web_driver_container)
        self.verify("Name after edited at main menu", self.new_name, routes_main_menu.get_name_value())
        routes_main_menu.click_on_more_actions()
        time.sleep(1)
        routes_main_menu.click_on_edit_at_more_actions()
        self.verify("Name after edited at values tab", self.new_name, routes_wizard.get_name_value_at_values_tab())
        routes_wizard.click_on_save_changes()
        routes_main_menu.set_name_at_filter(self.new_name)
        time.sleep(1)
        routes_main_menu.click_on_more_actions()
        time.sleep(1)
        routes_main_menu.click_on_delete_at_more_actions()
        time.sleep(1)
        routes_main_menu.click_on_ok()
