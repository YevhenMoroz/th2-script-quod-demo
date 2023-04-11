import random
import string
import sys
import time
import traceback

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.clients_accounts.clients.clients_page import ClientsPage
from test_framework.web_admin_core.pages.clients_accounts.clients.clients_wizard import ClientsWizard
from test_framework.web_admin_core.pages.clients_accounts.clients.clients_values_sub_wizard import ClientsValuesSubWizard
from test_framework.web_admin_core.pages.clients_accounts.clients.clients_assignments_sub_wizard \
    import ClientsAssignmentsSubWizard

from test_framework.web_admin_core.pages.positions.cash_positions.main_page import *
from test_framework.web_admin_core.pages.positions.cash_positions.wizards import *

from test_framework.web_admin_core.pages.general.common.common_page import CommonPage
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T7796(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")

        self.test_data = {
            "adm_user": {
                "login": "adm03",
                "password": "adm03"
            },
            "desk_user": {
                "login": self.data_set.get_user("user_3"),
                "password": self.data_set.get_password("password_3")
            },
            "client": {
                "id": 'QAP-T7796',
                "name": 'QAP-T7796',
                "disclose_exec": 'Manual',
                "ext_id_client": ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6)),
                "desk": self.data_set.get_desk("desk_1"),
            },
            "cash_position_1": {
                "name": "QAP-T7796-1",
                "client_cash_account_id": ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6)),
                "venue_cash_account_id": ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6)),
                "currency": 'BMD',
                "client": 'QAP-T7796'
            },
            "cash_position_2": {
                "name": "QAP-T7796-2",
                "client_cash_account_id": ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6)),
                "venue_cash_account_id": ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6)),
                "currency": 'BMD',
                "client": 'QAP-T7796'
            }
        }

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        side_menu = SideMenu(self.web_driver_container)
        client_page = ClientsPage(self.web_driver_container)
        client_values_tab = ClientsValuesSubWizard(self.web_driver_container)
        client_assignments_tab = ClientsAssignmentsSubWizard(self.web_driver_container)
        cash_positions_page = MainPage(self.web_driver_container)
        cash_positions_values_tab = ValuesTab(self.web_driver_container)
        cash_positions_wizard = MainWizard(self.web_driver_container)

        login_page.login_to_web_admin(self.login, self.password)
        side_menu.open_clients_page()
        client_page.set_name(self.test_data['client']['name'])
        time.sleep(1)
        if not client_page.is_searched_client_found(self.test_data['client']['name']):
            client_page.click_on_new()
            client_values_tab.set_id(self.test_data['client']['id'])
            client_values_tab.set_name(self.test_data['client']['name'])
            client_values_tab.set_ext_id_client(self.test_data['client']['ext_id_client'])
            client_values_tab.set_disclose_exec(self.test_data['client']['disclose_exec'])
            client_assignments_tab.set_desk(self.test_data['client']['desk'])
            client_wizard = ClientsWizard(self.web_driver_container)
            client_wizard.click_on_save_changes()
            time.sleep(2)

        side_menu.open_cash_positions_page()
        cash_positions_page.set_name(self.test_data['cash_position_1']['name'])
        time.sleep(1)
        if not cash_positions_page.is_searched_cash_account_found(self.test_data['cash_position_1']['name']):
            cash_positions_page.click_on_new()
            cash_positions_values_tab.set_name(self.test_data['cash_position_1']['name'])
            cash_positions_values_tab.set_client_cash_account_id(self.test_data['cash_position_1']['client_cash_account_id'])
            cash_positions_values_tab.set_venue_cash_account_id(self.test_data['cash_position_1']['venue_cash_account_id'])
            cash_positions_values_tab.set_currency(self.test_data['cash_position_1']['currency'])
            cash_positions_values_tab.set_client(self.test_data['cash_position_1']['client'])
            cash_positions_wizard.click_on_save_changes()
            cash_positions_page.set_name(self.test_data['cash_position_1']['name'])
            time.sleep(1)
            cash_positions_page.click_on_more_actions()
            cash_positions_page.click_on_edit()
            cash_positions_values_tab.select_default_cash_position_checkbox()
            cash_positions_wizard.click_on_save_changes()

        cash_positions_page.set_name(self.test_data['cash_position_2']['name'])
        time.sleep(1)
        if not cash_positions_page.is_searched_cash_account_found(self.test_data['cash_position_2']['name']):
            cash_positions_page.click_on_new()
            cash_positions_values_tab.set_name(self.test_data['cash_position_2']['name'])
            cash_positions_values_tab.set_client_cash_account_id(self.test_data['cash_position_2']['client_cash_account_id'])
            cash_positions_values_tab.set_venue_cash_account_id(self.test_data['cash_position_2']['venue_cash_account_id'])
            cash_positions_values_tab.set_currency(self.test_data['cash_position_2']['currency'])
            cash_positions_values_tab.set_client(self.test_data['cash_position_2']['client'])
            cash_positions_wizard.click_on_save_changes()

    def test_context(self):
        cash_positions_page = MainPage(self.web_driver_container)
        cash_positions_values_tab = ValuesTab(self.web_driver_container)
        cash_positions_wizard = MainWizard(self.web_driver_container)

        try:
            self.precondition()

            cash_positions_page.set_name(self.test_data['cash_position_2']['name'])
            time.sleep(1)
            cash_positions_page.click_on_more_actions()
            cash_positions_page.click_on_edit()
            cash_positions_values_tab.select_default_cash_position_checkbox()
            cash_positions_wizard.click_on_save_changes()
            time.sleep(1)

            common_act = CommonPage(self.web_driver_container)

            self.verify("Get an reject with error message - A default cash account for this currency on this client "
                        "is already assigned", True, common_act.is_error_message_displayed())

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
