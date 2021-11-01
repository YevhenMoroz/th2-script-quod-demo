import random
import time
import traceback

from custom import basic_custom_actions
from quod_qa.web_admin.web_admin_core.pages.login.login_page import LoginPage
from quod_qa.web_admin.web_admin_core.pages.reference_data.instr_symbol_info.instr_symbol_info_page import \
    InstrSymbolInfoPage
from quod_qa.web_admin.web_admin_core.pages.reference_data.instr_symbol_info.instr_symbol_info_wizard import \
    InstrSymbolInfoWizard
from quod_qa.web_admin.web_admin_core.pages.root.side_menu import SideMenu
from quod_qa.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer
from quod_qa.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_2302(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id)
        self.login = "adm02"
        self.password = "adm02"
        self.instr_symbol = 'AUD/DKK'
        self.cum_trading_limit_percentage = str(random.randint(0, 100))
        self.md_max_spread = str(random.randint(0, 100))

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

    def test_context(self):

        try:
            self.precondition()
            page = InstrSymbolInfoPage(self.web_driver_container)
            wizard = InstrSymbolInfoWizard(self.web_driver_container)
            page.set_instr_symbol(self.instr_symbol)
            time.sleep(3)
            page.click_on_more_actions()
            time.sleep(2)
            page.click_on_edit()
            time.sleep(2)
            wizard.set_md_max_spread(self.md_max_spread)
            wizard.click_on_save_changes()
            time.sleep(2)
            page.set_instr_symbol(self.instr_symbol)
            time.sleep(3)
            expected_values = [self.instr_symbol, self.md_max_spread]
            actual_values = [page.get_instr_symbol(), page.get_md_max_spread()]
            self.verify("Is entity edited and saved correctly", expected_values, actual_values)
        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            print(traceback.format_exc() + " Search in ->  " + self.__class__.__name__)
