from test_framework.mobile_android_core.pages.main_page.main_page_constants import MainPageConstants
from test_framework.mobile_android_core.utils.common_page import CommonPage
from test_framework.mobile_android_core.utils.driver import AppiumDriver


class MainPage(CommonPage):
    def __init__(self, driver: AppiumDriver):
        """
        class contains generic methods for communication with elements located on Login Page
        """
        super().__init__(driver)

    def click_button_user_profile(self):
        """
        click userProfile button
        """
        self.tap(MainPageConstants.buttonUserProfile)

