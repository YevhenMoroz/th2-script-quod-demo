import random
import string
import sys
import time
import traceback

from custom import basic_custom_actions
from test_cases.web_admin.web_admin_core.pages.market_making.auto_hedger.auto_hedger_internal_client_sub_wizard import \
    AutoHedgerInternalClientsSubWizard
from test_cases.web_admin.web_admin_core.pages.market_making.auto_hedger.auto_hedger_page import AutoHedgerPage
from test_cases.web_admin.web_admin_core.pages.market_making.auto_hedger.auto_hedger_values_sub_wizard import \
    AutoHedgerValuesSubWizard
from test_cases.web_admin.web_admin_core.pages.login.login_page import LoginPage
from test_cases.web_admin.web_admin_core.pages.root.side_menu import SideMenu
from test_cases.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_4118(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id)
        self.login = "adm03"
        self.password = "adm03"
        self.name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.position_book = "QUODAH"
        self.symbol = "AUD/TRY"
        self.hedging_strategy = "PositionLimits"

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        time.sleep(2)
        side_menu.open_auto_hedger_page()
        time.sleep(2)
        page = AutoHedgerPage(self.web_driver_container)
        page.click_on_new()
        time.sleep(2)
        values_sub_wizard = AutoHedgerValuesSubWizard(self.web_driver_container)
        values_sub_wizard.set_position_book(self.position_book)

    def test_context(self):

        try:
            self.precondition()
            internal_client_sub_wizard  = AutoHedgerInternalClientsSubWizard(self.web_driver_container)
            internal_client_sub_wizard.click_on_plus()
            time.sleep(2)
            try:
                internal_client_sub_wizard.set_client(self.position_book)
                self.verify("Client set, it's issue",False,True)
            except Exception:
                self.verify("Client not set, because same is in position book",True,True)

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
