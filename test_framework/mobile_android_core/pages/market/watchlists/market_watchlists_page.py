import time

from test_framework.mobile_android_core.pages.market.watchlists.market_watchlists_constants import MarketWatchlistsConstants
from test_framework.mobile_android_core.utils.common_page import CommonPage
from test_framework.mobile_android_core.utils.driver import AppiumDriver

class MarketWatchlistsPage(CommonPage):
    def __init__(self, driver: AppiumDriver):
        super().__init__(driver)

    # region watchlists

    def create_watchlist(self, count=1):
        self.tap_by_coordinates(MarketWatchlistsConstants.MARKET_WATCHLISTS_PLUS_BUTTON_X, MarketWatchlistsConstants.MARKET_WATCHLISTS_PLUS_BUTTON_Y, count)

    def delete_watchlist(self, name):
        xpath = self.get_watchlist_xpath(name)
        watchlist = self.find_by_xpath(xpath)
        watchlist_params = watchlist.rect
        self.swipe_by_coordinates(watchlist_params['x']+watchlist_params['width']-1,
                                  watchlist_params['y']+watchlist_params['height']-1,
                                  watchlist_params['x'],
                                  watchlist_params['y'])
        self.tap_by_coordinates(watchlist_params['x'] + watchlist_params['width'] - 1,
                                watchlist_params['y'] + watchlist_params['height'] - 1)

    def click_watchlist(self, name):
        self.find_by_xpath(self.get_watchlist_xpath(name)).click()

    def click_outside_watchlist(self):
        watchlist = self.find_by_xpath("//android.widget.EditText")
        watchlist_params = watchlist.rect
        self.tap_by_coordinates(1, watchlist_params['y']+watchlist_params['height']/2)

    def clear_watchlist(self):
        self.find_by_xpath('//android.widget.EditText').clear()

    def set_watchlist_name(self, newName):
        self.find_by_xpath('//android.widget.EditText').send_keys(newName)

    def get_watchlist_xpath(self, name=''):
        return f'''//android.view.View[@content-desc="{name}"]'''

    def get_watchlist_exist(self, name):
        return self.element_exists_by_xpath(self.get_watchlist_xpath(name))

    def get_edit_watchlist_xpath(self, name=''):
        if name=='':
            value = f'''Watchlist title'''
        else:
            value = f'''{name}, Watchlist title'''
        return f"//div[contains(@text, '{value}'"

    def get_edit_watchlist_exist(self, name=''):
        return self.element_exists_by_xpath('//android.widget.EditText')

    def rename_watchlist(self, oldName, newName):
        self.click_watchlist(oldName)
        self.clear_watchlist(oldName)
        self.set_watchlist_name(newName)