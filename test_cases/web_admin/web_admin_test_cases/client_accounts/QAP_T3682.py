import random
import string
import time

from test_framework.web_admin_core.pages.clients_accounts.clients.clients_assignments_sub_wizard import \
    ClientsAssignmentsSubWizard
from test_framework.web_admin_core.pages.clients_accounts.clients.clients_page import ClientsPage
from test_framework.web_admin_core.pages.clients_accounts.clients.clients_trade_confirm_sub_wizard import \
    ClientsTradeConfirmSubWizard
from test_framework.web_admin_core.pages.clients_accounts.clients.clients_values_sub_wizard import \
    ClientsValuesSubWizard
from test_framework.web_admin_core.pages.clients_accounts.clients.clients_wizard import ClientsWizard
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T3682(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.id = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.ext_id_client = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.disclose_exec = self.data_set.get_disclose_exec("disclose_exec_1")
        self.email_address = self.data_set.get_email("email_1")
        self.trade_confirm_generation = self.data_set.get_trade_confirm_generation("trade_confirm_generation_1")
        self.trade_confirm_preference = self.data_set.get_trade_confirm_preference("trade_confirm_preference_1")
        self.net_gross_ind_type = self.data_set.get_net_gross_ind_type("net_gross_ind_type_1")
        self.recipient_types = self.data_set.get_recipient_type("recipient_type_1")
        self.desk = self.data_set.get_desk("desk_3")

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        time.sleep(2)
        side_menu.open_clients_page()
        main_page = ClientsPage(self.web_driver_container)
        values_sub_wizard = ClientsValuesSubWizard(self.web_driver_container)
        wizard = ClientsWizard(self.web_driver_container)
        time.sleep(2)
        main_page.click_on_new()
        time.sleep(2)
        values_sub_wizard.set_id(self.id)
        values_sub_wizard.set_name(self.name)
        values_sub_wizard.set_disclose_exec(self.disclose_exec)
        values_sub_wizard.set_ext_id_client(self.ext_id_client)
        time.sleep(1)
        assignments_sub_wizard = ClientsAssignmentsSubWizard(self.web_driver_container)
        assignments_sub_wizard.set_desk(self.desk)
        time.sleep(1)
        wizard.click_on_save_changes()
        time.sleep(2)
        main_page.set_name(self.name)
        time.sleep(2)
        main_page.click_on_more_actions()
        time.sleep(2)
        main_page.click_on_edit()
        time.sleep(2)
        trade_confirm_sub_wizard = ClientsTradeConfirmSubWizard(self.web_driver_container)
        trade_confirm_sub_wizard.set_trade_confirm_generation(self.trade_confirm_generation)
        trade_confirm_sub_wizard.set_trade_confirm_preference(self.trade_confirm_preference)
        trade_confirm_sub_wizard.set_net_gross_ind_type(self.net_gross_ind_type)
        trade_confirm_sub_wizard.click_on_plus()
        time.sleep(1)
        trade_confirm_sub_wizard.set_email_address(self.email_address)
        trade_confirm_sub_wizard.set_recipient_types(self.recipient_types)
        trade_confirm_sub_wizard.click_on_checkmark()
        time.sleep(1)
        wizard.click_on_save_changes()
        time.sleep(2)
        main_page.set_name(self.name)
        time.sleep(2)
        main_page.click_on_more_actions()
        main_page.click_on_edit()
        time.sleep(2)

    def test_context(self):
        trade_confirm_sub_wizard = ClientsTradeConfirmSubWizard(self.web_driver_container)

        self.precondition()
        actual_result = [trade_confirm_sub_wizard.get_trade_confirm_generation(),
                         trade_confirm_sub_wizard.get_trade_confirm_preference(),
                         trade_confirm_sub_wizard.get_net_gross_ind_type()]
        trade_confirm_sub_wizard.click_on_edit()
        time.sleep(1)
        actual_result.append(trade_confirm_sub_wizard.get_email_address())
        actual_result.append(trade_confirm_sub_wizard.get_recipient_types())
        expected_result = [self.trade_confirm_generation, self.trade_confirm_preference, self.net_gross_ind_type,
                           self.email_address, self.recipient_types]

        self.verify("Edit entity saved correctly", expected_result, actual_result)
