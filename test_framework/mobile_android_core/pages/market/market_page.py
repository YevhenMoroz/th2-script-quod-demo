from test_framework.mobile_android_core.pages.market.market_constants import MarketConstants
from test_framework.mobile_android_core.utils.common_page import CommonPage
from test_framework.mobile_android_core.utils.driver import AppiumDriver


class MarketPage(CommonPage):
    def __init__(self, driver: AppiumDriver):
        super().__init__(driver)

    # region market

    def click_market_plus_button(self, count=1):
        self.tap_by_coordinates(MarketConstants.MARKET_PLUS_BUTTON_X, MarketConstants.MARKET_PLUS_BUTTON_Y, count)

