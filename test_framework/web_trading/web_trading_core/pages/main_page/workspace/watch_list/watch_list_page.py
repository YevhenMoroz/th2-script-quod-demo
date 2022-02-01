from test_cases.web_admin.web_admin_core.pages.common_page import CommonPage
from test_cases.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer


class WatchListPage(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    # TODO: implement methods, if something changed in FE part, please take a look

    # region Filter values in main page
    def get_symbol(self):
        pass

    def get_last_trend(self):
        pass

    def get_bid_qty(self):
        pass

    def get_ask(self):
        pass

    def get_ask_qty(self):
        pass

    def get_trade(self):
        pass

    def get_open_px(self):
        pass

    def get_closing_px(self):
        pass

    def get_high_px(self):
        pass

    def get_low_px(self):
        pass

    def get_trade_volume(self):
        pass

    def get_open_interest(self):
        pass

    # endregion

    # region Visible columns
    def click_on_field_chooser_button(self):
        pass

    def select_visible_columns(self, value):
        pass

    def click_on_hide_all(self):
        pass

    def click_on_show_all(self):
        pass

    # endregion

    # region Advanced filtering
    def click_on_advanced_filtering_button(self):
        pass

    # endregion

    def set_search_symbol(self, value):
        pass

    def click_on_traded_listings_switch(self):
        pass

    def click_on_copy_panel_button(self):
        pass

    def click_on_maximize_button(self):
        pass

    def click_on_minimize_button(self):
        pass

    def click_on_close_watch_list_button(self):
        pass

    # region Auxiliary menu on the symbol

    def click_on_buy_button(self):
        pass

    def click_on_sell_button(self):
        pass

    def click_on_market_depth_button(self):
        pass

    def click_on_times_and_sales_button(self):
        pass
# endregion

#TODO: pay attention!
    def horizontal_scroll(self):
        pass