import random
import string
import time
import traceback

from custom import basic_custom_actions
from quod_qa.web_admin.web_admin_core.pages.client_accounts.clients.clients_page import ClientsPage
from quod_qa.web_admin.web_admin_core.pages.client_accounts.clients.clients_trade_confirm_sub_wizard import \
    ClientsTradeConfirmSubWizard
from quod_qa.web_admin.web_admin_core.pages.client_accounts.clients.clients_values_sub_wizard import \
    ClientsValuesSubWizard
from quod_qa.web_admin.web_admin_core.pages.client_accounts.clients.clients_wizard import ClientsWizard
from quod_qa.web_admin.web_admin_core.pages.login.login_page import LoginPage
from quod_qa.web_admin.web_admin_core.pages.root.side_menu import SideMenu
from quod_qa.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer
from quod_qa.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_4864(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id)
        self.login = "adm03"
        self.password = "adm03"
        self.id = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.disclose_exec = 'Manual'
        self.email_address = "email"
        self.trade_confirm_generation = "Automatic"
        self.trade_confirm_preference = "Excel"
        self.net_gross_ind_type = "Net"
        self.recipient_types = "CC"

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
        time.sleep(2)

    def test_context(self):
        try:
            self.precondition()
            main_page = ClientsPage(self.web_driver_container)
            expected_pdf_result = [self.disclose_exec,
                                   self.email_address,
                                   self.trade_confirm_generation,
                                   self.trade_confirm_preference,
                                   self.net_gross_ind_type,
                                   self.recipient_types]

            self.verify("Is pdf contains correctly values", True,
                        main_page.click_download_pdf_entity_button_and_check_pdf(expected_pdf_result))
        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            print(traceback.format_exc() + " Search in ->  " + self.__class__.__name__)
