from appium_flutter_finder import FlutterElement, FlutterFinder

from test_cases.mobile_android.common_test_case import CommonTestCase
from test_framework.mobile_android_core.utils.common_page import CommonPage
from test_framework.mobile_android_core.pages.login.login_page import LoginPage
from test_framework.mobile_android_core.pages.login.login_constant import LoginConstants
from test_framework.mobile_android_core.pages.main_page.main_page import MainPage
from test_framework.mobile_android_core.pages.main_page.main_page_constants import MainPageConstants
from test_framework.mobile_android_core.pages.user_profile.user_profile_page import UserProfilePage
from test_framework.mobile_android_core.pages.user_profile.user_profile_constants import UserProfileConstants
from test_framework.mobile_android_core.utils.driver import AppiumDriver

from pathlib import Path
from test_framework.mobile_android_core.utils.decorators.try_except_decorator_mobile import try_except
import time

class QAP_T3375(CommonTestCase):

    def __init__(self, driver: AppiumDriver, report_id=None, data_set=None, environment=None):
        super().__init__(driver, self.__class__.__name__, report_id, data_set=data_set,
                         environment=environment)
        self.appium_driver = driver
        self.user1 = self.data_set.get_user("user_1")
        self.password1 = self.data_set.get_password("password_1")

    @try_except(test_id=Path(__file__).name[:-3])
    def test_context(self):
        # region - preconditions
        # region - test details

        # Step 1
        login_page = LoginPage(self.appium_driver)
        login_page.enter_data_field_username(self.user1)
        self.verify("Step 1 - User1_Email is set in Email field",
                    self.user1,
                    login_page.get_text_field_username())
        # endregion

        # Step 2
        login_page.enter_data_field_password(self.password1)
        self.verify("Step 2 - User1_Password is set in Email field",
                    self.password1,
                    login_page.get_text_field_password())
        # endregion

        # Step 3
        login_page.click_button_login()
        main_page = MainPage(self.appium_driver)
        self.verify("Step 3 - User1 is logged in. Main Page is shown",
                    True,
                    main_page.is_element_presented(MainPageConstants.buttonUserProfile))
        # endregion

        # Step 4
        main_page.click_button_user_profile()
        user_profile_page = UserProfilePage(self.appium_driver)
        self.verify("Step 4 - User1 is logged in. Main Page is shown",
                    True,
                    user_profile_page.is_element_presented(UserProfileConstants.buttonLogout))
        # endregion

        # Step 5
        user_profile_page.click_button_logout()
        self.verify("Step 5 - User1 is logged out. Login Page is shown",
                    True,
                    login_page.is_element_presented(LoginConstants.buttonLogin))
        # endregion

        # Step 6
        login_page.login_to_application(self.user1, self.password1)
        self.verify("Step 6 - User1 is logged in. Main Page is shown",
                    True,
                    main_page.is_element_presented(MainPageConstants.buttonUserProfile))
        # endregion

        # region - postconditions
        # endregion
