import sys
import traceback

from custom import basic_custom_actions
from test_cases.mobile_android.common_test_case import CommonTestCase
from test_framework.mobile_android_core.utils.common_page import CommonPage
from test_framework.mobile_android_core.pages.login.login_constant import LoginConstants
from test_framework.mobile_android_core.pages.login.login_page import LoginPage

from test_framework.mobile_android_core.utils.driver import AppiumDriver


class QAP_6877(CommonTestCase):

    def __init__(self, driver: AppiumDriver, second_lvl_id=None):
        super().__init__(driver, self.__class__.__name__, second_lvl_id)
        self.email = "QA4"
        self.password = "QA4"

    def test_context(self):
        try:
            login_page = LoginPage(self.appium_driver)
            common_page = CommonPage(self.appium_driver)
            login_page.open_login_page(self.email)
            self.appium_driver.wait_time(2)
            #time.sleep(2) #add implicit wait -> selenium can help with it
            self.verify("Login successful", True, True)
            self.verify("Verify: E-mail widget is unclickable", "false",
                        common_page.get_attribute_of_element_by_xpath(LoginConstants.EMAIL_LOGIN, "clickable"))

        except Exception as e:
            basic_custom_actions.create_event("TEST FAILED on Login Page", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
            print(e.__class__)
