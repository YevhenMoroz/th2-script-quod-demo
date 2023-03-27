from test_cases.mobile_android.common_test_case import CommonTestCase
from test_framework.mobile_android_core.pages.login.login_constant import LoginConstants
from test_framework.mobile_android_core.pages.login.login_page import LoginPage

from test_framework.mobile_android_core.pages.main_page.main_page_constants import MainPageConstants
from test_framework.mobile_android_core.pages.main_page.main_page import MainPage

from test_framework.mobile_android_core.pages.menu.menu_constants import MenuConstants
from test_framework.mobile_android_core.pages.menu.menu_page import MenuPage

from test_framework.mobile_android_core.utils.driver import AppiumDriver

from pathlib import Path
from test_framework.mobile_android_core.utils.decorators.try_except_decorator_mobile import try_except

class QAP_T3456(CommonTestCase):

    def __init__(self, driver: AppiumDriver, second_lvl_id=None, data_set=None, environment=None):
        super().__init__(driver, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login1 = self.data_set.get_user("user_1")
        self.password1 = self.data_set.get_password("password_1")
        self.user1_personal_details = self.data_set.get_user_personal_details("user_1")

    @try_except(test_id=Path(__file__).name[:-3])
    def test_context(self):
        # region - preconditions
        login_page = LoginPage(self.appium_driver)
        main_page = MainPage(self.appium_driver)
        menu_page = MenuPage(self.appium_driver)

        login_page.login_to_mobile_trading(self.login1, self.password1)
        self.verify("Precondition - Login successful", None, main_page.wait_element_presence(MainPageConstants.PORTFOLIO_BUTTON))
        # endregion

        # region - test details

        # Step 1
        main_page.click_on_menu()
        self.verify("Step 1 - User Profile is displayed", None, menu_page.wait_element_presence(MenuConstants.USER_PROFILE_TITLE))
        # endregion

        # Step 2
        self.verify(f'Step 2 - {self.user1_personal_details["FirstName"]} {self.user1_personal_details["LastName"]}', None,
                    menu_page.wait_element_presence(f'//android.view.View[@content-desc="{self.user1_personal_details["FirstName"]} {self.user1_personal_details["LastName"]}"]'))
        # endregion

        # Step 3
        menu_page.click_pd_go_back()
        self.verify("Step 3 - User Profile closed", None, main_page.wait_element_presence(MainPageConstants.PORTFOLIO_BUTTON))
        # endregion

        # Step 4
        main_page.click_on_menu()
        self.verify("Step 4 - User Profile is displayed", None,
                    menu_page.wait_element_presence(MenuConstants.USER_PROFILE_TITLE))
        # endregion

        # Step 5
        menu_page.click_on_logout()
        self.verify("Step 5 - Logout successful", None, login_page.wait_element_presence(LoginConstants.LOGIN_TITLE))
        # endregion

        # region - postconditions
        # endregion