import sys
import time
import traceback

from custom import basic_custom_actions

from test_cases.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase
from test_framework.web_trading.web_trading_core.pages.login.login_page import LoginPage
from test_framework.web_trading.web_trading_core.pages.main_page.main_page import MainPage

#DOUBLE CHECK
class QAP_6436(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id)
        self.version = 'Version 5.1.145.158.RET.1643831102_75265687'

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        self.actual_version = login_page.get_version()
        time.sleep(2)

    def test_context(self):
        try:
            self.precondition()

            self.verify("Are the version and revision number correct? ", self.version, self.actual_version)

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)