from test_framework.mobile_android_core.pages.main_page.main_page_constants import MainPageConstants
from test_framework.mobile_android_core.utils.common_page import CommonPage
from test_framework.mobile_android_core.utils.driver import AppiumDriver


class MainPage(CommonPage):
    def __init__(self, driver: AppiumDriver):
        super().__init__(driver)

    def click_on_market(self):
        self.find_by_xpath(MainPageConstants.MARKET_BUTTON).click()

    def click_on_portfolio(self):
        self.find_by_xpath(MainPageConstants.PORTFOLIO_BUTTON).click()

    def click_on_orders(self):
        self.find_by_xpath(MainPageConstants.ORDERS_BUTTON).click()

    def click_on_news(self):
        self.find_by_xpath(MainPageConstants.NEWS_BUTTON).click()

    def click_on_create_new_order(self):
        self.find_by_xpath(MainPageConstants.NEW_ORDER_BUTTON).click()

    def click_on_menu(self):
        self.find_by_xpath(MainPageConstants.MENU_BUTTON).click()
