import sys
import traceback

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.clients_accounts.clients.clients_page import ClientsPage
from test_framework.web_admin_core.pages.clients_accounts.clients.clients_values_sub_wizard import \
    ClientsValuesSubWizard
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T3882(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")

        self.clearing_account_type = 'Institutional'
        self.option = 'Manual'

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        side_menu.open_clients_page()
        main_page = ClientsPage(self.web_driver_container)
        main_page.click_on_new()

    def test_context(self):

        try:
            self.precondition()

            values_sub_wizard = ClientsValuesSubWizard(self.web_driver_container)
            values_sub_wizard.set_clearing_account_type(self.clearing_account_type)
            values_sub_wizard.set_booking_inst(self.option)
            values_sub_wizard.set_allocation_preference(self.option)
            values_sub_wizard.set_confirmation_service(self.option)
            values_sub_wizard.set_block_approval(self.option)

            selected_values = [values_sub_wizard.get_clearing_account_type(), values_sub_wizard.get_booking_inst(),
                               values_sub_wizard.get_allocation_preference(), values_sub_wizard.get_confirmation_service(),
                               values_sub_wizard.get_block_approval()]
            actual_result = True
            for i in selected_values:
                if i == self.clearing_account_type or i == self.option:
                    pass
                else:
                    actual_result = False
                    break

            self.verify("The required options have been selected", True, actual_result)

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
