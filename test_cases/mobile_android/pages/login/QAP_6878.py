import sys
import time
import traceback

from custom import basic_custom_actions
from test_cases.mobile_android.common_test_case import CommonTestCase
from test_framework.mobile_android_core.pages.login.login_page import LoginPage


from test_framework.mobile_android_core.utils.driver import AppiumDriver


class QAP_6878(CommonTestCase):

    def __init__(self, driver: AppiumDriver, second_lvl_id=None):
        super().__init__(driver, self.__class__.__name__, second_lvl_id)
        self.email = "QA4"
        self.password = "QA4"

    def precondition(self):
        time.sleep(2)
        #deactivate QA4 user

    def test_context(self):
        try:
            login_page = LoginPage(self.appium_driver)
            login_page.open_login_page(self.email)
            time.sleep(2) #add implicit wait -> selenium can help with it
            self.verify("Login successful", True, True)
            self.verify("Verify: Authentication Failure text is displayed", "true",
                        login_page.get_attribute_auth("displayed"))
        except Exception as e:
            basic_custom_actions.create_event("TEST FAILED on Login Page", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
            print(e.__class__)
