import time

from test_cases.web_admin.web_admin_core.pages.common_page import CommonPage
from test_cases.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_framework.web_trading.web_trading_core.pages.main_page.main_page_constants import MainPageConstants


class MainPage(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def click_on_new_workspace_button(self):
        self.find_by_xpath(MainPageConstants.PLUS_BUTTON_XPATH).click()

    def click_on_close_new_workspace_button(self):
        self.find_element_in_shadow_root(MainPageConstants.NEW_WORKSPACE_CLOSE_BUTTON_CSS)

    def click_on_buy_button(self):
        self.find_by_xpath(MainPageConstants.BUY_BUTTON_XPATH).click()

    def click_on_sell_button(self):
        self.find_by_xpath(MainPageConstants.SELL_BUTTON_XPATH).click()

    def click_on_watch_list_button(self):
        self.find_by_xpath(MainPageConstants.WATCH_LIST_BUTTON_XPATH).click()

    def click_on_order_book_button(self):
        self.find_by_xpath(MainPageConstants.ORDER_BOOK_BUTTON_XPATH).click()

    def click_on_trades_button(self):
        self.find_by_xpath(MainPageConstants.TRADES_BUTTON_XPATH).click()

    def click_on_position_button(self):
        self.find_by_xpath(MainPageConstants.POSITION_BUTTON_XPATH).click()

    def click_on_account_summary_button(self):
        self.find_by_xpath(MainPageConstants.ACCOUNT_SUMMARY_BUTTON_XPATH).click()

    def click_on_symbol_details_button(self):
        self.find_by_xpath(MainPageConstants.SYMBOL_DETAILS_BUTTON_XPATH).click()

    def click_on_notification_button(self):
        self.find_by_xpath(MainPageConstants.NOTIFICATION_BUTTON_XPATH).click()

    def click_on_menu_button(self):
        self.find_by_xpath(MainPageConstants.MENU_BUTTON_XPATH).click()
