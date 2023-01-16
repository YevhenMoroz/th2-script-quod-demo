import sys
import time
import traceback

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.market_making.auto_hedger.auto_hedger_instruments_sub_wizard \
    import AutoHedgerInstrumentsSubWizard
from test_framework.web_admin_core.pages.market_making.auto_hedger.auto_hedger_page import AutoHedgerPage

from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T9217(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        side_menu.open_auto_hedger_page()
        page = AutoHedgerPage(self.web_driver_container)
        page.click_on_new()

    def test_context(self):
        try:
            self.precondition()
            instruments_tab = AutoHedgerInstrumentsSubWizard(self.web_driver_container)
            instruments_tab.click_on_plus_button()
            time.sleep(1)
            expected_result = [True for _ in range(4)]
            actual_result = [instruments_tab.is_execution_strategy_field_displayed(),
                             instruments_tab.is_execution_strategy_tif_field_displayed(),
                             instruments_tab.is_execution_strategy_max_duration_field_displayed(),
                             instruments_tab.is_request_approval_checkbox_displayed()]

            self.verify("New fields for Instrument displayed", expected_result, actual_result)

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
