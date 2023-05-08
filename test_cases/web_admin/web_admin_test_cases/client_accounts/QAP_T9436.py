import sys
import time
import traceback
import random
import string

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.clients_accounts.client_lists.main_page import ClientListsPage
from test_framework.web_admin_core.pages.clients_accounts.client_lists.wizard import ClientListsWizard
from test_framework.web_admin_core.pages.general.common.common_page import CommonPage
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T9436(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None,
                 db_manager=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.db_manager = db_manager
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")

        self.client_list_name =  self.__class__.__name__
        self.client_list_description = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.clients = ["CLIENT1", "CLIENT2", "CLIENT3"]

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        side_menu = SideMenu(self.web_driver_container)
        client_list_page = ClientListsPage(self.web_driver_container)
        wizard = ClientListsWizard(self.web_driver_container)
        common_act = CommonPage(self.web_driver_container)

        login_page.login_to_web_admin(self.login, self.password)
        side_menu.open_client_list_page()
        client_list_page.set_name(self.client_list_name)
        time.sleep(1)
        if not client_list_page.is_client_list_found(self.client_list_name):
            client_list_page.click_on_new()
            wizard.set_client_list_name(self.client_list_name)
            wizard.set_client_list_description(self.client_list_description)
            for client in self.clients:
                wizard.click_on_plus()
                wizard.set_client(client)
                wizard.click_on_checkmark()

            wizard.click_on_save_changes()
            client_list_page.set_name(self.client_list_name)

            self.db_manager.my_db.execute(
                "UPDATE QUODSETTINGS SET settingvalue = '10' WHERE settingkey = 'WEB_ADMIN_CACHE_THRESHOLD'")
            common_act.refresh_page(True)
            time.sleep(2)
            client_list_page.set_name(self.client_list_name)
            time.sleep(1)

    def test_context(self):
        client_list_page = ClientListsPage(self.web_driver_container)
        wizard = ClientListsWizard(self.web_driver_container)

        try:
            self.precondition()

            client_list_page.click_on_more_actions()
            client_list_page.click_on_edit()
            time.sleep(1)
            expected_result = self.clients
            actual_result = wizard.get_all_client_from_table()
            self.verify("Saved client names displayed and not empty.", sorted(expected_result), sorted(actual_result))

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)

        finally:
            self.db_manager.my_db.execute(
                "UPDATE QUODSETTINGS SET settingvalue = '500' WHERE settingkey = 'WEB_ADMIN_CACHE_THRESHOLD'")
