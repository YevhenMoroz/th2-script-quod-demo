import sys
import time
import traceback
import random
import string

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.pages.users.users.users_values_sub_wizard import UsersValuesSubWizard
from test_framework.web_admin_core.pages.users.users.users_user_details_sub_wizard import UsersUserDetailsSubWizard
from test_framework.web_admin_core.pages.users.users.users_wizard import UsersWizard
from test_framework.web_admin_core.pages.users.users.users_assignments_sub_wizard import UsersAssignmentsSubWizard
from test_framework.web_admin_core.pages.users.users.users_page import UsersPage
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T3658(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")

        self.user_id = 'QAP-T3658'
        self.ext_id_client = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.email = '2@2'

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        time.sleep(2)
        side_menu = SideMenu(self.web_driver_container)
        side_menu.open_users_page()
        time.sleep(2)
        users_page = UsersPage(self.web_driver_container)
        users_page.set_user_id(self.user_id)
        time.sleep(1)
        if not users_page.is_searched_user_found(self.user_id):
            users_page.click_on_new_button()
            time.sleep(2)
            values_tab = UsersValuesSubWizard(self.web_driver_container)
            values_tab.set_user_id(self.user_id)
            values_tab.set_ext_id_client(self.ext_id_client)
            user_details_tab = UsersUserDetailsSubWizard(self.web_driver_container)
            user_details_tab.set_mail(self.email)
            wizard = UsersWizard(self.web_driver_container)
            wizard.click_on_save_changes()
            time.sleep(2)
            users_page.set_user_id(self.user_id)
            time.sleep(1)

    def post_conditions(self):
        assignments_tab = UsersAssignmentsSubWizard(self.web_driver_container)
        assignments_tab.select_technical_user_checkbox()
        wizard = UsersWizard(self.web_driver_container)
        wizard.click_on_save_changes()

    def test_context(self):
        try:
            self.precondition()

            users_page = UsersPage(self.web_driver_container)
            users_page.click_on_more_actions()
            time.sleep(1)
            users_page.click_on_edit_at_more_actions()
            time.sleep(2)
            assignments_tab = UsersAssignmentsSubWizard(self.web_driver_container)
            assignments_tab.select_technical_user_checkbox()
            wizard = UsersWizard(self.web_driver_container)
            wizard.click_on_save_changes()
            time.sleep(2)
            users_page.set_user_id(self.user_id)
            time.sleep(1)
            users_page.click_on_more_actions()
            time.sleep(1)
            users_page.click_on_edit_at_more_actions()
            time.sleep(2)

            self.verify("Technical user checkbox selected", True, assignments_tab.is_technical_user_selected())

            self.post_conditions()

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
