import time
import random
import string

from test_framework.web_admin_core.pages.clients_accounts.clients.clients_values_sub_wizard import \
    ClientsValuesSubWizard
from test_framework.web_admin_core.pages.clients_accounts.clients.clients_assignments_sub_wizard \
    import ClientsAssignmentsSubWizard
from test_framework.web_admin_core.pages.clients_accounts.clients.clients_page import ClientsPage
from test_framework.web_admin_core.pages.clients_accounts.clients.clients_wizard import ClientsWizard
from test_framework.web_admin_core.pages.clients_accounts.accounts.accounts_page import AccountsPage
from test_framework.web_admin_core.pages.clients_accounts.accounts.accounts_wizard import AccountsWizard
from test_framework.web_admin_core.pages.positions.cash_positions.main_page import MainPage as CashPositionsPage
from test_framework.web_admin_core.pages.positions.cash_positions.wizards import MainWizard as CashPositionsWizard
from test_framework.web_admin_core.pages.positions.cash_positions.wizards import ValuesTab as CashPositionsValuesTab

from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T10723(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None,
                 db_manager=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)

        self.db_manager = db_manager
        self.user = {"adm":
                          {"login": self.data_set.get_user("user_1"),
                           "password": self.data_set.get_password("password_1")}}

        self.client_name = f"Client {self.__class__.__name__}"
        self.account_id = f"Account {self.__class__.__name__}"
        self.client_id = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.ext_id_client = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.disclose_exec = 'Manual'
        self.desk = self.data_set.get_desk("desk_3")
        self.clearing_account_type = 'Firm'
        self.client_id_source = 'BIC'

        self.cash_position_name = self.__class__.__name__
        self.client_cash_account_id = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.venue_cash_account_id = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.currency = 'ALL'
        self.warn_message = 'Margin is being utilised and hence margin account can not be deselected.'

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        side_menu = SideMenu(self.web_driver_container)
        client_page = ClientsPage(self.web_driver_container)
        account_page = AccountsPage(self.web_driver_container)
        cash_positions_page = CashPositionsPage(self.web_driver_container)
        cash_position_values_tab = CashPositionsValuesTab(self.web_driver_container)
        cash_position_wizard = CashPositionsWizard(self.web_driver_container)

        login_page.login_to_web_admin(self.user["adm"]["login"], self.user["adm"]["password"])
        side_menu.open_clients_page()
        client_page.set_name(self.client_name)
        time.sleep(1)
        if not client_page.is_searched_client_found(self.client_name):
            client_page.click_on_new()
            values_tab = ClientsValuesSubWizard(self.web_driver_container)
            values_tab.set_id(self.client_id)
            values_tab.set_name(self.client_name)
            values_tab.set_ext_id_client(self.ext_id_client)
            values_tab.set_disclose_exec(self.disclose_exec)
            assignments_tab = ClientsAssignmentsSubWizard(self.web_driver_container)
            assignments_tab.set_desk(self.desk)
            wizard = ClientsWizard(self.web_driver_container)
            wizard.click_on_save_changes()
            time.sleep(1)

        side_menu.open_accounts_page()
        account_page.set_id(self.account_id)
        time.sleep(1)
        if not account_page.is_searched_account_found(self.account_id):
            account_page.click_new_button()
            values_tab = AccountsWizard(self.web_driver_container)
            values_tab.set_id(self.account_id)
            values_tab.set_ext_id_client(self.ext_id_client)
            values_tab.set_client_id_source(self.client_id_source)
            values_tab.set_client(self.client_name)
            wizard = AccountsWizard(self.web_driver_container)
            wizard.click_save_button()
            time.sleep(1)

        side_menu.open_cash_positions_page()
        cash_positions_page.set_name(self.cash_position_name)
        time.sleep(2)
        if not cash_positions_page.is_searched_cash_account_found(self.cash_position_name):
            cash_positions_page.click_on_new()
            cash_position_values_tab.set_name(self.cash_position_name)
            cash_position_values_tab.set_client_cash_account_id(self.client_cash_account_id)
            cash_position_values_tab.set_venue_cash_account_id(self.venue_cash_account_id)
            cash_position_values_tab.set_currency(self.currency)
            cash_position_values_tab.set_client(self.client_name)
            time.sleep(1)
            cash_position_values_tab.set_security_accounts(self.account_id)
            time.sleep(1)
            cash_position_values_tab.select_margin_account_checkbox()
            time.sleep(1)
            cash_position_wizard.click_on_save_changes()

        self.db_manager.my_db.execute(
            f"UPDATE cashaccount SET cashloaned = '100' WHERE cashaccountname = '{self.cash_position_name}'")

    def test_context(self):
        cash_positions_page = CashPositionsPage(self.web_driver_container)
        cash_position_wizard = CashPositionsWizard(self.web_driver_container)
        cash_position_values_tab = CashPositionsValuesTab(self.web_driver_container)

        self.precondition()

        cash_positions_page.set_name(self.cash_position_name)
        time.sleep(1)
        cash_positions_page.click_on_more_actions()
        cash_positions_page.click_on_edit()
        time.sleep(1)

        expected_result = ['Checkbox selected = True', 'Checkbox enabled = False',
                           'WARN displayed = True', self.warn_message]
        actual_result = [f'Checkbox selected = {cash_position_values_tab.is_margin_account_checkbox_selected()}',
                         f'Checkbox enabled = {cash_position_values_tab.is_margin_account_checkbox_enabled()}',
                         f'WARN displayed = {cash_position_values_tab.is_warning_message_displayed()}',
                         cash_position_values_tab.get_warning_message()]
        self.verify("Margin Accounts disabled and selected, WARN message displayed", expected_result, actual_result)
        cash_position_wizard.click_on_close()
        time.sleep(1)
        if cash_position_wizard.is_confirmation_of_leave_wizard_displayed():
            cash_position_wizard.click_on_ok_button()

        self.db_manager.my_db.execute(
            f"UPDATE cashaccount SET bookedcashloan = '20' WHERE cashaccountname = '{self.cash_position_name}'")

        cash_positions_page.set_name(self.cash_position_name)
        time.sleep(1)
        cash_positions_page.click_on_more_actions()
        cash_positions_page.click_on_edit()
        time.sleep(1)
        cash_position_values_tab.select_margin_account_checkbox()
        time.sleep(1)

        expected_result = ['Checkbox selected = True', 'Checkbox enabled = False',
                           'WARN displayed = True', self.warn_message]
        actual_result = [f'Checkbox selected = {cash_position_values_tab.is_margin_account_checkbox_selected()}',
                         f'Checkbox enabled = {cash_position_values_tab.is_margin_account_checkbox_enabled()}',
                         f'WARN displayed = {cash_position_values_tab.is_warning_message_displayed()}',
                         cash_position_values_tab.get_warning_message()]
        self.verify("Margin Accounts disabled and selected, WARN message displayed", expected_result, actual_result)
