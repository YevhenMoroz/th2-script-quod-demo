import random
import string
import time

from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.pages.users.users.users_user_details_sub_wizard import \
    UsersUserDetailsSubWizard
from test_framework.web_admin_core.pages.general.common.common_page import CommonPage
from test_framework.web_admin_core.pages.users.users.users_values_sub_wizard import UsersValuesSubWizard
from test_framework.web_admin_core.pages.users.users.users_page import UsersPage
from test_framework.web_admin_core.pages.users.users.users_wizard import UsersWizard

from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T8890(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")

        self.email = '2@2'
        self.user_id = self.__class__.__name__
        self.ext_id_client = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.user_password = 'Qwerty123!'
        self.new_password = 'QWEasd123!'
        self.wrong_password = 'ASDasd123!'
        self.error_message = ['Incorrect or missing values', 'New passwords don\'t match']

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        side_menu = SideMenu(self.web_driver_container)
        users_page = UsersPage(self.web_driver_container)
        values_tab = UsersValuesSubWizard(self.web_driver_container)
        details_tab = UsersUserDetailsSubWizard(self.web_driver_container)
        common_act = CommonPage(self.web_driver_container)
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
            users_page.click_on_more_actions()
            users_page.click_on_edit_at_more_actions()
            values_tab.click_on_change_password()
            values_tab.set_new_password(self.user_password)
            values_tab.set_confirm_new_password(self.user_password)
            values_tab.accept_or_cancel_confirmation_new_password(True)
            time.sleep(5)
            wizard.click_on_save_changes()
            time.sleep(1)

        common_act.click_on_user_icon()
        common_act.click_on_logout()
        time.sleep(2)
        login_page.login_to_web_admin(self.user_id, self.user_password)

    def test_context(self):
        login_page = LoginPage(self.web_driver_container)
        values_tab = UsersValuesSubWizard(self.web_driver_container)
        common_act = CommonPage(self.web_driver_container)

        self.precondition()

        common_act.click_on_user_icon()
        time.sleep(1)
        common_act.click_on_change_password_in_user_menu()

        time.sleep(1)
        expected_result = ["Pop-up appears: True",
                           "Current Password field displayed: True",
                           "New Password field displayed: True",
                           "Confirm New Password field displayed: True"]
        actual_result = [f"Pop-up appears: {common_act.is_change_password_pop_up_displayed()}",
                         f"Current Password field displayed: {common_act.is_current_password_field_displayed_in_change_password_pop_up()}"
                         f"New Password field displayed: {common_act.is_new_password_filed_displayed_in_change_password_pop_up()}",
                         f"Confirm New Password field displayed: {common_act.is_confirm_new_password_field_displayed_in_change_password_pop_up()}"]
        self.verify("Change Password pop-up appears", expected_result, actual_result)

        common_act.click_on_change_password_button_in_change_password_pop_up()
        time.sleep(1)
        self.verify("Incorrect or missing values appears",
                    self.error_message[0], values_tab.get_error_message_text_in_change_password_pop_up())
        common_act.set_current_password_in_change_password_pop_up(self.user_password)
        common_act.set_new_password_in_change_password_pop_up(self.new_password)
        common_act.set_confirm_new_password_in_change_password_pop_up(self.wrong_password)
        common_act.click_on_change_password_button_in_change_password_pop_up()
        time.sleep(1)
        self.verify("New passwords don't match appears",
                    self.error_message[1], values_tab.get_error_message_text_in_change_password_pop_up())
        common_act.set_current_password_in_change_password_pop_up(self.ext_id_client)
        common_act.set_new_password_in_change_password_pop_up(self.new_password)
        common_act.set_confirm_new_password_in_change_password_pop_up(self.wrong_password)
        common_act.click_on_change_password_button_in_change_password_pop_up()
        time.sleep(1)
        self.verify("New passwords don't match appears",
                    self.error_message[1], values_tab.get_error_message_text_in_change_password_pop_up())
        common_act.click_on_cancel_button()
        time.sleep(1)
        common_act.click_on_user_icon()
        common_act.click_on_logout()
        time.sleep(5)
        login_page.login_to_web_admin(self.user_id, self.user_password)
        time.sleep(1)
        self.verify("Login with common password successful", True, common_act.is_user_icon_displayed())
