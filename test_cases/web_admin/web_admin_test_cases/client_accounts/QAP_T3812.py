import sys
import time
import traceback
import random
import string

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.clients_accounts.accounts.accounts_page import AccountsPage
from test_framework.web_admin_core.pages.clients_accounts.accounts.accounts_wizard import AccountsWizard
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T3812(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")

        self.id = "QAP3783"
        self.ext_id_client = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.client_id_source = self.data_set.get_client_id_source("client_id_source_1")
        self.bo_fields = dict(zip([str(_) for _ in range(1, 6)],
                              [''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
                               for _ in range(6)]))

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        time.sleep(2)
        side_menu = SideMenu(self.web_driver_container)
        side_menu.open_accounts_page()
        time.sleep(2)
        account_page = AccountsPage(self.web_driver_container)
        account_page.set_id(self.id)
        time.sleep(1)
        if not account_page.is_searched_account_found(self.id):
            account_page.click_new_button()
            time.sleep(2)
            wizard = AccountsWizard(self.web_driver_container)
            wizard.set_id(self.id)
            wizard.set_ext_id_client(self.id)
            wizard.set_client_id_source(self.client_id_source)
            wizard.set_bo_field_1(self.bo_fields['1'])
            wizard.set_bo_field_2(self.bo_fields['2'])
            wizard.set_bo_field_3(self.bo_fields['3'])
            wizard.set_bo_field_4(self.bo_fields['4'])
            wizard.set_bo_field_5(self.bo_fields['5'])
            wizard.click_save_button()
            time.sleep(2)
            account_page.set_id(self.id)
            time.sleep(1)

    def test_context(self):

        try:
            self.precondition()

            account_page = AccountsPage(self.web_driver_container)
            account_page.click_more_actions_button()
            time.sleep(1)
            account_page.click_edit_entity_button()
            time.sleep(2)
            wizard = AccountsWizard(self.web_driver_container)
            wizard.set_bo_field_1(self.bo_fields['1'])
            wizard.set_bo_field_2(self.bo_fields['2'])
            wizard.set_bo_field_3(self.bo_fields['3'])
            wizard.set_bo_field_4(self.bo_fields['4'])
            wizard.set_bo_field_5(self.bo_fields['5'])
            wizard.click_save_button()
            time.sleep(2)
            account_page.set_id(self.id)
            time.sleep(1)
            account_page.click_more_actions_button()
            time.sleep(1)
            account_page.click_edit_entity_button()
            time.sleep(2)

            excepted_result = [self.bo_fields['1'], self.bo_fields['2'], self.bo_fields['3'], self.bo_fields['4'],
                               self.bo_fields['5']]
            actual_result = [wizard.get_bo_field_1(), wizard.get_bo_field_2(), wizard.get_bo_field_3(),
                             wizard.get_bo_field_4(), wizard.get_bo_field_5()]

            self.verify("New data for the BO fields saved correct", excepted_result, actual_result)

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
