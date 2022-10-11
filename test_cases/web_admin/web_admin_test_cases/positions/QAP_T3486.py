import sys
import time
import traceback

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.positions.cash_positions.cash_postitions_page import CashPositionsPage
from test_framework.web_admin_core.pages.positions.cash_positions.cash_positions_wizard import CashPositionsWizard
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T3486(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")

        self.labels = {"values_tab": ["Name", "Currency", "Client", "Venue CashAccount ID", "Client CashAccount ID"],
                       "positions_tab": ["Actual Balance", "Available Balance", "Initial Balance", "Reserved Amount",
                                         "Sell Amount", "Buy Amount", "Cash Deposited", "Cash Withdrawn",
                                         "Cash Held by Transactions", "Cash Loan", "Booked Cash Loan", "Temporary Cash",
                                         "Booked Temporary Cash", "Collateral", "Booked Collateral"]}

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        time.sleep(2)
        side_menu = SideMenu(self.web_driver_container)
        side_menu.open_cash_positions_page()

    def test_context(self):
        try:
            self.precondition()

            cash_positions_page = CashPositionsPage(self.web_driver_container)
            cash_positions_page.click_on_more_actions()
            cash_positions_page.click_on_edit()

            wizard = CashPositionsWizard(self.web_driver_container)
            self.verify("PDF file contains correct names of labels and corresponded values like in 'self.labels'", True,
                        wizard.click_download_pdf_entity_button_and_check_pdf(self.labels["values_tab"]))
            self.verify("PDF file contains correct names of labels and corresponded values like in 'self.labels'", True,
                        wizard.click_download_pdf_entity_button_and_check_pdf(self.labels["positions_tab"]))

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
