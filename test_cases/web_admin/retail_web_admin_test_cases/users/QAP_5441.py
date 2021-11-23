import random
import string
import time
import traceback

from custom import basic_custom_actions
from test_cases.web_admin.web_admin_core.pages.login.login_page import LoginPage
from test_cases.web_admin.web_admin_core.pages.root.side_menu import SideMenu
from test_cases.web_admin.web_admin_core.pages.users.users.users_login_sub_wizard import UsersLoginSubWizard
from test_cases.web_admin.web_admin_core.pages.users.users.users_page import UsersPage
from test_cases.web_admin.web_admin_core.pages.users.users.users_wizard import UsersWizard
from test_cases.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_5441(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id)
        self.login = "adm02"
        self.password = "adm02"
        self.institution = "QUOD FINANCIAL"
        self.ext_id_client = "test"
        self.user_id = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.password_for_new_user = "1111"

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        time.sleep(2)
        side_menu.open_users_page()
        time.sleep(2)
        users_page = UsersPage(self.web_driver_container)
        users_page.click_on_more_actions()
        time.sleep(2)
        users_page.click_on_edit_at_more_actions()
        time.sleep(2)
        login_sub_wizard = UsersLoginSubWizard(self.web_driver_container)
        login_sub_wizard.set_ext_id_client(self.ext_id_client)
        wizard = UsersWizard(self.web_driver_container)
        wizard.click_on_save_changes()
        time.sleep(2)

    def test_context(self):
        try:
            self.precondition()
            users_page = UsersPage(self.web_driver_container)
            self.verify("Is ext id client saved correctly after edited", self.ext_id_client,
                        users_page.get_ext_id_client())
            time.sleep(2)
            try:
                users_page.click_on_enable_disable_button()
                self.verify("User disabled correctly", expected_result=True, actual_result=True)
            except Exception as e:
                self.verify("User disabled correctly", expected_result=True, actual_result=e.__class__.__name__)
            time.sleep(2)
            users_page.click_on_new_button()
            time.sleep(2)
            login_sub_wizard = UsersLoginSubWizard(self.web_driver_container)
            try:
                login_sub_wizard.set_user_id(self.user_id)
                time.sleep(2)
                login_sub_wizard.set_generate_pin_code_checkbox()
                time.sleep(2)
                login_sub_wizard.set_password(self.password_for_new_user)
                time.sleep(2)
                wizard = UsersWizard(self.web_driver_container)
                wizard.click_on_save_changes()
                time.sleep(2)
                users_page.set_user_id(self.user_id)
            except Exception as e:
                self.verify("something went wrong during user creation", expected_result=True,
                            actual_result=e.__class__.__name__)
            try:
                users_page.click_on_more_actions()
                self.verify("New user created correctly", expected_result=True, actual_result=True)
            except Exception as e:
                self.verify("New user created incorrectly", expected_result=True, actual_result=e.__class__.__name__)

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            print(traceback.format_exc() + " Search in ->  " + self.__class__.__name__)
