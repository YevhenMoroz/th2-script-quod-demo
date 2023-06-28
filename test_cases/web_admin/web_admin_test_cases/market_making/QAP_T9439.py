import sys
import time
import traceback
from pathlib import Path

from custom import basic_custom_actions
from test_framework.core.try_exept_decorator import try_except
from test_framework.web_admin_core.pages.market_making.quoting_sessions.quoting_sessions_page import \
    QuotingSessionsPage
from test_framework.web_admin_core.pages.market_making.quoting_sessions.quoting_sessions_wizard import \
    QuotingSessionsWizard
from test_framework.web_admin_core.pages.market_making.quoting_sessions.quoting_sessions_client_tier_symbols_sub_wizard \
    import QuotingSessionsClientTiersSymbolsSubWizard
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T9439(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.symbol = ['AUD/BRL', 'AUD/CAD', 'AUD/CHF']
        self.client_tier = ['Gold', 'Silver', 'Bronze']

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        side_menu.open_quoting_sessions_page()

    @try_except(test_id=Path(__file__).name[:-3])
    def test_context(self):
        wizard = QuotingSessionsWizard(self.web_driver_container)
        page = QuotingSessionsPage(self.web_driver_container)
        client_tier_symbols_tab = QuotingSessionsClientTiersSymbolsSubWizard(self.web_driver_container)

        def add_new_client_tier_symbol(symbol, client_tier):
            client_tier_symbols_tab.click_on_plus()
            client_tier_symbols_tab.set_symbol(symbol)
            client_tier_symbols_tab.set_client_tier(client_tier)
            client_tier_symbols_tab.click_on_checkmark()

        self.precondition()

        page.click_on_new()
        add_new_client_tier_symbol(self.symbol[0], self.client_tier[0])
        add_new_client_tier_symbol(self.symbol[0], self.client_tier[1])
        time.sleep(1)
        self.verify("Client Tiers Symbols with the same Symbol and different Client Tiers added",
                    False, wizard.is_error_in_footer_displayed())

        add_new_client_tier_symbol(self.symbol[1], self.client_tier[2])
        add_new_client_tier_symbol(self.symbol[2], self.client_tier[2])
        time.sleep(1)
        self.verify("Client Tiers Symbols with different Symbol and the same Client Tiers added",
                    False, wizard.is_error_in_footer_displayed())
