import random
import string
import sys
import time
import traceback
from pathlib import Path

from custom import basic_custom_actions
from test_framework.core.try_exept_decorator import try_except
from test_framework.web_admin_core.pages.market_making.quoting_sessions.quoting_sessions_client_client_tiers_sub_wizard import \
    QuotingSessionsClientClientTiersSubWizard
from test_framework.web_admin_core.pages.market_making.quoting_sessions.quoting_sessions_client_tier_symbols_sub_wizard import \
    QuotingSessionsClientTiersSymbolsSubWizard
from test_framework.web_admin_core.pages.market_making.quoting_sessions.quoting_sessions_client_tiers_sub_wizard import \
    QuotingSessionsClientTiersSubWizard
from test_framework.web_admin_core.pages.market_making.quoting_sessions.quoting_sessions_page import \
    QuotingSessionsPage
from test_framework.web_admin_core.pages.market_making.quoting_sessions.quoting_sessions_values_sub_wizard import \
    QuotingSessionsValuesSubWizard
from test_framework.web_admin_core.pages.market_making.quoting_sessions.quoting_sessions_wizard import \
    QuotingSessionsWizard
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T3969(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.published_quote_id_format = "#20d"
        self.quote_update_format = "FullRefresh"
        self.concurrently_active_quotes_age = "10"
        self.broadcast_client_client_tier_id = "TEST"
        self.client_tier = "Gold"
        self.symbol = self.data_set.get_symbol_by_name("symbol_1")
        self.client_client_tier_id = "test"

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        time.sleep(2)
        side_menu.open_quoting_sessions_page()
        time.sleep(1)
        page = QuotingSessionsPage(self.web_driver_container)
        wizard = QuotingSessionsWizard(self.web_driver_container)
        values_sub_wizard = QuotingSessionsValuesSubWizard(self.web_driver_container)
        client_tiers_sub_wizard = QuotingSessionsClientTiersSubWizard(self.web_driver_container)
        client_tier_symbols_sub_wizard = QuotingSessionsClientTiersSymbolsSubWizard(self.web_driver_container)
        client_client_tiers_sub_wizard = QuotingSessionsClientClientTiersSubWizard(self.web_driver_container)
        page.click_on_new()
        time.sleep(2)
        values_sub_wizard.set_name(self.name)
        time.sleep(1)
        values_sub_wizard.set_published_quote_id_format(self.published_quote_id_format)
        time.sleep(1)
        values_sub_wizard.set_quote_update_format(self.quote_update_format)
        time.sleep(1)
        values_sub_wizard.set_concurrently_active_quotes_age(self.concurrently_active_quotes_age)
        time.sleep(1)
        values_sub_wizard.click_on_always_use_new_md_entry_id_checkbox()
        time.sleep(1)
        values_sub_wizard.click_on_always_acknowledge_orders_checkbox()
        time.sleep(1)
        values_sub_wizard.click_on_use_same_session_for_market_date_and_trading()
        time.sleep(1)
        client_tiers_sub_wizard.click_on_plus()
        time.sleep(1)
        client_tiers_sub_wizard.set_broadcast_client_client_tier_id(self.broadcast_client_client_tier_id)
        time.sleep(1)
        client_tiers_sub_wizard.set_client_tier(self.client_tier)
        time.sleep(1)
        client_tiers_sub_wizard.click_on_checkmark()
        time.sleep(1)
        client_tier_symbols_sub_wizard.click_on_plus()
        time.sleep(1)
        client_tier_symbols_sub_wizard.set_symbol(self.symbol)
        time.sleep(1)
        client_tier_symbols_sub_wizard.set_client_tier(self.client_tier)
        time.sleep(1)
        client_tier_symbols_sub_wizard.click_on_checkmark()
        time.sleep(1)
        client_client_tiers_sub_wizard.click_on_plus()
        time.sleep(1)
        client_client_tiers_sub_wizard.set_client_client_tier_id(self.client_client_tier_id)
        time.sleep(1)
        client_client_tiers_sub_wizard.set_client_tier(self.client_tier)
        time.sleep(1)
        client_client_tiers_sub_wizard.click_on_checkmark()
        time.sleep(1)
        wizard.click_on_save_changes()
        time.sleep(15)
        page.click_on_user_icon()
        time.sleep(2)
        page.click_on_logout()
        login_page.login_to_web_admin(self.login, self.password)
        time.sleep(2)
        side_menu.open_quoting_sessions_page()
        time.sleep(1)
        page.set_name_filter(self.name)
        time.sleep(2)
        page.click_on_more_actions()
        time.sleep(2)
        page.click_on_edit()
        time.sleep(2)

    @try_except(test_id=Path(__file__).name[:-3])
    def test_context(self):
        self.precondition()
        wizard = QuotingSessionsWizard(self.web_driver_container)

        expected_result_values = [self.name,
                                  self.published_quote_id_format,
                                  self.quote_update_format,
                                  "Always Use New MDEntry ID: true",
                                  "Always Acknowledge Orders: true",
                                  "Use Same Session For Market Data and Trading: true",
                                  self.broadcast_client_client_tier_id,
                                  self.client_tier,
                                  self.symbol,
                                  self.client_tier,
                                  self.client_client_tier_id,
                                  self.client_tier,
                                  ]
        self.verify("Check is entity created correctly in PDF values", True,
                    wizard.click_download_pdf_entity_button_and_check_pdf(expected_result_values))