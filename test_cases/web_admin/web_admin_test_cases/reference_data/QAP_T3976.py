import random
import sys
import time
import traceback

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.reference_data.instr_symbol_info.instr_symbol_info_page import \
    InstrSymbolInfoPage
from test_framework.web_admin_core.pages.reference_data.instr_symbol_info.instr_symbol_info_wizard import \
    InstrSymbolInfoWizard
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T3976(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.instr_symbol = self.data_set.get_instr_symbol("instr_symbol_1")
        self.cum_trading_limit_percentage = str(random.randint(0, 100))
        self.cum_trading_limit_percentage_new = str(random.randint(0, 100))

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        time.sleep(2)
        side_menu.open_instr_symbol_info_page()
        time.sleep(2)
        page = InstrSymbolInfoPage(self.web_driver_container)
        wizard = InstrSymbolInfoWizard(self.web_driver_container)
        page.click_on_new()
        time.sleep(2)
        wizard.set_instr_symbol(self.instr_symbol)
        wizard.set_cum_trading_limit_percentage(self.cum_trading_limit_percentage)
        wizard.click_on_save_changes()
        time.sleep(2)

        if wizard.is_error_message_displayed():
            all_instr_symbol = wizard.get_all_instr_symbols_from_drop_menu()
            while wizard.is_error_message_displayed():
                wizard.click_on_error_message_pop_up()
                self.instr_symbol = random.choice(all_instr_symbol)
                wizard.set_instr_symbol(self.instr_symbol)
                all_instr_symbol.remove(self.instr_symbol)
                time.sleep(1)
                wizard.click_on_save_changes()
                time.sleep(2)

    def test_context(self):
        try:
            self.precondition()
            page = InstrSymbolInfoPage(self.web_driver_container)
            try:
                page.set_instr_symbol(self.instr_symbol)
                time.sleep(3)
                page.click_on_more_actions()
                time.sleep(2)
                page.click_on_delete(True)
                self.verify("Delete button working", True, True)
            except Exception as e:
                self.verify("Delete button does not works", True, e.__class__.__name__)

            try:
                time.sleep(2)
                page.set_instr_symbol(self.instr_symbol)

                time.sleep(2)
                self.verify("Entity is not displayed after delete", False, page.is_instr_symbol_present())
            except Exception as e:
                self.verify("Entity stayed after delete", True, e.__class__.__name__)

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
