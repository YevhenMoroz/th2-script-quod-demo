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


class QAP_T11252(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")

        self.email = '2@2'
        self.user_id = self.__class__.__name__
        self.ext_id_client = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.first_name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        side_menu = SideMenu(self.web_driver_container)
        users_page = UsersPage(self.web_driver_container)
        values_tab = UsersValuesSubWizard(self.web_driver_container)
        details_tab = UsersUserDetailsSubWizard(self.web_driver_container)
        wizard = UsersWizard(self.web_driver_container)

        login_page.login_to_web_admin(self.login, self.password)
        side_menu.open_users_page()
        users_page.set_user_id(self.user_id)
        time.sleep(1)
        if not users_page.is_searched_user_found(self.user_id):
            users_page.click_on_new_button()
            values_tab.set_user_id(self.user_id)
            values_tab.set_ext_id_client(self.ext_id_client)
            details_tab.set_mail(self.email)
            details_tab.set_first_name(self.ext_id_client)
            wizard.click_on_save_changes()
            users_page.set_user_id(self.user_id)
            time.sleep(1)

        if users_page.is_user_enable_disable():
            users_page.click_on_enable_disable_button()
            time.sleep(1)

    def test_context(self):
        users_page = UsersPage(self.web_driver_container)
        wizard = UsersWizard(self.web_driver_container)
        details_tab = UsersUserDetailsSubWizard(self.web_driver_container)

        try:
            self.precondition()

            self.verify("User Disabled", False, users_page.is_user_enable_disable())
            users_page.click_on_more_actions()
            users_page.click_on_edit_at_more_actions()
            self.verify("Edit wizard open", True, wizard.is_wizard_open())
            details_tab.set_first_name(self.first_name)
            wizard.click_on_save_changes()
            time.sleep(1)
            self.verify("User still Disabled after modify", False, users_page.is_user_enable_disable())
            users_page.click_on_more_actions()
            users_page.click_on_edit_at_more_actions()
            self.verify("Edit wizard open", True, wizard.is_wizard_open())
            self.verify("User changed applied", self.first_name, details_tab.get_first_name())

        except Exception:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            errors = f'"{[traceback.extract_tb(exc_traceback, limit=4)]}"'.replace("\\", "/")
            basic_custom_actions.create_event(f"FAILED", self.test_case_id, status='FAILED',
                                              body="[{\"type\": \"message\", \"data\":" + f"{errors}" + "}]")
            traceback.print_tb(exc_traceback, limit=3, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
