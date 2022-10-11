import time
import traceback
import random
import string

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.client_accounts.clients.clients_page import ClientsPage
from test_framework.web_admin_core.pages.client_accounts.clients.clients_wizard import ClientsWizard
from test_framework.web_admin_core.pages.client_accounts.clients.clients_values_sub_wizard import \
    ClientsValuesSubWizard
from test_framework.web_admin_core.pages.client_accounts.clients.clients_external_allocation_matching_service_sub_wizard\
    import ClientsExternalAllocationMatchingService
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T8215(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.allocation_matching_service = "External"
        self.client_name = ''
        self.name_at_manage = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.gateway_instance_at_manage = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        time.sleep(2)
        side_menu.open_clients_page()

    def post_condition(self):
        values_sub_wizard = ClientsValuesSubWizard(self.web_driver_container)
        values_sub_wizard.click_on_manage_external_allocation_matching_service()
        manage_sub_wizard = ClientsExternalAllocationMatchingService(self.web_driver_container)
        manage_sub_wizard.set_name_filter(self.name_at_manage)
        time.sleep(1)
        manage_sub_wizard.click_on_delete_button(True)

    def test_context(self):
        try:
            self.precondition()

            main_page = ClientsPage(self.web_driver_container)
            main_page.click_on_more_actions()
            main_page.click_on_edit()

            values_sub_wizard = ClientsValuesSubWizard(self.web_driver_container)
            self.client_name = values_sub_wizard.get_name()

            values_sub_wizard.click_on_manage_external_allocation_matching_service()
            manage_sub_wizard = ClientsExternalAllocationMatchingService(self.web_driver_container)
            manage_sub_wizard.click_on_plus_button()
            manage_sub_wizard.set_name(self.name_at_manage)
            manage_sub_wizard.set_gateway_instance(self.gateway_instance_at_manage)
            manage_sub_wizard.click_on_unsolicited_checkmark()
            manage_sub_wizard.click_on_save_checkmark()

            wizard = ClientsWizard(self.web_driver_container)
            wizard.click_on_go_back()
            values_sub_wizard.set_allocation_matching_service(self.allocation_matching_service)
            time.sleep(1)
            self.verify("Allocation Matching Service field is enable", True,
                        values_sub_wizard.is_external_allocation_matching_service_field_enable())
            values_sub_wizard.set_external_allocation_matching_service(self.name_at_manage)
            wizard.click_on_save_changes()
            time.sleep(1)
            main_page.set_name(self.client_name)
            time.sleep(1)
            main_page.click_on_more_actions()
            main_page.click_on_edit()
            time.sleep(1)
            self.verify("External allocation matching service saved", self.name_at_manage,
                        values_sub_wizard.get_external_allocation_matching_service())

            self.post_condition()

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            print(traceback.format_exc() + " Search in ->  " + self.__class__.__name__)
