import random
import string
import time

from stubs import ROOT_DIR
from test_framework.web_admin_core.pages.general.common.common_page import CommonPage
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.pages.users.users.users_user_details_sub_wizard import \
    UsersUserDetailsSubWizard
from test_framework.web_admin_core.pages.users.users.users_values_sub_wizard import UsersValuesSubWizard
from test_framework.web_admin_core.pages.users.users.users_interface_preferences_sub_wizard import UsersInterfacePreferencesSubWizard
from test_framework.web_admin_core.pages.users.users.users_page import UsersPage
from test_framework.web_admin_core.pages.users.users.users_wizard import UsersWizard
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T10317(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.path_to_file = f'{ROOT_DIR}\\test_framework\\web_admin_core\\resources\\for_interface_preferences_tests.txt'
        self.file_content = ''

        self.user_id = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.ext_id_client = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.email = '2@2'
        self.interface_pref_id = f'TEST {self.__class__.__name__}'
        self.new_interface_pref_id = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        side_menu = SideMenu(self.web_driver_container)
        common_act = CommonPage(self.web_driver_container)

        self.file_content = [common_act.parse_from_file(self.path_to_file)]
        login_page.login_to_web_admin(self.login, self.password)
        side_menu.open_users_page()

    def test_context(self):
        users_page = UsersPage(self.web_driver_container)
        values_tab = UsersValuesSubWizard(self.web_driver_container)
        interface_preferences_tab = UsersInterfacePreferencesSubWizard(self.web_driver_container)
        details_tab = UsersUserDetailsSubWizard(self.web_driver_container)
        wizard = UsersWizard(self.web_driver_container)

        self.precondition()

        users_page.click_on_new_button()
        values_tab.set_user_id(self.user_id)
        values_tab.set_ext_id_client(self.ext_id_client)
        details_tab.set_mail(self.email)

        interface_preferences_tab.user_interface_preference_table.click_on_plus_button()
        interface_preferences_tab.user_interface_preference_table.set_interface_id(self.interface_pref_id)
        interface_preferences_tab.user_interface_preference_table.click_on_update_button_and_app_file(self.path_to_file)
        interface_preferences_tab.user_interface_preference_table.click_on_checkmark_button()
        wizard.click_on_save_changes()
        time.sleep(2)
        users_page.set_user_id(self.user_id)
        time.sleep(1)
        users_page.click_on_more_actions()
        users_page.click_on_edit_at_more_actions()
        time.sleep(1)
        interface_preferences_tab.user_interface_preference_table.click_on_edit_button()
        interface_preferences_tab.user_interface_preference_table.set_interface_id(self.new_interface_pref_id)
        interface_preferences_tab.user_interface_preference_table.click_on_checkmark_button()
        time.sleep(1)
        self.verify("No errors appears", False, wizard.is_warning_displayed())
        wizard.click_on_save_changes()
        time.sleep(2)
        users_page.set_user_id(self.user_id)
        time.sleep(1)
        users_page.click_on_more_actions()
        users_page.click_on_edit_at_more_actions()
        time.sleep(1)
        self.verify("User Interface Preference file the same",
                    self.file_content,
                    interface_preferences_tab.user_interface_preference_table.click_on_download_button_and_get_content())
