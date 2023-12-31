import time

from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.pages.users.users.users_page import UsersPage
from test_framework.web_admin_core.pages.general.common.common_page import CommonPage
from test_framework.web_admin_core.pages.users.users.users_values_sub_wizard import UsersValuesSubWizard
from test_framework.web_admin_core.pages.users.users.users_wizard import UsersWizard
from test_framework.web_admin_core.pages.users.users.users_user_details_sub_wizard import UsersUserDetailsSubWizard
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T3920(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.user_for_login = self.data_set.get_user("user_1")
        self.password_for_login = self.data_set.get_password("password_1")
        self.user_for_block = self.data_set.get_user("user_13")
        self.email = 'email@email'
        self.wrong_password = "abcde"

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.user_for_login, self.password_for_login)
        side_menu = SideMenu(self.web_driver_container)
        side_menu.open_users_page()
        users_page = UsersPage(self.web_driver_container)
        users_page.set_user_id(self.user_for_block)
        time.sleep(1)
        if not users_page.is_searched_user_found(self.user_for_block):
            users_page.click_on_new_button()
            values_tab = UsersValuesSubWizard(self.web_driver_container)
            values_tab.set_user_id(self.user_for_block)
            values_tab.set_ext_id_client(self.user_for_block)
            details_tab = UsersUserDetailsSubWizard(self.web_driver_container)
            details_tab.set_mail(self.email)
            wizard = UsersWizard(self.web_driver_container)
            wizard.click_on_save_changes()

        common_act = CommonPage(self.web_driver_container)
        common_act.click_on_user_icon()
        common_act.click_on_logout()
        time.sleep(2)

        login_page.set_login(self.user_for_block)
        login_page.set_password(self.wrong_password)
        for i in range(52):
            login_page.click_login_button()
            time.sleep(1)
        self.web_driver_container.stop_driver()
        time.sleep(2)
        self.web_driver_container.start_driver()
        time.sleep(2)
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.user_for_login, self.password_for_login)
        side_menu = SideMenu(self.web_driver_container)
        side_menu.open_users_page()

    def test_context(self):
        self.precondition()

        users_page = UsersPage(self.web_driver_container)
        users_page.set_user_id(self.user_for_block)
        time.sleep(1)
        self.verify("User is locked", "lock", users_page.get_lock_unlock_status())
        time.sleep(1)
        users_page.click_on_lock_unlock_button()
        time.sleep(2)
        self.verify("User is unlocked", "unlock", users_page.get_lock_unlock_status())
