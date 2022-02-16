from test_framework.mobile_android_core.pages.menu.menu_constants import MenuConstants
from test_framework.mobile_android_core.utils.common_page import CommonPage
from test_framework.mobile_android_core.utils.driver import AppiumDriver


class MenuPage(CommonPage):
    def __init__(self, driver: AppiumDriver):
        super().__init__(driver)

    # region account
    def click_on_trade_preferences(self):
        self.find_by_xpath(MenuConstants.TRADE_PREFERENCES_BUTTON).click()

    def click_on_logout(self):
        self.find_by_xpath(MenuConstants.LOGOUT_BUTTON).click()

    # endregion

    # region Trade Preferences

    def set_default_client(self):
        pass

    def get_default_client(self):
        pass

     #TODO: need to create one constant for that, currently incorrect xpath
    def click_on_go_back_button(self):
        pass
    # endregion
