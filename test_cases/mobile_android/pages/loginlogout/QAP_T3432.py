import sys
import time
import traceback

from custom import basic_custom_actions
from test_cases.mobile_android.common_test_case import CommonTestCase
from test_framework.mobile_android_core.pages.login.login_page import LoginPage
from test_framework.mobile_android_core.pages.main_page.main_page import MainPage

from test_framework.mobile_android_core.utils.driver import AppiumDriver


class QAP_T3432(CommonTestCase):

    def __init__(self, driver: AppiumDriver, second_lvl_id=None):
        super().__init__(driver, self.__class__.__name__, second_lvl_id)
        self.email = "User_Ret2"
        self.password = "User_Ret2"

    def precondition(self):
        login_page = LoginPage(self.appium_driver)
        login_page.login_to_mobile_trading(self.email, self.password)
        time.sleep(2)
        main_page = MainPage(self.appium_driver)
        main_page.click_on_create_new_order()

    def test_context(self):
        try:
            self.precondition()
            self.verify("Login successful", True, True)

        except Exception as e:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
            print(e.__class__)
