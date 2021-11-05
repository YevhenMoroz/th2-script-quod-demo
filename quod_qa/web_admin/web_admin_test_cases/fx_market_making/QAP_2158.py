import random
import string
import time
import traceback

from custom import basic_custom_actions
from quod_qa.web_admin.web_admin_core.pages.fx_market_making.auto_hedger.auto_hedger_instruments_sub_wizard import \
    AutoHedgerInstrumentsSubWizard
from quod_qa.web_admin.web_admin_core.pages.fx_market_making.auto_hedger.auto_hedger_page import AutoHedgerPage
from quod_qa.web_admin.web_admin_core.pages.fx_market_making.auto_hedger.auto_hedger_values_sub_wizard import \
    AutoHedgerValuesSubWizard
from quod_qa.web_admin.web_admin_core.pages.fx_market_making.auto_hedger.auto_hedger_wizard import AutoHedgerWizard

from quod_qa.web_admin.web_admin_core.pages.login.login_page import LoginPage
from quod_qa.web_admin.web_admin_core.pages.root.side_menu import SideMenu
from quod_qa.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer
from quod_qa.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_2158(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id)
        self.login = "adm03"
        self.password = "adm03"
        self.name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.position_book = 'QUODAH'
        self.symbol = "AUD/CAD"
        self.hedging_strategy = 'PositionLimits'
        self.long_threshold_qty = '11'
        self.long_residual_qty = '12'
        self.short_threshold_qty = '5'
        self.short_residual_qty = '7'

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        time.sleep(2)
        side_menu.open_auto_hedger_page()
        main_page = AutoHedgerPage(self.web_driver_container)
        wizard = AutoHedgerWizard(self.web_driver_container)
        main_page.click_on_new()
        time.sleep(2)
        values_sub_wizard = AutoHedgerValuesSubWizard(self.web_driver_container)
        values_sub_wizard.set_name(self.name)
        time.sleep(2)
        values_sub_wizard.set_position_book(self.position_book)
        time.sleep(2)
        instruments_sub_wizard = AutoHedgerInstrumentsSubWizard(self.web_driver_container)
        instruments_sub_wizard.click_on_plus_button()
        time.sleep(2)
        instruments_sub_wizard.set_symbol(self.symbol)
        time.sleep(1)
        instruments_sub_wizard.set_hedging_strategy(self.hedging_strategy)
        time.sleep(1)
        instruments_sub_wizard.set_long_threshold_qty(self.long_threshold_qty)
        time.sleep(1)
        instruments_sub_wizard.set_long_residual_qty(self.long_residual_qty)
        time.sleep(1)
        instruments_sub_wizard.set_short_threshold_qty(self.short_threshold_qty)
        time.sleep(1)
        instruments_sub_wizard.set_short_residual_qty(self.short_residual_qty)
        time.sleep(1)
        instruments_sub_wizard.click_on_checkmark_button()
        time.sleep(2)
        wizard.click_on_save_changes()
        time.sleep(2)
        main_page.click_on_user_icon()
        time.sleep(2)
        main_page.click_on_logout()
        time.sleep(2)
        login_page.login_to_web_admin(self.login, self.password)
        time.sleep(2)
        side_menu.open_auto_hedger_page()
        time.sleep(2)
        main_page.set_name_filter(self.name)
        time.sleep(2)
        main_page.click_on_more_actions()
        time.sleep(2)
        main_page.click_on_edit()
        time.sleep(2)

    def test_context(self):

        try:

            self.precondition()
            values_sub_wizard = AutoHedgerValuesSubWizard(self.web_driver_container)
            instruments_sub_wizard = AutoHedgerInstrumentsSubWizard(self.web_driver_container)
            instruments_sub_wizard.click_on_edit_button()
            time.sleep(2)

            expected_result_values = [self.name,
                                      self.position_book,
                                      self.symbol,
                                      self.hedging_strategy,
                                      self.long_threshold_qty,
                                      self.long_residual_qty,
                                      self.short_threshold_qty,
                                      self.short_residual_qty]

            actual_result_values = [values_sub_wizard.get_name(),
                                    values_sub_wizard.get_position_book(),
                                    instruments_sub_wizard.get_symbol(),
                                    instruments_sub_wizard.get_hedging_strategy(),
                                    instruments_sub_wizard.get_long_threshold_qty(),
                                    instruments_sub_wizard.get_long_residual_qty(),
                                    instruments_sub_wizard.get_short_threshold_qty(),
                                    instruments_sub_wizard.get_short_residual_qty()
                                    ]
            self.verify("Is values saved correctly after relogin", expected_result_values, actual_result_values)

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            print(traceback.format_exc() + " Search in ->  " + self.__class__.__name__)
