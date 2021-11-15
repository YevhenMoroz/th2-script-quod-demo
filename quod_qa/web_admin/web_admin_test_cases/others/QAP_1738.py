import random
import string
import time
import traceback

from custom import basic_custom_actions
from quod_qa.web_admin.web_admin_core.pages.login.login_page import LoginPage
from quod_qa.web_admin.web_admin_core.pages.others.routes.routes_page import RoutesPage
from quod_qa.web_admin.web_admin_core.pages.others.routes.routes_wizard import RoutesWizard
from quod_qa.web_admin.web_admin_core.pages.root.side_menu import SideMenu
from quod_qa.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer
from quod_qa.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_1738(CommonTestCase):
    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id)
        self.name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))

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
        try:
            self.precondition()
            routes_wizard = RoutesWizard(self.web_driver_container)
            self.verify("Error after click on next button", "Incorrect or missing values",
                        routes_wizard.get_actual_error_after_click_on_next_in_empty_page())
            routes_wizard.set_name_at_values_tab(self.name)
            routes_wizard.click_on_save_changes()
            time.sleep(2)
            routes_main_menu = RoutesPage(self.web_driver_container)
            routes_main_menu.set_name_at_filter(self.name)
            time.sleep(2)
            self.verify("Correctly name saved", self.name, routes_main_menu.get_name_value())
            time.sleep(1)
            routes_main_menu.click_on_more_actions()
            routes_main_menu.click_on_delete_at_more_actions()
        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            print(traceback.format_exc() + " Search in ->  " + self.__class__.__name__)
