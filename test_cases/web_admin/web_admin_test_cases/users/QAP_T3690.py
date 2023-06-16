import sys
import time
import traceback

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.pages.users.users.users_page import UsersPage
from test_framework.web_admin_core.pages.general.common.common_page import CommonPage

from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T3690(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None,
                 db_manager=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")

        self.db_manager = db_manager

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        side_menu = SideMenu(self.web_driver_container)

        login_page.login_to_web_admin(self.login, self.password)
        side_menu.open_users_page()

    def test_context(self):
        users_page = UsersPage(self.web_driver_container)
        common_act = CommonPage(self.web_driver_container)

        try:
            self.precondition()
            users_page.set_user_id("")
            time.sleep(1)
            self.verify("Users not displayed on the main page", True, users_page.is_users_displayed())

            self.db_manager.my_db.execute(
                "UPDATE QUODSETTINGS SET settingvalue = '10' WHERE settingkey = 'WEB_ADMIN_CACHE_THRESHOLD'")
            common_act.refresh_page(True)
            time.sleep(2)

            self.verify("Users not displayed on the main page", False, users_page.is_users_displayed())
            self.verify("Load users look up field displayed", True, users_page.is_load_users_look_up_displayed())
            users_page.set_user_id("")
            time.sleep(1)
            users_page.load_users_by_look_up_pattern(self.login)
            time.sleep(1)
            self.verify("Users not displayed on the main page", True, users_page.is_users_displayed())

        except Exception:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            errors = f'"{[traceback.extract_tb(exc_traceback, limit=4)]}"'.replace("\\", "/")
            basic_custom_actions.create_event(f"FAILED", self.test_case_id, status='FAILED',
                                              body="[{\"type\": \"message\", \"data\":" + f"{errors}" + "}]")
            traceback.print_tb(exc_traceback, limit=3, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)

        finally:
            self.db_manager.my_db.execute(
                "UPDATE QUODSETTINGS SET settingvalue = '500' WHERE settingkey = 'WEB_ADMIN_CACHE_THRESHOLD'")