from test_cases.mobile_android.common_test_case import CommonTestCase
from test_framework.mobile_android_core.pages.login.login_page import LoginPage

from test_framework.mobile_android_core.pages.main_page.main_page_constants import MainPageConstants
from test_framework.mobile_android_core.pages.main_page.main_page import MainPage
from test_framework.mobile_android_core.pages.market.market_constants import MarketConstants
from test_framework.mobile_android_core.pages.market.market_page import MarketPage
from test_framework.mobile_android_core.pages.market.watchlists.market_watchlists_constants import \
    MarketWatchlistsConstants
from test_framework.mobile_android_core.pages.market.watchlists.market_watchlists_page import MarketWatchlistsPage

from test_framework.mobile_android_core.utils.driver import AppiumDriver

from pathlib import Path
from test_framework.mobile_android_core.utils.decorators.try_except_decorator_mobile import try_except

class QAP_T3381(CommonTestCase):

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
        self.verify("Step 3 - Watchlist 1 is deleted", False, market_watchlists_page.get_watchlist_exist("Watchlist 1"))
        # endregion

        # Step 4
        market_watchlists_page.create_watchlist()
        market_watchlists_page.create_watchlist()
        self.verify('''Step 4 - "Watchlist 1" is created''', True,
                    market_watchlists_page.get_watchlist_exist("Watchlist 1"))
        self.verify('''Step 4 - "Watchlist 2" is created''', True,
                    market_watchlists_page.get_watchlist_exist("Watchlist 2"))
        # endregion

        # Step 5
        market_watchlists_page.reorder_watchlist("Watchlist 1", 1)
        self.verify("Step 5 - Watchlist are ordered: 2→1", "Watchlist 2 is upper", market_watchlists_page.compare_watchlists_positioning("Watchlist 2", "Watchlist 1"))
        # endregion

        # Step 6 and 7
        market_watchlists_page.delete_watchlist("Watchlist 2")
        self.verify("Step 6 and 7 - Watchlist 2 is deleted", False, market_watchlists_page.get_watchlist_exist("Watchlist 2"))
        self.verify("Step 6 and 7 - Watchlist 1 is shown", True,
                    market_watchlists_page.get_watchlist_exist("Watchlist 1"))
        # endregion

        # region - postconditions
        market_watchlists_page.delete_watchlist("Watchlist 1")
        self.verify('''Postconditions - "Watchlist 1" is deleted''', False,
                    market_watchlists_page.get_watchlist_exist("Watchlist 1"))
        # endregion