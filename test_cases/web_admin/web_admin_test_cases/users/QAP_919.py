import sys
import time
import traceback

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.pages.users.users.users_client_sub_wizard import \
    UsersClientSubWizard
from test_framework.web_admin_core.pages.users.users.users_page import UsersPage
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_919(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = "adm02"
        self.password = "Zxcvbn123!"
        self.client = "CLIENT1"
        self.type = "Holder"
        self.empty_data_error_message = "Incorrect or missing values"
        self.duplicate_error_message = "Such a record already exists"

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        time.sleep(2)
        side_menu.open_users_page()
        users_page = UsersPage(self.web_driver_container)
        time.sleep(2)
        users_page.click_on_more_actions()
        time.sleep(2)
        users_page.click_on_edit_at_more_actions()
        time.sleep(2)

    def test_context(self):
        client_sub_wizard = UsersClientSubWizard(self.web_driver_container)
        try:
            self.precondition()
            client_sub_wizard.click_on_plus_button()
            time.sleep(2)
            client_sub_wizard.click_on_checkmark_button()
            time.sleep(2)
            try:
                self.verify("Client was not add with empty data. Error message displayed",
                            self.empty_data_error_message, client_sub_wizard.get_error_message())
            except Exception as e:
                self.verify("Error message for empty data is not displayed", True, e.__class__.__name__)

            client_sub_wizard.add_non_existing_client(self.type, self.client)
            try:
                self.verify("Non existing client is not add",
                            self.empty_data_error_message, client_sub_wizard.get_error_message())
            except Exception as e:
                self.verify("Non existing client add", True, e.__class__.__name__)

            time.sleep(2)
            client_sub_wizard.add_new_client(self.client, self.type)
            client_sub_wizard.click_on_plus_button()
            time.sleep(2)
            client_sub_wizard.add_new_client(self.client, self.type)
            time.sleep(2)
            try:
                self.verify("Is 'Such record already exist' exception displayed",
                            self.duplicate_error_message, client_sub_wizard.get_error_message())
            except Exception as e:
                self.verify("Error message for duplicate user is not displayed", True, e.__class__.__name__)

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
