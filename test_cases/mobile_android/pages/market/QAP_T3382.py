import sys
import time
import traceback
from datetime import datetime

from custom import basic_custom_actions
from test_cases.mobile_android.common_test_case import CommonTestCase
from test_framework.mobile_android_core.pages.login.login_constant import LoginConstants
from test_framework.mobile_android_core.pages.login.login_page import LoginPage

from test_framework.mobile_android_core.pages.main_page.main_page_constants import MainPageConstants
from test_framework.mobile_android_core.pages.main_page.main_page import MainPage
from test_framework.mobile_android_core.pages.market.market_constants import MarketConstants
from test_framework.mobile_android_core.pages.market.market_page import MarketPage
from test_framework.mobile_android_core.pages.market.watchlists.market_watchlists_constants import \
    MarketWatchlistsConstants
from test_framework.mobile_android_core.pages.market.watchlists.market_watchlists_page import MarketWatchlistsPage

from test_framework.mobile_android_core.pages.menu.menu_constants import MenuConstants
from test_framework.mobile_android_core.pages.menu.menu_page import MenuPage

from test_framework.mobile_android_core.utils.driver import AppiumDriver

from pathlib import Path
from test_framework.mobile_android_core.utils.try_except_decorator_mobile import try_except

class QAP_T3382(CommonTestCase):

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
        market_page = MarketPage(self.appium_driver)
        market_watchlists_page = MarketWatchlistsPage(self.appium_driver)

        login_page.login_to_mobile_trading(self.login, self.password)
        self.verify("Precondition - Login successful", None, main_page.wait_element_presence(MainPageConstants.PORTFOLIO_BUTTON))
        # endregion
        # region - test details

        # Step 1
        main_page.click_on_market()
        self.verify("Step 1 - Market menu is opened", None, main_page.wait_element_presence(MarketConstants.MARKET_TITLE))
        # endregion

        # Step 2
        market_page.click_market_plus_button()
        self.verify("Step 2 - Watchlists sub-menu is opened", None, market_watchlists_page.wait_element_presence(MarketWatchlistsConstants.MARKET_WATCHLISTS_TITLE))
        # endregion

        # Step 3
        market_watchlists_page.delete_watchlist("Watchlist 1")
        self.verify("Step 3 - Watchlist is deleted", False, market_watchlists_page.get_watchlist_exist("Watchlist 1"))
        # endregion

        # Step 4
        market_watchlists_page.create_watchlist()
        self.verify('''Step 4 - "Watchlist 1" is created''', True, market_watchlists_page.get_watchlist_exist("Watchlist 1"))
        # endregion

        # Step 5
        market_watchlists_page.click_watchlist("Watchlist 1")
        self.verify('''Step 5 - Watchlist is in edit mode''', True, market_watchlists_page.get_edit_watchlist_exist())
        # endregion

        # Step 6
        market_watchlists_page.clear_watchlist()
        market_watchlists_page.set_watchlist_name("Watchlist Test")
        market_watchlists_page.click_keyboard("Enter")
        self.verify('''Step 6 - "Watchlist Test" is created''', True,
                    market_watchlists_page.get_watchlist_exist("Watchlist Test"))
        # endregion

        # Step 7
        market_watchlists_page.click_watchlist("Watchlist Test")
        self.verify('''Step 7 - Watchlist is in edit mode''', True, market_watchlists_page.get_edit_watchlist_exist())
        # endregion

        # Step 8
        market_watchlists_page.clear_watchlist()
        market_watchlists_page.set_watchlist_name("Watchlist123")
        market_watchlists_page.click_outside_watchlist()
        self.verify('''Step 8 - "Watchlist Test" is renamed''', True,
                    market_watchlists_page.get_watchlist_exist("Watchlist123"))
        # endregion

        # region - postconditions
        market_watchlists_page.delete_watchlist("Watchlist123")
        self.verify('''Postconditions - "Watchlist123" is deleted''', False,
                    market_watchlists_page.get_watchlist_exist("Watchlist Test"))
        # endregion