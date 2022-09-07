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

class QAP_T3277(CommonTestCase):

    def __init__(self, driver: AppiumDriver, second_lvl_id=None, data_set=None, environment=None):
        super().__init__(driver, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")

    @try_except(test_id=Path(__file__).name[:-3])
    def test_context(self):
        # region - preconditions
        login_page = LoginPage(self.appium_driver)
        main_page = MainPage(self.appium_driver)
        menu_page = MenuPage(self.appium_driver)

        login_page.login_to_mobile_trading(self.login, self.password)
        # self.appium_driver.wait_time(2)
        self.verify("Login successful", None, main_page.wait_element_presence(MainPageConstants.PORTFOLIO_BUTTON))
        # endregion
        # region - test details

        # Step 1
        main_page.click_on_menu()
        menu_page.click_on_personal_details()
        self.verify("Personal Details is opened", None, menu_page.wait_element_presence(MenuConstants.PERSONAL_DETAILS_TITLE))
        # endregion

        # Step 2
        # endregion
        # region - postconditions
        # endregion