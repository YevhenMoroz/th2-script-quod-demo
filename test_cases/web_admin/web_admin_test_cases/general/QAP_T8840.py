import sys
import time
import traceback

from custom import basic_custom_actions
from stubs import ROOT_DIR
from test_framework.web_admin_core.pages.general.interface_preferences.main_page import MainPage
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T8840(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.path_to_file = f'{ROOT_DIR}\\test_framework\\web_admin_core\\resourses\\password_for_QAP_T3565.txt'
        self.interface_id = '123'
        self.name = '321'

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        side_menu.open_interface_preferences_page()

    def test_context(self):
        try:
            self.precondition()

            main_page = MainPage(self.web_driver_container)
            main_page.click_on_plus_button()
            time.sleep(1)
            main_page.send_upload_file(self.path_to_file)
            main_page.set_interface_id(self.interface_id)
            main_page.set_name(self.name)
            main_page.click_on_save_checkmark()

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
