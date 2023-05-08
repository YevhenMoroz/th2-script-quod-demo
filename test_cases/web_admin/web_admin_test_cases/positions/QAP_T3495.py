import sys
import traceback

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.positions.cash_positions.main_page import *

from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T3495(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")

        self.transaction_type = ['CashLoanDeposit', 'CashLoanWithdrawal', 'CollateralLimit', 'Deposit', 'ReserveLimit',
                                 'TemporaryCashDeposit', 'TemporaryCashWithdrawal', 'Withdrawal']

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        side_menu = SideMenu(self.web_driver_container)

        login_page.login_to_web_admin(self.login, self.password)
        side_menu.open_cash_positions_page()

    def test_context(self):
        cash_positions_page = MainPage(self.web_driver_container)

        try:
            self.precondition()

            cash_positions_page.click_on_transaction()
            transaction_type_options = cash_positions_page.get_all_transaction_type_from_drop_down()

            self.verify(f"These drop-down contains such values {self.transaction_type}",
                        sorted(self.transaction_type), sorted(transaction_type_options))

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
