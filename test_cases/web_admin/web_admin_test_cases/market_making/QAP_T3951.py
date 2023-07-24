import random
import string
import sys
import time
import traceback
from pathlib import Path

from custom import basic_custom_actions
from test_framework.core.try_exept_decorator import try_except
from test_framework.web_admin_core.pages.general.common.common_page import CommonPage
from test_framework.web_admin_core.pages.market_making.auto_hedger.auto_hedger_instruments_sub_wizard import \
    AutoHedgerInstrumentsSubWizard
from test_framework.web_admin_core.pages.market_making.auto_hedger.auto_hedger_page import AutoHedgerPage
from test_framework.web_admin_core.pages.market_making.auto_hedger.auto_hedger_values_sub_wizard import \
    AutoHedgerValuesSubWizard
from test_framework.web_admin_core.pages.market_making.auto_hedger.auto_hedger_wizard import AutoHedgerWizard

from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T3951(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.position_book = 'QUODAH'
        self.symbol = self.data_set.get_symbol_by_name("symbol_2")
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
        time.sleep(1)
        values_sub_wizard.set_position_book(self.position_book)
        time.sleep(2)
        instruments_sub_wizard = AutoHedgerInstrumentsSubWizard(self.web_driver_container)
        instruments_sub_wizard.click_on_plus_button()
        time.sleep(1)
        instruments_sub_wizard.set_symbol(self.symbol)
        time.sleep(1)
        instruments_sub_wizard.set_hedging_strategy(self.hedging_strategy)
        instruments_sub_wizard.set_long_threshold_qty(self.long_threshold_qty)
        instruments_sub_wizard.set_long_residual_qty(self.long_residual_qty)
        instruments_sub_wizard.set_short_threshold_qty(self.short_threshold_qty)
        instruments_sub_wizard.set_short_residual_qty(self.short_residual_qty)
        instruments_sub_wizard.click_on_checkmark_button()
        time.sleep(1)
        wizard.click_on_save_changes()
        time.sleep(2)
        common_page = CommonPage(self.web_driver_container)
        common_page.click_on_info_error_message_pop_up()
        main_page.click_on_user_icon()
        time.sleep(1)
        main_page.click_on_logout()
        time.sleep(2)
        login_page.login_to_web_admin(self.login, self.password)
        time.sleep(2)
        side_menu.open_auto_hedger_page()
        time.sleep(2)
        main_page.set_name_filter(self.name)
        time.sleep(1)
        main_page.click_on_more_actions()
        time.sleep(1)
        main_page.click_on_edit()
        time.sleep(1)

    @try_except(test_id=Path(__file__).name[:-3])
    def test_context(self):
        self.precondition()
        values_sub_wizard = AutoHedgerValuesSubWizard(self.web_driver_container)
        instruments_sub_wizard = AutoHedgerInstrumentsSubWizard(self.web_driver_container)
        instruments_sub_wizard.click_on_edit_button()
        time.sleep(2)

        expected_result_values = [self.name,
                                  self.position_book,
                                  self.symbol,
                                  self.long_threshold_qty,
                                  self.hedging_strategy,
                                  self.long_residual_qty,
                                  self.short_threshold_qty,
                                  self.short_residual_qty]

        actual_result_values = [values_sub_wizard.get_name(),
                                values_sub_wizard.get_position_book(),
                                instruments_sub_wizard.get_symbol(),
                                instruments_sub_wizard.get_long_threshold_qty(),
                                instruments_sub_wizard.get_hedging_strategy(),
                                instruments_sub_wizard.get_long_residual_qty(),
                                instruments_sub_wizard.get_short_threshold_qty(),
                                instruments_sub_wizard.get_short_residual_qty()]
        self.verify("Is values saved correctly after relogin", expected_result_values, actual_result_values)
