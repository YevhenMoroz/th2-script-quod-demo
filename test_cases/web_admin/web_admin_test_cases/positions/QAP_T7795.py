import random
import string
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


class QAP_T7795(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")

        self.name = [''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6)) for _ in range(2)]
        self.client_cash_account_id = [''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
                                       for _ in range(2)]
        self.venue_cash_account_id = [''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
                                      for _ in range(2)]

        self.currency = 'EUR'
        self.client = 'CLIENT1'

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
            cash_positions_page.click_on_new()
            wizard = CashPositionsWizard(self.web_driver_container)
            wizard.set_name(self.name[0])
            wizard.set_client_cash_account_id(self.client_cash_account_id[0])
            wizard.set_venue_cash_account_id(self.venue_cash_account_id[0])
            wizard.set_currency(self.currency)
            wizard.set_client(self.client)
            wizard.click_on_save_changes()

            cash_positions_page.click_on_new()
            wizard = CashPositionsWizard(self.web_driver_container)
            wizard.set_name(self.name[1])
            wizard.set_client_cash_account_id(self.client_cash_account_id[1])
            wizard.set_venue_cash_account_id(self.venue_cash_account_id[1])
            wizard.set_currency(self.currency)
            wizard.set_client(self.client)
            wizard.click_on_save_changes()

            cash_positions_page.set_name(self.name[0])
            time.sleep(1)
            self.verify("Firs entity has been saved", True,
                        cash_positions_page.is_searched_cash_account_found(self.name[0]))
            cash_positions_page.click_on_more_actions()
            cash_positions_page.click_on_delete(True)

            cash_positions_page.set_name(self.name[1])
            time.sleep(1)
            self.verify("Second entity has been saved", True,
                        cash_positions_page.is_searched_cash_account_found(self.name[1]))
            cash_positions_page.click_on_more_actions()
            cash_positions_page.click_on_delete(True)

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
