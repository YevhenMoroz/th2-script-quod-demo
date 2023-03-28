from test_framework.mobile_android_core.pages.user_profile.user_profile_constants import UserProfileConstants
from test_framework.mobile_android_core.utils.common_page import CommonPage
from test_framework.mobile_android_core.utils.driver import AppiumDriver


class UserProfilePage(CommonPage):
    def __init__(self, driver: AppiumDriver):
        """
        class contains generic methods for communication with elements located on User Profile Page
        """
        super().__init__(driver)

    # region account
    def click_button_logout(self):
        """
        click on Logout button
        """
        self.tap(UserProfileConstants.buttonLogout)