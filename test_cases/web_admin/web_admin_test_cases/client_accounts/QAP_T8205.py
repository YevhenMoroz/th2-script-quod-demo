import time
import traceback

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.client_accounts.clients.clients_page import ClientsPage
from test_framework.web_admin_core.pages.client_accounts.clients.clients_values_sub_wizard import \
    ClientsValuesSubWizard
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T8205(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.allocation_matching_service = ["External", "Internal", "Manual"]

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        time.sleep(2)
        side_menu.open_clients_page()

    def test_context(self):
        try:
            self.precondition()

            main_page = ClientsPage(self.web_driver_container)
            main_page.click_on_more_actions()
            main_page.click_on_edit()

            values_sub_wizard = ClientsValuesSubWizard(self.web_driver_container)
            values_sub_wizard.clear_allocation_matching_service_field()
            time.sleep(1)
            self.verify("Allocation Matching Service field is disable", False,
                        values_sub_wizard.is_external_allocation_matching_service_field_enable())

            values_sub_wizard.set_allocation_matching_service(self.allocation_matching_service[0])
            time.sleep(1)
            self.verify("Allocation Matching Service field is enable", True,
                        values_sub_wizard.is_external_allocation_matching_service_field_enable())

            values_sub_wizard.set_allocation_matching_service(self.allocation_matching_service[1])
            time.sleep(1)
            self.verify("Allocation Matching Service field is disable", False,
                        values_sub_wizard.is_external_allocation_matching_service_field_enable())

            values_sub_wizard.set_allocation_matching_service(self.allocation_matching_service[2])
            time.sleep(1)
            self.verify("Allocation Matching Service field is disable", False,
                        values_sub_wizard.is_external_allocation_matching_service_field_enable())

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            print(traceback.format_exc() + " Search in ->  " + self.__class__.__name__)
