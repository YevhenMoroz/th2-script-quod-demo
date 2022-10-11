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


class QAP_T3676(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.description = "QAP4966"
        self.new_description = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.max_quantity = str(random.randint(1000, 10000))
        self.max_amount = str(random.randint(100, 1000))
        self.currency = ''

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        time.sleep(2)
        side_menu = SideMenu(self.web_driver_container)
        side_menu.open_trading_limits_page()
        time.sleep(2)
        main_page = TradingLimitsPage(self.web_driver_container)
        main_page.set_description(self.description)
        time.sleep(1)
        if not main_page.is_searched_entity_found_by_description(self.description):
            main_page.click_on_new()
            time.sleep(2)
            value_tab = TradingLimitsValuesSubWizardPage(self.web_driver_container)
            value_tab.set_description(self.description)
            wizard = TradingLimitsWizard(self.web_driver_container)
            wizard.click_on_save_changes()
            time.sleep(2)

    def post_conditions(self):
        value_tab = TradingLimitsValuesSubWizardPage(self.web_driver_container)
        value_tab.set_description(self.description)
        wizard = TradingLimitsWizard(self.web_driver_container)
        wizard.click_on_save_changes()

    def test_context(self):
        try:
            self.precondition()

            main_page = TradingLimitsPage(self.web_driver_container)
            main_page.set_description(self.description)
            time.sleep(1)
            main_page.click_on_more_actions()
            time.sleep(1)
            main_page.click_on_edit()
            time.sleep(2)
            value_tab = TradingLimitsValuesSubWizardPage(self.web_driver_container)
            value_tab.set_description(self.new_description)
            value_tab.set_max_quantity(self.max_quantity)
            value_tab.set_max_amount(self.max_amount)
            all_currency = value_tab.get_all_currency_from_drop_menu()
            self.currency = random.choice(all_currency)
            value_tab.set_currency(self.currency)
            wizard = TradingLimitsWizard(self.web_driver_container)
            wizard.click_on_save_changes()
            time.sleep(2)

            main_page.set_description(self.new_description)
            time.sleep(1)
            main_page.click_on_more_actions()
            time.sleep(1)
            main_page.click_on_edit()
            time.sleep(2)

            expected_result = [self.new_description, self.max_quantity, self.max_amount, self.currency]
            actual_result = [value_tab.get_description(), value_tab.get_max_quantity(), value_tab.get_max_amount(),
                             value_tab.get_currency()]
            self.verify("New data has been saved correctly", expected_result, actual_result)

            self.post_conditions()

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
