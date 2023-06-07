import random
import string
import sys
import time
import traceback

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.pages.users.user_lists.main_page import MainPage
from test_framework.web_admin_core.pages.users.user_lists.wizard import *

from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T11215(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")

        self.user_list_name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.user = self.data_set.get_user("user_8")

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        side_menu = SideMenu(self.web_driver_container)

        login_page.login_to_web_admin(self.login, self.password)
        side_menu.open_user_lists_page()

    def test_context(self):
        user_lists_page = MainPage(self.web_driver_container)
        wizard = Wizard(self.web_driver_container)
        values_tab = ValuesTab(self.web_driver_container)

        try:
            self.precondition()

            user_lists_page.click_on_new_button()
            values_tab.set_user_list_name(self.user_list_name)
            values_tab.click_on_plus_button()
            values_tab.set_user(self.user)
            values_tab.click_on_save_checkmark_button()
            wizard.click_on_save_changes_button()
            time.sleep(1)
            user_lists_page.set_name_filter(self.user_list_name)
            time.sleep(1)
            self.verify("User List has been created", True, user_lists_page.is_user_lists_found(self.user_list_name))

        except Exception:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            errors = f'"{[traceback.extract_tb(exc_traceback, limit=4)]}"'.replace("\\", "/")
            basic_custom_actions.create_event(f"FAILED", self.test_case_id, status='FAILED',
                                              body="[{\"type\": \"message\", \"data\":" + f"{errors}" + "}]")
            traceback.print_tb(exc_traceback, limit=3, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
