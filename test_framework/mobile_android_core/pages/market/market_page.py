from test_framework.mobile_android_core.pages.market.market_constants import MarketConstants
from test_framework.mobile_android_core.utils.common_page import CommonPage
from test_framework.mobile_android_core.utils.driver import AppiumDriver


class MarketPage(CommonPage):
    def __init__(self, driver: AppiumDriver):
        super().__init__(driver)

    # region market
    def click_on_menu(self):
        self.find_by_xpath(MarketConstants.MENU_BUTTON).click()

    def click_market_plus_button(self, count=1):
        self.tap_by_coordinates(MarketConstants.MARKET_PLUS_BUTTON_X, MarketConstants.MARKET_PLUS_BUTTON_Y, count)

    def delete_instrument(self, name):
        pass

    def click_watchlist(self, name):
        self.get_watchlist_xpath(name).click()

    def click_search_field(self):
        self.find_by_xpath(MarketConstants.MARKET_SEARCH_FIELD).click()

    def click_in_search(self):
        pass

    def set_search(self, name=''):
        self.find_by_xpath(MarketConstants.SEARCH_FIELD).send_keys(name)

    def clear_search_input(self):
        pass

    def click_clear_button(self):
        pass

    def click_instrument_by_search_result(self, name):
        self.get_instrument_element_by_name(name).click()

    def get_watchlist_element_by_name(self, name):
        return self.find_by_xpath(self.get_watchlist_xpath(name))

    def get_watchlist_xpath(self, name):
        return MarketConstants.WATCHLIST_NAME_START + name + MarketConstants.WATCHLIST_NAME_END

    def get_instrument_element_by_name(self, name):
        return self.find_by_xpath(self.get_instrument_xpath(name))

    def get_instrument_xpath(self, name):
        return MarketConstants.INSTRUMENT_START + name + MarketConstants.INSTRUMENT_END

    def add_new_instrument(self, watchlist=None, instrument=''):
        if watchlist != None:
            self.click_watchlist(watchlist)
        self.click_search_field()
        self.set_search(instrument)
        self.click_instrument_by_search_result(instrument)

    def reorder_instrument(self, instrument, direction=1):
        instrument_params = self.get_instrument_element_by_name(instrument).rect
        self.reorder_by_coordinates(instrument_params['x'] + instrument_params['width'] - 1,
                                    instrument_params['y'] + instrument_params['height'] / 2,
                                    instrument_params['x'] + instrument_params['width'] - 1,
                                    instrument_params['y'] + instrument_params['height'] * (direction + 0.5))

    def compare_instruments(self, firstInstrument, secondInstrument):
        firstInstrument_params = self.get_instrument_element_by_name(firstInstrument).rect
        secondInstrument_params = self.get_instrument_element_by_name(secondInstrument).rect
        if firstInstrument_params['y'] < secondInstrument_params['y']:
            return f"{firstInstrument} is upper"
        else:
            return f"{firstInstrument} is lower"

    def delete_instrument_from_watchlist(self, watchlist=None, instrument=''):
        if watchlist != None:
            self.click_watchlist(watchlist)
        instrument_params = self.get_instrument_element_by_name(instrument).rect
        self.swipe_by_coordinates(instrument_params['x'] + instrument_params['width'] - 1,
                                  instrument_params['y'] + instrument_params['height'] - 1,
                                  instrument_params['x'],
                                  instrument_params['y'])
        self.tap_by_coordinates(instrument_params['x'] + instrument_params['width'] * 3 / 4,
                                instrument_params['y'] + instrument_params['height'] / 2)

    def swipe_instrument_left(self, watchlist=None, instrument=''):
        if watchlist != None:
            self.click_watchlist(watchlist)
        instrument_params = self.get_instrument_element_by_name(instrument).rect
        self.swipe_by_coordinates(instrument_params['x'] + instrument_params['width'] - 1,
                                  instrument_params['y'] + instrument_params['height'] - 1,
                                  instrument_params['x'],
                                  instrument_params['y'])

    def swipe_instrument_right(self, watchlist=None, instrument=''):
        pass