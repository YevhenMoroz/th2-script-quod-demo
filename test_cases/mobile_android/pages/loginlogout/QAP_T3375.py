from appium_flutter_finder import FlutterElement, FlutterFinder

from test_cases.mobile_android.common_test_case import CommonTestCase
from test_framework.mobile_android_core.utils.common_page import CommonPage
from test_framework.mobile_android_core.pages.login.login_page import LoginPage
from test_framework.mobile_android_core.utils.driver import AppiumDriver

from pathlib import Path
from test_framework.mobile_android_core.utils.decorators.try_except_decorator_mobile import try_except
import time

class QAP_T3375(CommonTestCase):

    def __init__(self, driver: AppiumDriver, report_id=None, data_set=None, environment=None):
        super().__init__(driver, self.__class__.__name__, report_id, data_set=data_set,
                         environment=environment)
        self.appium_driver = driver
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")

    @try_except(test_id=Path(__file__).name[:-3])
    def test_context(self):
        # region - preconditions
        login_page = LoginPage(self.appium_driver)

        # login_page.click_field_username()
        login_page.enter_data_field_username("a_MobileQA1")

        # login_page.click_field_password()
        login_page.enter_data_field_password("a_MobileQA1!")

        # login_page.tap("buttonLogin")
        #
        # login_page.tap("buttonUserProfile")
        #
        # login_page.tap("buttonLogout")
        print(login_page.is_element_presented("usernameField"))
        print(login_page.is_element_presented("passwordField"))
        print(login_page.is_element_presented("buttonLogout", 100))
        print(login_page.is_element_presented("buttonUserProfile", 100))

        login_page.tap("buttonLogin")

        print(login_page.is_element_presented("buttonUserProfile", 2000))
        print(login_page.is_element_presented("usernameField"))
        time.sleep(3)

        # finder = FlutterFinder()
        #
        # text_finder = finder.by_value_key("usernameField")
        # text_element = FlutterElement(self.appium_driver.get_driver(), text_finder)
        # text_element.click()
        # text_element.send_keys("a_MobileQA1")
        #
        # passwordField = FlutterElement(self.appium_driver.get_driver(), finder.by_value_key("passwordField"))
        # passwordField.click()
        # passwordField.send_keys("a_MobileQA1!")
        #
        # loginButton = FlutterElement(self.appium_driver.get_driver(), finder.by_value_key("buttonLogin"))
        # loginButton.click()
        # time.sleep(4)
        #
        # userProfileButton = FlutterElement(self.appium_driver.get_driver(), finder.by_value_key("buttonUserProfile"))
        # userProfileButton.click()
        #
        # buttonLogout = FlutterElement(self.appium_driver.get_driver(), finder.by_value_key("buttonLogout"))
        # buttonLogout.click()
        # time.sleep(2)
        #
        # try:
        #     self.appium_driver.get_driver().execute_script('flutter:waitFor', finder.by_value_key("passwordField"), 100)
        # except:
        #     print("There is an Error, couldn't find 'passwordField'")
        # passwordField = FlutterElement(self.appium_driver.get_driver(), finder.by_value_key("passwordField"))
        # assert (passwordField.text == '')
        # print(passwordField)
        #
        # # try:
        # #     self.appium_driver.get_driver().execute_script('flutter:waitFor', finder.by_value_key("buttonOrderTicket"), 100)
        # # except:
        # #     print("There is an EXPECTED Error, couldn't find 'buttonOrderTicket'")
        # self.verify("Step Last - All Actions are done", None, None)

        # region - postconditions
        # endregion
