from test_cases.mobile_android.common_test_case import CommonTestCase
from test_framework.mobile_android_core.pages.login.login_page import LoginPage

from test_framework.mobile_android_core.pages.main_page.main_page_constants import MainPageConstants
from test_framework.mobile_android_core.pages.main_page.main_page import MainPage
from test_framework.mobile_android_core.pages.market.market_constants import MarketConstants
from test_framework.mobile_android_core.pages.market.market_page import MarketPage
from test_framework.mobile_android_core.pages.market.watchlists.market_watchlists_constants import \
    MarketWatchlistsConstants
from test_framework.mobile_android_core.pages.market.watchlists.market_watchlists_page import MarketWatchlistsPage

from test_framework.mobile_android_core.pages.menu.menu_page import MenuPage

from test_framework.mobile_android_core.utils.driver import AppiumDriver

from pathlib import Path
from test_framework.mobile_android_core.utils.decorators.try_except_decorator_mobile import try_except

class QAP_T3384(CommonTestCase):

    def __init__(self, driver: AppiumDriver, second_lvl_id=None, data_set=None, environment=None):
        super().__init__(driver, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.instrument_1 = self.data_set.get_instrument("instrument_1")

    @try_except(test_id=Path(__file__).name[:-3])
    def test_context(self):
        # region - preconditions
        login_page = LoginPage(self.appium_driver)
        main_page = MainPage(self.appium_driver)
        market_page = MarketPage(self.appium_driver)
        menu_page = MenuPage(self.appium_driver)
        market_watchlists_page = MarketWatchlistsPage(self.appium_driver)

        login_page.login_to_mobile_trading(self.login, self.password)
        self.verify("Precondition - Login successful", None, main_page.wait_element_presence(MainPageConstants.PORTFOLIO_BUTTON))
        # endregion
        # region - test details

        # Step 1
        main_page.click_on_market()
        self.verify("Step 1 - Market menu is opened", None, market_page.wait_element_presence(MarketConstants.MARKET_TITLE))
        # endregion

        # Step 2
        market_page.add_new_instrument(instrument=self.instrument_1)
        self.verify(f"Step 2 - {self.instrument_1} is displayed", True,
                    market_page.get_element_exists_by_xpath(market_page.get_instrument_xpath(self.instrument_1)))
        # endregion


        # Step 3
        market_page.click_search_field()
        market_page.set_search(self.instrument_1)
        self.verify(f"Step 3 - {self.instrument_1} is shown in Search results",
                    None,
                    market_page.wait_element_presence(market_page.get_instrument_xpath(self.instrument_1)))
        # endregion

        # Step 4
        market_page.click_instrument_by_search_result(self.instrument_1)
        self.verify(f"Step 4 - {self.instrument_1} is displayed", True,
                    market_page.get_element_exists_by_xpath(market_page.get_instrument_xpath(self.instrument_1)))
        self.verify(f"Step 4 - {self.instrument_1} is NOT doubled", 1, market_page.get_count_of_elements_by_xpath(market_page.get_instrument_xpath(self.instrument_1)))
        rect = market_page.find_by_xpath(market_page.get_instrument_xpath(self.instrument_1)).rect
        # endregion

        # Step 5
        market_page.click_on_menu()
        menu_page.click_on_logout()
        login_page.login_to_mobile_trading(self.login, self.password)
        main_page.click_on_market()
        self.verify("Step 5 - Market menu is opened", None,
                    market_page.wait_element_presence(MarketConstants.MARKET_TITLE))
        # endregion

        # Step 6
        self.verify(f"Step 6 - {self.instrument_1} is displayed", True,
                    market_page.get_element_exists_by_xpath(market_page.get_instrument_xpath(self.instrument_1)))
        self.verify(f"Step 6 - {self.instrument_1} is NOT doubled", 1,
                    market_page.get_count_of_elements_by_xpath(market_page.get_instrument_xpath(self.instrument_1)))
        self.verify(f"Step 6 - {self.instrument_1} positioning was not changed", rect, market_page.find_by_xpath(market_page.get_instrument_xpath(self.instrument_1)).rect)
        # endregion


        # region - postconditions
        market_page.click_market_plus_button()
        self.verify("Postconditions - Watchlists sub-menu is opened", None, market_watchlists_page.wait_element_presence(MarketWatchlistsConstants.MARKET_WATCHLISTS_TITLE))
        market_watchlists_page.delete_watchlist("Watchlist 1")
        self.verify('''Postconditions - "Watchlist 1" is deleted''', False,
                    market_watchlists_page.get_watchlist_exist("Watchlist 1"))
        # endregion