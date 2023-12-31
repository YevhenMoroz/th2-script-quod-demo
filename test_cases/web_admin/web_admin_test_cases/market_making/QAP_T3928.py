import random
import string
import sys
import time
import traceback
from pathlib import Path

from custom import basic_custom_actions
from test_framework.core.try_exept_decorator import try_except
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


class QAP_T3928(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.position_book = "QUODAH"
        self.symbol = self.data_set.get_symbol_by_name("symbol_3")
        self.hedging_strategy = "PositionLimits"

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        time.sleep(2)
        side_menu.open_auto_hedger_page()
        time.sleep(2)
        page = AutoHedgerPage(self.web_driver_container)
        page.click_on_new()
        time.sleep(2)
        values_sub_wizard = AutoHedgerValuesSubWizard(self.web_driver_container)
        values_sub_wizard.set_name(self.name)
        time.sleep(1)
        values_sub_wizard.set_position_book(self.position_book)

    @try_except(test_id=Path(__file__).name[:-3])
    def test_context(self):
        self.precondition()
        instruments_sub_wizard = AutoHedgerInstrumentsSubWizard(self.web_driver_container)
        instruments_sub_wizard.click_on_plus_button()
        time.sleep(2)
        instruments_sub_wizard.set_symbol(self.symbol)
        time.sleep(1)
        instruments_sub_wizard.set_hedging_strategy(self.hedging_strategy)
        time.sleep(1)
        instruments_sub_wizard.click_on_checkmark_button()
        time.sleep(1)
        wizard = AutoHedgerWizard(self.web_driver_container)
        wizard.click_on_save_changes()
        time.sleep(2)
        page = AutoHedgerPage(self.web_driver_container)
        page.set_name_filter(self.name)
        time.sleep(2)
        page.click_on_more_actions()
        time.sleep(2)
        page.click_on_edit()
        time.sleep(2)
        self.verify("Is 'Position Book already assigned to' message displayed", True,
                    wizard.is_position_book_assigned_to_message_displayed())
