import random
import string
import sys
import time
import traceback

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.clients_accounts.accounts.accounts_page import AccountsPage
from test_framework.web_admin_core.pages.clients_accounts.accounts.accounts_wizard import \
    AccountsWizard
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T3518(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None,
                 db_manager=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.db_manager = db_manager

        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.account_id = self.__class__.__name__

        self.id = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.client_id_source = self.data_set.get_client_id_source("client_id_source_1")
        self.ext_id_client = [''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6)) for _ in range(2)]

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        side_menu = SideMenu(self.web_driver_container)
        main_page = AccountsPage(self.web_driver_container)
        values_sub_wizard = AccountsWizard(self.web_driver_container)
        wizard = AccountsWizard(self.web_driver_container)

        login_page.login_to_web_admin(self.login, self.password)
        side_menu.open_accounts_page()

        self.db_manager.my_db.execute("SELECT ACCOUNTID FROM SECURITYACCOUNT WHERE DUMMY = 'Y'")
        dummy_account = [_[0] for _ in self.db_manager.my_db]
        if len(dummy_account) == 0:
            main_page.click_new_button()
            values_sub_wizard.set_id(self.account_id)
            values_sub_wizard.set_ext_id_client(self.ext_id_client[0])
            values_sub_wizard.set_client_id_source(self.client_id_source)
            values_sub_wizard.click_on_dummy_checkbox()
            wizard.click_save_button()

    def test_context(self):
        values_sub_wizard = AccountsWizard(self.web_driver_container)
        main_page = AccountsPage(self.web_driver_container)
        wizard = AccountsWizard(self.web_driver_container)

        try:
            self.precondition()

            main_page.click_new_button()
            values_sub_wizard.set_id(self.id)
            values_sub_wizard.set_ext_id_client(self.ext_id_client[1])
            values_sub_wizard.set_client_id_source(self.client_id_source)
            values_sub_wizard.click_on_dummy_checkbox()
            wizard.click_save_button()
            time.sleep(2)

            self.verify("Second DUMMY account is not saving", True, wizard.is_request_failed_message_displayed())

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
