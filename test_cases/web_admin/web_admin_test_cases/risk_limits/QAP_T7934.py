import random
import sys
import traceback

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.risk_limits.cumtrdlmt_counter.cumtrdlmt_counter_page import CumTrdLmtPage
from test_framework.web_admin_core.pages.risk_limits.cumtrdlmt_counter.cumtrdlmt_counter_wizard \
    import CumTrdLmtCounterWizard
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T7934(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.cum_trading_limit = ''
        self.cum_buy_ord_qty = random.randint(1, 100)
        self.cum_ord_amount = random.randint(1, 100)
        self.cum_sell_ord_qty = random.randint(1, 100)
        self.cum_buy_ord_amt = random.randint(1, 100)
        self.cum_ord_qty = random.randint(1, 100)
        self.cum_sell_ord_amt = random.randint(1, 100)
        self.cum_leaves_ord_amt = random.randint(1, 100)

        self.fields_name = ["Cum Trading Limit", "Cum Buy Ord Qty", "Cum Ord Amt", "Cum Sell Ord Qty",
                            "Cum Buy Ord Amt", "Cum Ord Qty", "Cum Sell Ord Amt", "Cum Leaves Ord Amt"]

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        side_menu.open_cumtrdlmt_counter_page()

    def test_context(self):
        try:
            self.precondition()

            main_page = CumTrdLmtPage(self.web_driver_container)
            main_page.click_on_new()

            wizard = CumTrdLmtCounterWizard(self.web_driver_container)

            self.verify("PDF contains all fields name", True,
                        wizard.click_download_pdf_entity_button_and_check_pdf(self.fields_name))

            self.cum_trading_limit = random.choice(wizard.get_all_cum_trading_limit_from_drop_menu())
            wizard.set_cum_trading_limit(self.cum_trading_limit)
            wizard.set_cum_buy_ord_qty(self.cum_buy_ord_qty)
            wizard.set_cum_ord_amt(self.cum_ord_amount)
            wizard.set_cum_sell_ord_qty(self.cum_sell_ord_qty)
            wizard.set_cum_buy_ord_amt(self.cum_buy_ord_amt)
            wizard.set_cum_ord_qty(self.cum_ord_qty)
            wizard.set_cum_sell_ord_amt(self.cum_sell_ord_amt)
            wizard.set_cum_leaves_ord_amt(self.cum_leaves_ord_amt)

            self.verify("PDF contains all fields name", True,
                        wizard.click_download_pdf_entity_button_and_check_pdf(self.fields_name))
            actual_result = [self.cum_trading_limit, self.cum_buy_ord_qty, self.cum_ord_amount, self.cum_sell_ord_qty,
                             self.cum_buy_ord_amt, self.cum_ord_qty, self.cum_sell_ord_amt, self.cum_leaves_ord_amt]
            self.verify("PDF contains all values field", True,
                        wizard.click_download_pdf_entity_button_and_check_pdf(actual_result))

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
