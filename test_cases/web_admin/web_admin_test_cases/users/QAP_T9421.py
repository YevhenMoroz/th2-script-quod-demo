import random
import string
import sys
import time
import traceback

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.pages.users.users.users_user_details_sub_wizard import \
    UsersUserDetailsSubWizard
from test_framework.web_admin_core.pages.users.users.users_client_sub_wizard import UsersClientSubWizard
from test_framework.web_admin_core.pages.users.users.users_values_sub_wizard import UsersValuesSubWizard
from test_framework.web_admin_core.pages.users.users.users_page import UsersPage
from test_framework.web_admin_core.pages.users.users.users_wizard import UsersWizard
from test_framework.web_admin_core.pages.general.common.common_page import CommonPage

from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T9421(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None,
                 db_manager=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.db_manager = db_manager

        self.email = '2@2'
        self.user_id = self.__class__.__name__
        self.ext_id_client = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.client = [self.data_set.get_client("client_1"), self.data_set.get_client("client_2")]
        self.type = 'BelongsTo'

    def precondition(self):
        values_tab = UsersValuesSubWizard(self.web_driver_container)
        details_tab = UsersUserDetailsSubWizard(self.web_driver_container)
        wizard = UsersWizard(self.web_driver_container)
        users_page = UsersPage(self.web_driver_container)
        login_page = LoginPage(self.web_driver_container)
        side_menu = SideMenu(self.web_driver_container)

        login_page.login_to_web_admin(self.login, self.password)
        side_menu.open_users_page()
        users_page.set_user_id(self.user_id)
        time.sleep(1)
        if not users_page.is_searched_user_found(self.user_id):
            users_page.click_on_new_button()
            values_tab.set_user_id(self.user_id)
            values_tab.set_ext_id_client(self.ext_id_client)
            details_tab.set_mail(self.email)
            wizard.click_on_save_changes()
            time.sleep(1)
            users_page.set_user_id(self.user_id)

    def test_context(self):
        users_page = UsersPage(self.web_driver_container)
        client_tab = UsersClientSubWizard(self.web_driver_container)
        wizard = UsersWizard(self.web_driver_container)
        common_act = CommonPage(self.web_driver_container)

        try:
            self.precondition()

            users_page.click_on_more_actions()
            users_page.click_on_edit_at_more_actions()
            client_tab.click_on_plus_button()
            client_tab.set_client(self.client[0])
            client_tab.set_type(self.type)
            client_tab.click_on_checkmark_button()
            time.sleep(1)
            wizard.click_on_save_changes()
            i = 0
            while i < 10:
                if not users_page.is_main_page_open():
                    time.sleep(1)
                    i += 1
                else:
                    self.db_manager.my_db.execute(
                        "UPDATE QUODSETTINGS SET settingvalue = '10' WHERE settingkey = 'WEB_ADMIN_CACHE_THRESHOLD'")
                    common_act.refresh_page(True)
                    time.sleep(2)
                    break

            users_page.load_users_by_look_up_pattern(self.user_id)
            time.sleep(1)
            users_page.click_on_more_actions()
            users_page.click_on_edit_at_more_actions()
            time.sleep(1)
            self.verify("Saved Client displayed", True, self.client[0] in client_tab.get_all_clients_in_table())
            client_tab.click_on_plus_button()
            client_tab.set_client(self.client[1])
            client_tab.set_type(self.type)
            client_tab.click_on_checkmark_button()
            time.sleep(1)
            self.verify("Client added when THRESHOLD < than created clients",
                        True, self.client[1] in client_tab.get_all_clients_in_table())
            wizard.click_on_save_changes()
            users_page.load_users_by_look_up_pattern(self.user_id)
            time.sleep(1)
            users_page.click_on_more_actions()
            users_page.click_on_edit_at_more_actions()
            time.sleep(1)
            self.verify("Saved Client displayed",
                        True, sorted(self.client) == sorted(client_tab.get_all_clients_in_table()))

        except Exception:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            errors = f'"{[traceback.extract_tb(exc_traceback, limit=4)]}"'.replace("\\", "/")
            basic_custom_actions.create_event(f"FAILED", self.test_case_id, status='FAILED',
                                              body="[{\"type\": \"message\", \"data\":" + f"{errors}" + "}]")
            traceback.print_tb(exc_traceback, limit=3, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)

        finally:
            self.db_manager.my_db.execute(
                "UPDATE QUODSETTINGS SET settingvalue = '500' WHERE settingkey = 'WEB_ADMIN_CACHE_THRESHOLD'")
            self.db_manager.my_db.execute(
                f"UPDATE USERROLESACCOUNTGROUP SET ALIVE = 'N' WHERE USERID = '{self.user_id}'")
