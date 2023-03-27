import random
import string
import sys
import time
import traceback

from stubs import ROOT_DIR
from custom import basic_custom_actions
from test_framework.web_admin_core.pages.general.common.common_page import CommonPage
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.pages.users.users.users_values_sub_wizard import UsersValuesSubWizard
from test_framework.web_admin_core.pages.users.users.users_user_details_sub_wizard import UsersUserDetailsSubWizard
from test_framework.web_admin_core.pages.users.users.users_page import UsersPage
from test_framework.web_admin_core.pages.users.users.users_wizard import UsersWizard
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T3565(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.user_id = 'QAP-T3565'
        self.new_password = 'Qwe!'.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.current_password = ""
        self.email = '2@2'
        self.path_to_file = f'{ROOT_DIR}\\test_framework\\web_admin_core\\resourses\\password_for_QAP_T3565.txt'

    def read_password_from_file(self):
        try:
            with open(self.path_to_file, "r") as file:
                self.current_password = file.readline()
        except FileNotFoundError as e:
            self.verify("File with password not found", True, e.__class__.__name__)
        finally:
            file.close()

    def write_password_in_file(self):
        try:
            with open(self.path_to_file, "w") as file:
                self.current_password = self.new_password
                file.write(self.current_password)
        except FileNotFoundError as e:
            self.verify("File with password not found", True, e.__class__.__name__)
        finally:
            file.close()

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        time.sleep(2)
        side_menu.open_users_page()
        users_page = UsersPage(self.web_driver_container)
        time.sleep(2)
        users_page.set_user_id(self.user_id)
        time.sleep(2)
        values_tab = UsersValuesSubWizard(self.web_driver_container)
        details_tab = UsersUserDetailsSubWizard(self.web_driver_container)
        users_wizard = UsersWizard(self.web_driver_container)

        if not users_page.is_searched_user_found(self.user_id):
            users_page.click_on_new_button()
            values_tab.set_user_id(self.user_id)
            values_tab.set_ext_id_client(self.user_id)
            details_tab.set_mail(self.email)
            users_wizard.click_on_save_changes()
            users_page.set_user_id(self.user_id)
            time.sleep(1)
            users_page.click_on_more_actions()
            users_page.click_on_edit_at_more_actions()
            values_tab.click_on_change_password()
            self.read_password_from_file()
            values_tab.set_new_password(self.current_password)
            values_tab.set_confirm_new_password(self.current_password)
            values_tab.click_on_change_password()
            values_tab.set_first_time_login_checkbox()
            users_wizard.click_on_save_changes()
        else:
            users_page.click_on_more_actions()
            users_page.click_on_edit_at_more_actions()
            if not values_tab.is_first_time_login_checkbox_selected():
                values_tab.set_first_time_login_checkbox()
            users_wizard.click_on_save_changes()

        time.sleep(2)
        common_page = CommonPage(self.web_driver_container)
        common_page.click_on_info_error_message_pop_up()
        time.sleep(1)
        common_page.click_on_user_icon()
        time.sleep(1)
        common_page.click_on_logout()
        time.sleep(2)
        login_page.set_login(self.user_id)
        time.sleep(1)
        self.read_password_from_file()
        time.sleep(1)
        login_page.set_password(self.current_password)
        time.sleep(1)
        login_page.click_login_button()
        time.sleep(2)

    def test_context(self):
        try:
            self.precondition()
            common_page = CommonPage(self.web_driver_container)
            login_page = LoginPage(self.web_driver_container)
            common_page.set_old_password_at_login_page(self.current_password)
            common_page.set_new_password_at_login_page(self.new_password)
            common_page.set_confirm_new_password(self.new_password)
            common_page.click_on_change_password()
            time.sleep(2)
            login_page.login_to_web_admin(self.user_id, self.new_password)
            time.sleep(2)
            self.verify("User password edited correctly", True, True)
            self.write_password_in_file()
        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            pexc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
