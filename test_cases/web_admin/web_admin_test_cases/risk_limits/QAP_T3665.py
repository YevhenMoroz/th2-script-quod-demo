import random
import string
import sys
import time
import traceback

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.risk_limits.cum_trading_limits.cum_trading_limits_page \
    import CumTradingLimitsPage
from test_framework.web_admin_core.pages.risk_limits.cum_trading_limits.cum_trading_limits_wizard \
    import CumTradingLimitsWizard
from test_framework.web_admin_core.pages.risk_limits.cum_trading_limits.cum_trading_limits_dimensions_sub_wizard \
    import CumTradingLimitsDimensionsSubWizard
from test_framework.web_admin_core.pages.risk_limits.cum_trading_limits.cum_trading_limits_values_sub_wizard \
    import CumTradingLimitsValuesSubWizard
from test_framework.web_admin_core.pages.risk_limits.cum_trading_limits.cum_trading_limits_assignments_sub_wizard \
    import CumTradingLimitsAssignmentsSubWizard
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T3665(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.description = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.external_id = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.currency = "EUR"
        self.max_quantity = str(random.randint(1, 1000))
        self.soft_max_qty = str(random.randint(1, 1000))
        self.max_buy_qty = str(random.randint(1, 1000))
        self.soft_max_buy_qty = str(random.randint(1, 1000))
        self.max_sell_qty = str(random.randint(1, 1000))
        self.soft_max_sell_qty = str(random.randint(1, 1000))
        self.max_amount = str(random.randint(1, 1000))
        self.soft_max_amt = str(random.randint(1, 1000))
        self.max_buy_amt = str(random.randint(1, 1000))
        self.soft_max_buy_amt = str(random.randint(1, 1000))
        self.max_sell_amt = str(random.randint(1, 1000))
        self.soft_max_sell_amt = str(random.randint(1, 1000))
        self.max_open_order_amount = str(random.randint(1, 1000))

        self.venue = "AMEX"
        self.subvenue = "Forward"

        self.listing_group = "test"
        self.user = "12"
        self.desk = "Quod Desk"
        self.route = "Credit Suisse"
        self.instrument_type = "Bond"
        self.client = "CLIENT2"
        self.client_group = "DEMO"
        self.account = "DEMOM1"
        self.instr_symbol = "CAD/BRL"

        self.institution = "QUOD FINANCIAL"

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        time.sleep(2)
        side_menu = SideMenu(self.web_driver_container)
        side_menu.open_cum_trading_limits_page()
        time.sleep(2)
        main_page = CumTradingLimitsPage(self.web_driver_container)
        main_page.click_on_new()
        time.sleep(2)
        value_tab = CumTradingLimitsValuesSubWizard(self.web_driver_container)
        value_tab.set_description(self.description)
        value_tab.set_external_id(self.external_id)
        value_tab.set_currency(self.currency)
        value_tab.set_max_quantity(self.max_quantity)
        value_tab.set_soft_max_quantity(self.soft_max_qty)
        value_tab.set_max_buy_qty(self.max_buy_qty)
        value_tab.set_soft_max_buy_qty(self.soft_max_buy_qty)
        value_tab.set_max_sell_qty(self.max_sell_qty)
        value_tab.set_soft_max_sell_qty(self.soft_max_sell_qty)
        value_tab.set_max_amount(self.max_amount)
        value_tab.set_soft_max_amt(self.soft_max_amt)
        value_tab.set_max_buy_amt(self.max_buy_amt)
        value_tab.set_soft_max_buy_amt(self.soft_max_buy_amt)
        value_tab.set_max_sell_amt(self.max_sell_amt)
        value_tab.set_soft_max_sell_amt(self.soft_max_sell_amt)
        value_tab.set_max_open_order_amount(self.max_open_order_amount)
        dimensions_tab = CumTradingLimitsDimensionsSubWizard(self.web_driver_container)
        dimensions_tab.set_venue(self.venue)
        dimensions_tab.set_sub_venue(self.subvenue)
        dimensions_tab.set_listing_group(self.listing_group)
        dimensions_tab.click_on_per_listing()
        dimensions_tab.set_user(self.user)
        dimensions_tab.set_desk(self.desk)
        dimensions_tab.set_route(self.route)
        dimensions_tab.set_instrument_type(self.instrument_type)
        dimensions_tab.set_client(self.client)
        dimensions_tab.set_client_group(self.client_group)
        dimensions_tab.set_account(self.account)
        dimensions_tab.set_instr_symbol(self.instr_symbol)
        assignments_tab = CumTradingLimitsAssignmentsSubWizard(self.web_driver_container)
        assignments_tab.set_institution(self.institution)

    def test_context(self):
        try:
            self.precondition()

            wizard = CumTradingLimitsWizard(self.web_driver_container)
            actual_result = [self.description, self.external_id, self.currency, self.max_quantity, self.soft_max_qty,
                             self.max_buy_qty, self.soft_max_buy_qty, self.max_sell_qty, self.soft_max_sell_qty,
                             self.max_amount, self.soft_max_amt, self.max_buy_amt, self.soft_max_buy_amt,
                             self.max_sell_amt, self.soft_max_sell_amt, self.max_open_order_amount, self.venue,
                             self.subvenue, self.listing_group, self.user, self.desk, self.route,
                             self.instrument_type, self.client, self.client_group, self.account, self.instr_symbol,
                             self.institution, "true"]
            self.verify("PDF contains all data", True,
                        wizard.click_download_pdf_entity_button_and_check_pdf(actual_result))

            wizard.click_on_save_changes()
            time.sleep(2)
            main_page = CumTradingLimitsPage(self.web_driver_container)
            main_page.set_description(self.description)
            time.sleep(1)

            self.verify("New CumTradingLimits displayed at main page", True,
                        main_page.is_searched_cum_trading_limits_found(self.description))

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
