import sys
import traceback

from custom import basic_custom_actions
from test_cases.mobile_android.common_test_case import CommonTestCase
from test_framework.mobile_android_core.pages.login.login_constant import LoginConstants
from test_framework.mobile_android_core.pages.login.login_page import LoginPage

from test_framework.mobile_android_core.utils.driver import AppiumDriver

from pathlib import Path
from test_framework.mobile_android_core.utils.try_except_decorator_mobile import try_except

class QAP_6877(CommonTestCase):

    def __init__(self, driver: AppiumDriver, second_lvl_id=None, data_set=None, environment=None):
        super().__init__(driver, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")

    @try_except(test_id=Path(__file__).name[:-3])
    def test_context(self):
        login_page = LoginPage(self.appium_driver)
        login_page.open_login_page(self.login)
        self.appium_driver.wait_time(2)
        self.verify("Login successful", True, True)
        self.verify("Verify: E-mail widget is unclickable", "false",
                    login_page.get_attribute_of_element_by_xpath(LoginConstants.EMAIL_LOGIN, "clickable"))