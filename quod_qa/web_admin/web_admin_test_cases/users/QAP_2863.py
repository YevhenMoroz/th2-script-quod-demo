import time
import traceback

from selenium.common.exceptions import TimeoutException

from custom import basic_custom_actions
from quod_qa.web_admin.web_admin_core.pages.login.login_page import LoginPage
from quod_qa.web_admin.web_admin_core.pages.root.side_menu import SideMenu
from quod_qa.web_admin.web_admin_core.pages.users.users.users_page import UsersPage
from quod_qa.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer
from quod_qa.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_2863(CommonTestCase):
    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id)
        self.console_error_lvl_id = second_lvl_id
        self.login = "adm02"
        self.password = "adm02"
        self.user_name= "buyside09"

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        time.sleep(2)
        side_menu.open_users_page()
        users_page = UsersPage(self.web_driver_container)
        time.sleep(2)
        users_page.set_user_id(self.user_name)
        time.sleep(2)
        users_page.click_on_enable_disable_button()
        time.sleep(2)

    def test_context(self):
        users_page = UsersPage(self.web_driver_container)
        try:
            self.precondition()
            try:
                users_page.click_on_more_actions()
                users_page.click_on_edit_at_more_actions()
                print("You must disabled first entity at users")
            except TimeoutException as e:
                error_name = e.__class__.__name__
                self.verify("user can not edit Disabled Entities", "TimeoutException", error_name)

            finally:
                time.sleep(2)
                users_page.click_on_enable_disable_button()


        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.console_error_lvl_id,
                                              status='FAILED')
            print(traceback.format_exc() + " Search in ->  " + self.__class__.__name__)
