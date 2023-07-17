import random
import string
import time

from stubs import ROOT_DIR
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.root.side_menu import SideMenu

from test_framework.web_admin_core.pages.users.users.users_interface_preferences_sub_wizard import UsersInterfacePreferencesSubWizard
from test_framework.web_admin_core.pages.users.users.users_page import UsersPage
from test_framework.web_admin_core.pages.users.users.users_wizard import UsersWizard
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T10318(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.interface_pref_id = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.path_to_file = f'{ROOT_DIR}\\test_framework\\web_admin_core\\resources\\for_interface_preferences_tests.txt'
        self.error_message = 'Incorrect or missing values'

        self.user_id = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.ext_id_client = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.email = '2@2'

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        side_menu = SideMenu(self.web_driver_container)

        login_page.login_to_web_admin(self.login, self.password)
        side_menu.open_users_page()

    def test_context(self):
        users_page = UsersPage(self.web_driver_container)
        interface_preferences_tab = UsersInterfacePreferencesSubWizard(self.web_driver_container)
        wizard = UsersWizard(self.web_driver_container)

        self.precondition()

        users_page.click_on_new_button()

        interface_preferences_tab.user_interface_preference_table.click_on_plus_button()
        interface_preferences_tab.user_interface_preference_table.set_interface_id(self.interface_pref_id)
        interface_preferences_tab.user_interface_preference_table.click_on_update_button_and_attach_file(self.path_to_file)
        interface_preferences_tab.user_interface_preference_table.click_on_cancel_button()
        time.sleep(1)
        interface_preferences_tab.user_interface_preference_table.click_on_plus_button()
        interface_preferences_tab.user_interface_preference_table.set_interface_id(self.interface_pref_id)
        interface_preferences_tab.user_interface_preference_table.click_on_checkmark_button()
        time.sleep(1)
        self.verify("New User Interface Preferences entry was not added",
                    self.error_message, wizard.get_footer_error_message_text())
