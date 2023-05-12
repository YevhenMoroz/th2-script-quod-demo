import random
import string
import sys
import time
import traceback

from datetime import datetime, timedelta
from custom import basic_custom_actions
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.pages.general.common.common_page import CommonPage
from test_framework.web_admin_core.pages.users.users.users_assignments_sub_wizard import UsersAssignmentsSubWizard
from test_framework.web_admin_core.pages.users.users.users_values_sub_wizard import UsersValuesSubWizard
from test_framework.web_admin_core.pages.users.users.users_user_details_sub_wizard import UsersUserDetailsSubWizard
from test_framework.web_admin_core.pages.users.users.users_page import UsersPage
from test_framework.web_admin_core.pages.users.users.users_wizard import UsersWizard
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T3679(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.user_id = "QAP-T3679"
        self.ext_id_client = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.desks = [self.data_set.get_desk("desk_1"), self.data_set.get_desk("desk_3")]
        self.email = self.data_set.get_email("email_1")
        self.password_expiration = datetime.strftime(datetime.now() - timedelta(1), '%m/%d/%Y')
        self.new_password = 'Qwerty123!@'

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        side_menu.open_users_page()
        users_page = UsersPage(self.web_driver_container)
        users_page.set_user_id(self.user_id)
        time.sleep(1)
        if not users_page.is_searched_user_found(self.user_id):
            users_page.click_on_new_button()
            values_wizard = UsersValuesSubWizard(self.web_driver_container)
            values_wizard.set_user_id(self.user_id)
            values_wizard.set_ext_id_client(self.ext_id_client)
            values_wizard.set_password_expiration(self.password_expiration)
            user_details_sub_wizard = UsersUserDetailsSubWizard(self.web_driver_container)
            user_details_sub_wizard.set_mail(self.email)
            assignments_sub_wizard = UsersAssignmentsSubWizard(self.web_driver_container)
            assignments_sub_wizard.click_on_desks()
            assignments_sub_wizard.set_desks(self.desks)
            users_wizard = UsersWizard(self.web_driver_container)
            users_wizard.click_on_save_changes()
            users_page.set_user_id(self.user_id)
            time.sleep(1)
            users_page.click_on_more_actions()
            users_page.click_on_edit_at_more_actions()
            values_wizard.click_on_change_password()
            values_wizard.set_password(self.new_password)
            values_wizard.set_confirm_new_password(self.new_password)
            values_wizard.accept_or_cancel_confirmation_new_password(True)
            users_wizard.click_on_save_changes()

        else:
            users_page.click_on_more_actions()
            users_page.click_on_edit_at_more_actions()
            values_wizard = UsersValuesSubWizard(self.web_driver_container)
            values_wizard.set_password_expiration(self.password_expiration)
            users_wizard = UsersWizard(self.web_driver_container)
            users_wizard.click_on_save_changes()

    def test_context(self):
        try:
            self.precondition()

            common_page = CommonPage(self.web_driver_container)
            common_page.click_on_info_error_message_pop_up()
            common_page.click_on_user_icon()
            time.sleep(1)
            common_page.click_on_logout()
            time.sleep(2)
            login_page = LoginPage(self.web_driver_container)
            login_page.set_login(self.user_id)
            login_page.set_password(self.new_password)
            login_page.click_login_button()
            time.sleep(2)

            self.verify("Change password page is open", True, login_page.is_change_password_page_opened())

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
