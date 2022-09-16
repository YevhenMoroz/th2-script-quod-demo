import sys
import time
import traceback
import random
import string

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.client_accounts.clients.clients_page import ClientsPage
from test_framework.web_admin_core.pages.client_accounts.clients.clients_values_sub_wizard import ClientsValuesSubWizard
from test_framework.web_admin_core.pages.client_accounts.clients.clients_wizard import ClientsWizard
from test_framework.web_admin_core.pages.client_accounts.clients.clients_external_sources_sub_wizard \
    import ClientsExternalSourcesSubWizard
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T3813(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.client_name = ''
        self.client_bo_fields = [''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
                                 for _ in range(5)]

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        time.sleep(2)
        side_menu = SideMenu(self.web_driver_container)
        side_menu.open_clients_page()

    def test_context(self):

        try:
            self.precondition()

            client_page = ClientsPage(self.web_driver_container)
            client_page.click_on_more_actions()
            client_page.click_on_edit()

            values_tab = ClientsValuesSubWizard(self.web_driver_container)
            self.client_name = values_tab.get_name()

            external_source_tab = ClientsExternalSourcesSubWizard(self.web_driver_container)
            external_source_tab.set_bo_field_1(self.client_bo_fields[0])
            external_source_tab.set_bo_field_2(self.client_bo_fields[1])
            external_source_tab.set_bo_field_3(self.client_bo_fields[2])
            external_source_tab.set_bo_field_4(self.client_bo_fields[3])
            external_source_tab.set_bo_field_5(self.client_bo_fields[4])

            wizard = ClientsWizard(self.web_driver_container)
            wizard.click_on_save_changes()

            client_page.set_name(self.client_name)
            time.sleep(1)
            client_page.click_on_more_actions()
            client_page.click_on_edit()

            expected_result = self.client_bo_fields
            actual_result = [external_source_tab.get_bo_field_1(), external_source_tab.get_bo_field_2(),
                             external_source_tab.get_bo_field_3(), external_source_tab.get_bo_field_4(),
                             external_source_tab.get_bo_field_5()]

            self.verify("BO Fields saved correct", expected_result, actual_result)

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
