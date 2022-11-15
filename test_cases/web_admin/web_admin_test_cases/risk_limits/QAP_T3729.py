import random
import string
import sys
import time
import traceback

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.risk_limits.cum_trading_limits.cum_trading_limits_dimensions_sub_wizard import \
    CumTradingLimitsDimensionsSubWizard
from test_framework.web_admin_core.pages.risk_limits.cum_trading_limits.cum_trading_limits_page import \
    CumTradingLimitsPage
from test_framework.web_admin_core.pages.risk_limits.cum_trading_limits.cum_trading_limits_values_sub_wizard import \
    CumTradingLimitsValuesSubWizard
from test_framework.web_admin_core.pages.risk_limits.cum_trading_limits.cum_trading_limits_wizard import \
    CumTradingLimitsWizard
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T3729(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = "adm03"
        self.password = "adm03"
        self.description = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.external_id = '11'
        self.currency = "EUR"
        self.max_amount = "150000000"
        self.user = "acameron"

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        time.sleep(2)
        side_menu.open_cum_trading_limits_page()
        page = CumTradingLimitsPage(self.web_driver_container)
        wizard = CumTradingLimitsWizard(self.web_driver_container)
        values_sub_wizard = CumTradingLimitsValuesSubWizard(self.web_driver_container)
        dimensions_sub_wizard = CumTradingLimitsDimensionsSubWizard(self.web_driver_container)
        page.click_on_new()
        time.sleep(1)
        values_sub_wizard.set_description(self.description)
        values_sub_wizard.set_external_id(self.external_id)
        values_sub_wizard.set_currency(self.currency)
        values_sub_wizard.set_max_amount(self.max_amount)
        dimensions_sub_wizard.set_user(self.user)
        wizard.click_on_save_changes()
        time.sleep(2)
        page.set_description(self.description)
        time.sleep(2)

    def test_context(self):

        try:
            self.precondition()
            page = CumTradingLimitsPage(self.web_driver_container)
            page.click_on_more_actions()
            self.verify("Is cumtrading limit created correctly", True, True)

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id, status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
