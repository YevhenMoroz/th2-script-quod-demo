import random
import string
import sys
import time
import traceback

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.pages.users.users.users_user_details_sub_wizard import \
    UsersUserDetailsSubWizard
from test_framework.web_admin_core.pages.users.users.users_values_sub_wizard import UsersValuesSubWizard
from test_framework.web_admin_core.pages.users.users.users_page import UsersPage
from test_framework.web_admin_core.pages.users.users.users_wizard import UsersWizard

from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T3763(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.exist_ext_client_id = 'ijones'
        self.email = '2@2'
        self.user_id = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.ext_id_client = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        side_menu = SideMenu(self.web_driver_container)

        login_page.login_to_web_admin(self.login, self.password)
        side_menu.open_users_page()

    def test_context(self):
        users_page = UsersPage(self.web_driver_container)
        values_tab = UsersValuesSubWizard(self.web_driver_container)
        details_tab = UsersUserDetailsSubWizard(self.web_driver_container)
        wizard = UsersWizard(self.web_driver_container)

        try:
            self.precondition()

            users_page.click_on_new_button()
            details_tab.set_mail(self.email)
            wizard.click_on_save_changes()
            time.sleep(1)
            self.verify("User not save, error appear", True, wizard.is_warning_displayed())
            details_tab.set_mail('')
            values_tab.set_user_id(self.user_id)
            wizard.click_on_save_changes()
            time.sleep(1)
            self.verify("User not save, error appear", True, wizard.is_warning_displayed())
            values_tab.set_user_id('')
            values_tab.set_ext_id_client(self.ext_id_client)
            wizard.click_on_save_changes()
            time.sleep(1)
            self.verify("User not save, error appear", True, wizard.is_warning_displayed())
            values_tab.set_user_id(self.user_id)
            values_tab.set_ext_id_client(self.exist_ext_client_id)
            details_tab.set_mail(self.email)
            wizard.click_on_save_changes()
            time.sleep(1)
            self.verify("User not save, error appear", True, wizard.is_warning_displayed())

        except Exception:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            errors = f'"{[traceback.extract_tb(exc_traceback, limit=4)]}"'.replace("\\", "/")
            basic_custom_actions.create_event(f"FAILED", self.test_case_id, status='FAILED',
                                              body="[{\"type\": \"message\", \"data\":" + f"{errors}" + "}]")
            traceback.print_tb(exc_traceback, limit=3, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
