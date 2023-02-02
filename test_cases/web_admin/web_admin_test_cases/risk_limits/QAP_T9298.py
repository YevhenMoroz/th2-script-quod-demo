import random
import string
import sys
import time
import traceback

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.risk_limits.trading_limits.trading_limits_page import TradingLimitsPage
from test_framework.web_admin_core.pages.risk_limits.trading_limits.trading_limits_wizard import TradingLimitsWizard
from test_framework.web_admin_core.pages.risk_limits.trading_limits.trading_limits_values_sub_wizard \
    import TradingLimitsValuesSubWizardPage
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T9298(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.description = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.currency = 'EUR'
        self.min_display_percentage = ['1234', '-31', '40']
        self.min_display = '500'
        self.max_display = '1000'
        self.max_soft_display = '1500'

        self.expected_result = 'Percentage should between 0 and 100'

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        side_menu.open_trading_limits_page()

    def post_conditions(self):
        main_page = TradingLimitsPage(self.web_driver_container)
        main_page.set_description(self.description)
        time.sleep(1)
        main_page.click_on_more_actions()
        main_page.click_on_delete(True)

    def test_context(self):
        try:
            self.precondition()

            main_page = TradingLimitsPage(self.web_driver_container)
            main_page.click_on_new()
            value_tab = TradingLimitsValuesSubWizardPage(self.web_driver_container)
            value_tab.set_description(self.description)
            value_tab.set_currency(self.currency)
            value_tab.set_min_display_percentage(self.min_display_percentage[0])
            wizard = TradingLimitsWizard(self.web_driver_container)
            wizard.click_on_save_changes()
            time.sleep(1)
            actual_result = wizard.get_footer_warning_text()
            self.verify("Error appears", self.expected_result, actual_result)

            value_tab.set_min_display_percentage(self.min_display_percentage[1])
            wizard.click_on_save_changes()
            time.sleep(1)
            actual_result = wizard.get_footer_warning_text()
            self.verify("Error appears", self.expected_result, actual_result)

            value_tab.set_min_display_percentage(self.min_display_percentage[2])
            value_tab.set_min_display(self.min_display)
            value_tab.set_max_display(self.max_display)
            wizard.click_on_save_changes()

            main_page.set_description(self.description)
            time.sleep(1)
            main_page.click_on_more_actions()
            main_page.click_on_edit()
            expected_result = [self.description, self.min_display_percentage[2], self.min_display, self.max_display]
            actual_result = [value_tab.get_description(), value_tab.get_min_display_percentage(),
                             value_tab.get_min_display(), value_tab.get_max_display()]
            self.verify("New rule is created with all entered fields", expected_result, actual_result)
            wizard.click_on_save_changes()

            self.post_conditions()

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
