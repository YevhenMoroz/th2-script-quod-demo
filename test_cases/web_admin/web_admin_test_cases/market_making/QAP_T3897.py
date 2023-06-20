import random
import string
import sys
import time
import traceback
from pathlib import Path

from custom import basic_custom_actions
from test_framework.core.try_exept_decorator import try_except
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


class QAP_T3897(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.concurrently_active_quotes = 100
        self.quote_update_interval = 300

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        time.sleep(2)
        side_menu.open_quoting_sessions_page()
        time.sleep(1)
        page = QuotingSessionsPage(self.web_driver_container)
        values_sub_wizard = QuotingSessionsValuesSubWizard(self.web_driver_container)
        page.click_on_new()
        time.sleep(2)
        values_sub_wizard.set_name(self.name)
        values_sub_wizard.set_concurrently_active_quotes_age(self.concurrently_active_quotes)
        values_sub_wizard.set_quote_update_interval(self.quote_update_interval)
        time.sleep(1)

    @try_except(test_id=Path(__file__).name[:-3])
    def test_context(self):
        self.precondition()
        wizard = QuotingSessionsWizard(self.web_driver_container)
        page = QuotingSessionsPage(self.web_driver_container)
        expected_result_values = [self.name,
                                  str(self.concurrently_active_quotes),
                                  str(self.quote_update_interval),
                                  ]
        self.verify("Check entity in PDF ", True,
                    wizard.click_download_pdf_entity_button_and_check_pdf(expected_result_values))
        wizard.click_on_save_changes()
        page.set_name_filter(self.name)
        time.sleep(2)
        page.click_on_more_actions()
        time.sleep(2)
        self.verify("Check entity values in PDF after saving", True,
                    page.click_download_pdf_entity_button_and_check_pdf(expected_result_values))
