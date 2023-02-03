import sys
import time
import traceback
import random
import string

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.clients_accounts.clients.clients_values_sub_wizard import \
    ClientsValuesSubWizard
from test_framework.web_admin_core.pages.clients_accounts.clients.clients_page import ClientsPage
from test_framework.web_admin_core.pages.clients_accounts.clients.clients_wizard import ClientsWizard
from test_framework.web_admin_core.pages.clients_accounts.clients.clients_external_give_up_service_sub_wizard \
    import ClientsExternalGiveUpService
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T9090(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.id = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.ext_id_client = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.disclose_exec = 'Manual'
        self.give_up_service = ['External', 'Manual']
        self.give_up_matching_id = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.external_give_up_service_name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.gateway_instance = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        side_menu.open_clients_page()

        page = ClientsPage(self.web_driver_container)
        page.click_on_new()
        values_tab = ClientsValuesSubWizard(self.web_driver_container)
        values_tab.set_id(self.id)
        values_tab.set_name(self.name)
        values_tab.set_ext_id_client(self.ext_id_client)
        values_tab.set_disclose_exec(self.disclose_exec)
        wizard = ClientsWizard(self.web_driver_container)
        wizard.click_on_save_changes()

    def test_context(self):
        try:
            self.precondition()

            page = ClientsPage(self.web_driver_container)
            page.set_name(self.name)
            time.sleep(1)
            page.click_on_more_actions()
            page.click_on_edit()
            values_tab = ClientsValuesSubWizard(self.web_driver_container)
            actual_result = values_tab.get_all_give_up_service_from_drop_menu()
            expected_result = self.give_up_service
            self.verify(f"Give-Up Service fields contains: {self.give_up_service}", expected_result, actual_result)
            values_tab.set_give_up_service(self.give_up_service[0])

            self.verify("GiveUp Matching ID field  has value from Ext ID Client",
                        values_tab.get_give_up_matching_id(), values_tab.get_ext_id_client())

            values_tab.set_give_up_mathing_id(self.give_up_matching_id)
            values_tab.click_on_manage_external_give_up_service()
            manage_wizard = ClientsExternalGiveUpService(self.web_driver_container)
            manage_wizard.click_on_plus_button()
            manage_wizard.set_name(self.external_give_up_service_name)
            manage_wizard.set_gateway_instance(self.gateway_instance)
            manage_wizard.click_on_save_checkmark()
            wizard = ClientsWizard(self.web_driver_container)
            wizard.click_on_go_back()
            values_tab.set_external_give_up_service(self.external_give_up_service_name)
            wizard.click_on_save_changes()
            page.set_name(self.name)
            time.sleep(1)
            page.click_on_more_actions()
            page.click_on_edit()

            actual_result = [values_tab.get_give_up_service(), values_tab.get_external_give_up_service(),
                             values_tab.get_give_up_matching_id()]
            expected_result = [self.give_up_service[0], self.external_give_up_service_name, self.give_up_matching_id]

            self.verify("Client saved with new data", expected_result, actual_result)

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
