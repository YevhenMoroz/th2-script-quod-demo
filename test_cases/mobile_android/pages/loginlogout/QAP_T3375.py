import sys
import traceback

from custom import basic_custom_actions
from test_cases.mobile_android.common_test_case import CommonTestCase
from test_framework.mobile_android_core.pages.login.login_constant import LoginConstants
from test_framework.mobile_android_core.pages.login.login_page import LoginPage

from test_framework.mobile_android_core.pages.main_page.main_page_constants import MainPageConstants
from test_framework.mobile_android_core.pages.main_page.main_page import MainPage

from test_framework.mobile_android_core.pages.menu.menu_constants import MenuConstants
from test_framework.mobile_android_core.pages.menu.menu_page import MenuPage

from test_framework.mobile_android_core.utils.driver import AppiumDriver

from pathlib import Path
from test_framework.mobile_android_core.utils.try_except_decorator_mobile import try_except


class QAP_T3375(CommonTestCase):

    def __init__(self, driver: AppiumDriver, second_lvl_id=None, data_set=None, environment=None):
        super().__init__(driver, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")

    @try_except(test_id=Path(__file__).name[:-3])
    def test_context(self):
        # region - preconditions
        # endregion
        # region - test details
        # Step 1
        login_page = LoginPage(self.appium_driver)
        main_page = MainPage(self.appium_driver)
        menu_page = MenuPage(self.appium_driver)

        login_page.set_email(self.login)
        self.verify("Email Value is set correctly", "automation_mobile1, Email", login_page.get_attribute_of_element_by_xpath(LoginConstants.EMAIL, 'text'))
        # endregion

        # Step 2
        login_page.set_password(self.password)
        self.verify("Password value is set and hidden", "••••••••••••, Password", login_page.get_attribute_of_element_by_xpath(LoginConstants.PASSWORD, 'text'))
        # endregion

        # Step 3
        login_page.click_on_login_button()
        self.appium_driver.wait_time(1)
        self.verify("Login successful", None, main_page.check_if_element_presented(MainPageConstants.PORTFOLIO_TITLE))
        # endregion

        # Step 4
        main_page.click_on_menu()
        self.appium_driver.wait_time(1)
        menu_page.click_on_logout()
        self.appium_driver.wait_time(1)
        self.verify("Logout successful", None, login_page.check_if_element_presented(LoginConstants.LOGIN_TITLE))
        # endregion

        # Step 5
        login_page.login_to_mobile_trading(self.login, self.password)
        self.verify("Login successful", None, main_page.check_if_element_presented(MainPageConstants.PORTFOLIO_TITLE))
        # endregion

        # region - postconditions
        # endregion
