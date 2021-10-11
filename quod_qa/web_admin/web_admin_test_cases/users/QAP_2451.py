import time
import traceback

from custom import basic_custom_actions
from quod_qa.web_admin.web_admin_core.pages.login.login_page import LoginPage
from quod_qa.web_admin.web_admin_core.pages.root.side_menu import SideMenu
from quod_qa.web_admin.web_admin_core.pages.users.users.users_page import UsersPage
from quod_qa.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer
from quod_qa.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_2451(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id)
        self.disabled_massage = "User adm_desk Disabled"
        self.console_error_lvl_id = second_lvl_id

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.set_login("adm02")
        login_page.set_password("adm02")
        login_page.click_login_button()
        login_page.check_is_login_successful()
        side_menu = SideMenu(self.web_driver_container)
        time.sleep(2)
        side_menu.open_users_page()
        time.sleep(2)

    def test_context(self):
        try:
            self.precondition()
            users_page = UsersPage(self.web_driver_container)
            users_page.set_user_id("adm_desk")
            time.sleep(2)
            users_page.click_on_enable_disable_button()
            self.verify("After click on disabled", self.disabled_massage, users_page.get_disabled_massage())
            time.sleep(1)
            users_page.click_on_enable_disable_button()
        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.console_error_lvl_id,
                                              status='FAILED')
            print(traceback.format_exc() + " Search in ->  " + self.__class__.__name__)
