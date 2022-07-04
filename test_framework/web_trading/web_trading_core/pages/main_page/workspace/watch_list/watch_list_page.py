from selenium.webdriver import ActionChains

from test_framework.web_admin_core.pages.common_page import CommonPage
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_framework.web_trading.web_trading_core.pages.main_page.workspace.watch_list.watch_list_constants import \
    WatchListConstants


class WatchListPage(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    # TODO: implement methods, if something changed in FE part, please take a look

    # region Filter values in main page
    def get_symbol(self):
        return self.find_by_xpath(WatchListConstants.ORDER_SYMBOL_XPATH).text

    def get_last_trend(self):
        return self.find_by_xpath(WatchListConstants.ORDER_LAST_TREND_XPATH).text

    def get_bid_qty(self):
        return self.find_by_xpath(WatchListConstants.ORDER_BID_QTY_XPATH).text

    def get_bid(self):
        return self.find_by_xpath(WatchListConstants.ORDER_BID_XPATH).text

    def get_ask(self):
        return self.find_by_xpath(WatchListConstants.ORDER_ASK_XPATH).text

    def get_ask_qty(self):
        return self.find_by_xpath(WatchListConstants.ORDER_ASK_QTY_XPATH).text

    def get_trade(self):
        return self.find_by_xpath(WatchListConstants.ORDER_TRADE_XPATH).text

    def get_open_px(self):
        return self.find_by_xpath(WatchListConstants.ORDER_OPENPX_XPATH).text

    def get_closing_px(self):
        return self.find_by_xpath(WatchListConstants.ORDER_CLOSINGPX_XPATH).text

    def get_high_px(self):
        return self.find_by_xpath(WatchListConstants.ORDER_HIGHPX_XPATH).text

    def get_low_px(self):
        return self.find_by_xpath(WatchListConstants.ORDER_LOWPX_XPATH).text

    def get_trade_volume(self):
        return self.find_by_xpath(WatchListConstants.ORDER_TRADE_VOLUME_XPATH).text

    def get_open_interest(self):
        return self.find_by_xpath(WatchListConstants.ORDER_OPEN_INTEREST_XPATH).text

    def get_simulated_sell_price(self):
        return self.find_by_xpath(WatchListConstants.ORDER_SIMULATED_SELL_PRICE_XPATH).text

    def get_simulated_buy_price(self):
        return self.find_by_xpath(WatchListConstants.ORDER_SIMULATED_BUY_PRICE_XPATH).text

    def get_margin_rate(self):
        return self.find_by_xpath(WatchListConstants.ORDER_MARGIN_RATE_XPATH).text

    def get_mid_price(self):
        return self.find_by_xpath(WatchListConstants.ORDER_MID_PRICE_XPATH).text

    def get_settle_high_price(self):
        return self.find_by_xpath(WatchListConstants.ORDER_SETTLE_HIGH_PRICE_XPATH).text

    def get_prior_settle_price(self):
        return self.find_by_xpath(WatchListConstants.ORDER_PRIOR_SETTLE_PRICE_XPATH).text

    def get_prior_settle_price_price(self):
        return self.find_by_xpath(WatchListConstants.ORDER_PRIOR_SETTLE_PRICEPRICE_XPATH).text

    def get_session_high_bid(self):
        return self.find_by_xpath(WatchListConstants.ORDER_SESSION_HIGH_BID_XPATH).text

    def get_session_low_offer(self):
        return self.find_by_xpath(WatchListConstants.ORDER_SESSION_LOW_OFFER_XPATH).text

    def get_auction_price(self):
        return self.find_by_xpath(WatchListConstants.ORDER_AUCTION_PRICE_XPATH).text

    def get_fixing_price(self):
        return self.find_by_xpath(WatchListConstants.ORDER_FIXING_PRICE_XPATH).text

    def get_cash_rate(self):
        return self.find_by_xpath(WatchListConstants.ORDER_CASH_RATE_XPATH).text

    def get_recovery_rate(self):
        return self.find_by_xpath(WatchListConstants.ORDER_RECOVERY_RATE_XPATH).text

    # endregion

    # region Visible columns
    def click_on_field_chooser_button(self):
        self.find_by_xpath(WatchListConstants.FIELD_CHOOSER_XPATH).click()

    def select_visible_columns(self, value):
        self.set_checkbox_list(WatchListConstants.LIST_CHECKBOX_XPATH, value)

    def click_on_hide_all(self):
        self.find_by_xpath(WatchListConstants.HIDE_ALL_BUTTON_XPATH).click()

    def click_on_show_all(self):
        self.find_by_xpath(WatchListConstants.SHOW_ALL_BUTTON_XPATH).click()

    # endregion

    # region Advanced filtering
    def click_on_advanced_filtering_button(self):
        self.find_by_xpath(WatchListConstants.ADVANCED_FILTERING_BUTTON_XPATH).click()

    # endregion

    def set_search_symbol(self, value):
        self.set_text_by_xpath(WatchListConstants.SEARCH_SYMBOL_INPUT_XPATH, value)

    def click_on_traded_listings_switch(self):
        self.find_by_xpath(WatchListConstants.TRADED_LISTINGS_BUTTON_XPATH).click()

    def click_on_copy_panel_button(self):
        self.find_by_xpath(WatchListConstants.COPY_PANEL_BUTTON_XPATH).click()

    def click_on_maximize_button(self):
        self.find_element_in_shadow_root(WatchListConstants.MAXIMIZE_BUTTON_CSS)

    def click_on_minimize_button(self):
        self.find_element_in_shadow_root(WatchListConstants.MINIMIZE_BUTTON_CSS)

    def click_on_close_watch_list_button(self):
        self.find_element_in_shadow_root(WatchListConstants.CLOSE_BUTTON_CSS)

    # region Auxiliary menu on the symbol

    def click_on_buy_button(self):
        self.find_by_xpath(WatchListConstants.BUY_HOVER_BUTTON_XPATH).click()

    def click_on_sell_button(self):
        self.find_by_xpath(WatchListConstants.SELL_HOVER_BUTTON_XPATH).click()

    def click_on_market_depth_button(self):
        self.find_by_xpath(WatchListConstants.MARKET_DEPTH_HOVER_BUTTON_XPATH).click()

    def click_on_times_and_sales_button(self):
        self.find_by_xpath(WatchListConstants.TIMES_AND_SALES_HOVER_BUTTON_XPATH).click()

    # endregion

    def offset_horizontal_slide(self):
        slider = self.find_by_xpath(WatchListConstants.HORIZONTAL_SCROLL_XPATH)
        action = ActionChains(self.web_driver_container.get_driver())
        action.drag_and_drop_by_offset(slider, 200, 0).perform()
