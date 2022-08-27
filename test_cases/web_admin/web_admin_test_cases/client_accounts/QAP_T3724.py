import time
import traceback
import random
import string

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.client_accounts.accounts.accounts_page import AccountsPage
from test_framework.web_admin_core.pages.general.common.common_page import CommonPage
from test_framework.web_admin_core.pages.client_accounts.accounts.accounts_wizard import AccountsWizard
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T3724(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = "adm03"
        self.password = "adm03"
        self.client = "BrokerACA"
        self.client_id_source = "BIC"
        self.ext_id_client = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.id = 'ACABankFirm'

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        time.sleep(2)
        side_menu = SideMenu(self.web_driver_container)
        side_menu.open_accounts_page()

    def test_context(self):
        try:
            self.precondition()

            main_page = AccountsPage(self.web_driver_container)
            main_page.click_new_button()
            values_sub_wizard = AccountsWizard(self.web_driver_container)
            values_sub_wizard.set_client(self.client)
            values_sub_wizard.set_client_id_source(self.client_id_source)

            wizard = AccountsWizard(self.web_driver_container)
            wizard.click_save_button()
            time.sleep(1)
            self.verify("Is incorrect or missing value message displayed", True,
                        wizard.is_incorrect_or_missing_value_message_displayed())
            values_sub_wizard.set_id(self.id)
            values_sub_wizard.set_ext_id_client(self.ext_id_client)
            wizard.click_save_button()
            time.sleep(1)
            common_act = CommonPage(self.web_driver_container)
            self.verify("Such record already exists displayed", True, common_act.is_error_message_displayed())

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            print(traceback.format_exc() + " Search in ->  " + self.__class__.__name__)
