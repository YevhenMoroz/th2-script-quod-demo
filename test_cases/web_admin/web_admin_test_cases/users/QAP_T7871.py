import sys
import time
import random
import string
import traceback

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.pages.users.users.users_page import UsersPage
from test_framework.web_admin_core.pages.users.users.users_wizard import UsersWizard
from test_framework.web_admin_core.pages.users.users.users_values_sub_wizard import UsersValuesSubWizard
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T7871(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.test_data = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        time.sleep(2)
        side_menu = SideMenu(self.web_driver_container)
        side_menu.open_users_page()
        time.sleep(2)

    def test_context(self):
        try:
            self.precondition()
            users_page = UsersPage(self.web_driver_container)
            users_page.click_on_more_actions()
            time.sleep(1)
            users_page.click_on_edit_at_more_actions()
            time.sleep(2)
            wizard = UsersWizard(self.web_driver_container)
            self.verify("[REVERT CHANGES] btn become disable after click", False,
                        wizard.is_revert_changes_button_enabled())
            value_tab = UsersValuesSubWizard(self.web_driver_container)
            default_ext_id_client = value_tab.get_ext_id_client()
            default_ext_id_venue = value_tab.get_ext_id_venue()
            value_tab.set_ext_id_client(self.test_data)
            value_tab.set_ext_id_venue(self.test_data)
            time.sleep(1)
            self.verify("[REVERT CHANGES] btn become enable", True,
                        wizard.is_revert_changes_button_enabled())

            wizard.click_on_clear_changes()
            time.sleep(1)
            self.verify("Data has been revert",
                        [default_ext_id_client, default_ext_id_venue],
                        [value_tab.get_ext_id_client(), value_tab.get_ext_id_venue()])
            self.verify("[REVERT CHANGES] btn become disable after click", False,
                        wizard.is_revert_changes_button_enabled())

            value_tab.set_ext_id_client(self.test_data)
            value_tab.set_ext_id_venue(self.test_data)
            time.sleep(1)
            wizard = UsersWizard(self.web_driver_container)
            self.verify("[REVERT CHANGES] btn become enable", True,
                        wizard.is_revert_changes_button_enabled())

            wizard.click_on_clear_changes()
            time.sleep(1)
            self.verify("Data has been revert",
                        [default_ext_id_client, default_ext_id_venue],
                        [value_tab.get_ext_id_client(), value_tab.get_ext_id_venue()])
            self.verify("[REVERT CHANGES] btn become disable after click", False,
                        wizard.is_revert_changes_button_enabled())

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
