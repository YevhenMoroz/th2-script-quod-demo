import time
import traceback

from selenium.common.exceptions import TimeoutException

from custom import basic_custom_actions
from test_cases.web_admin.web_admin_core.pages.login.login_page import LoginPage
from test_cases.web_admin.web_admin_core.pages.root.side_menu import SideMenu
from test_cases.web_admin.web_admin_core.pages.users.users.users_page import UsersPage
from test_cases.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_2863(CommonTestCase):
    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id)
        self.login = "adm02"
        self.password = "adm02"


    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        time.sleep(2)
        side_menu.open_users_page()
        users_page = UsersPage(self.web_driver_container)
        time.sleep(2)
        users_page.click_on_enable_disable_button()
        time.sleep(2)

    def test_context(self):
        users_page = UsersPage(self.web_driver_container)
        try:
            self.precondition()
            try:
                users_page.click_on_more_actions()
                time.sleep(2)
                users_page.click_on_edit_at_more_actions()
                self.verify("Error, disabled entity can change ", True, False)
            except TimeoutException as e:
                error_name = e.__class__.__name__
                self.verify("user can not edit Disabled Entities", "TimeoutException", error_name)

            finally:
                time.sleep(2)
                users_page.click_on_enable_disable_button()



        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            print(traceback.format_exc() + " Search in ->  " + self.__class__.__name__)
