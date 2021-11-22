from test_cases.web_admin.web_admin_core.pages.common_page import CommonPage
from test_cases.web_admin.web_admin_core.pages.reference_data.listings.listings_constants import ListingsConstants
from test_cases.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer


class ListingsMarketDataSubWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def set_source(self, value):
        self.set_text_by_xpath(ListingsConstants.MARKET_DATA_TAB_SOURCE_XPATH, value)

    def get_source(self):
        return self.get_text_by_xpath(ListingsConstants.MARKET_DATA_TAB_SOURCE_XPATH)

    def set_news_symbol(self, value):
        self.set_text_by_xpath(ListingsConstants.MARKET_DATA_TAB_NEWS_SYMBOL_XPATH, value)

    def get_news_symbol(self):
        return self.get_text_by_xpath(ListingsConstants.MARKET_DATA_TAB_NEWS_SYMBOL_XPATH)

    def set_quote_symbol(self, value):
        self.set_text_by_xpath(ListingsConstants.MARKET_DATA_TAB_QUOTE_SYMBOL_XPATH, value)

    def get_quote_symbol(self):
        return self.get_text_by_xpath(ListingsConstants.MARKET_DATA_TAB_QUOTE_SYMBOL_XPATH)

    def set_market_depth_symbol(self, value):
        self.set_text_by_xpath(ListingsConstants.MARKET_DATA_TAB_MARKET_DEPTH_SYMBOL_XPATH, value)

    def get_market_depth_symbol(self):
        return self.get_text_by_xpath(ListingsConstants.MARKET_DATA_TAB_MARKET_DEPTH_SYMBOL_XPATH)

    def set_default_md_symbol(self, value):
        self.set_text_by_xpath(ListingsConstants.MARKET_DATA_TAB_DEFAULT_MD_SYMBOL_XPATH, value)

    def get_default_md_symbol(self):
        return self.get_text_by_xpath(ListingsConstants.MARKET_DATA_TAB_DEFAULT_MD_SYMBOL_XPATH)

    def set_trade_symbol(self, value):
        self.set_text_by_xpath(ListingsConstants.MARKET_DATA_TAB_TRADE_SYMBOL_XPATH, value)

    def get_trade_symbol(self):
        return self.get_text_by_xpath(ListingsConstants.MARKET_DATA_TAB_TRADE_SYMBOL_XPATH)

    def set_quote_book_symbol(self, value):
        self.set_text_by_xpath(ListingsConstants.MARKET_DATA_TAB_QUOTE_BOOK_SYMBOL_XPATH, value)

    def get_quote_book_symbol(self):
        return self.get_text_by_xpath(ListingsConstants.MARKET_DATA_TAB_QUOTE_BOOK_SYMBOL_XPATH)

    def set_order_book_symbol(self, value):
        self.set_text_by_xpath(ListingsConstants.MARKET_DATA_TAB_ORDER_BOOK_SYMBOL_XPATH, value)

    def get_order_book_symbol(self):
        return self.get_text_by_xpath(ListingsConstants.MARKET_DATA_TAB_ORDER_BOOK_SYMBOL_XPATH)

    def set_standard_market_size(self, value):
        self.set_text_by_xpath(ListingsConstants.MARKET_DATA_TAB_STANDARD_MARKET_SIZE_XPATH, value)

    def get_standard_market_size(self):
        return self.get_text_by_xpath(ListingsConstants.MARKET_DATA_TAB_STANDARD_MARKET_SIZE_XPATH)

    def set_status_symbol(self, value):
        self.set_text_by_xpath(ListingsConstants.MARKET_DATA_TAB_STATUS_SYMBOL_XPATH, value)

    def get_status_symbol(self):
        return self.get_text_by_xpath(ListingsConstants.MARKET_DATA_TAB_STATUS_SYMBOL_XPATH)

    def set_intraday_symbol(self, value):
        self.set_text_by_xpath(ListingsConstants.MARKET_DATA_TAB_INTRADAY_SYMBOL_XPATH, value)

    def get_intraday_symbol(self):
        return self.get_text_by_xpath(ListingsConstants.MARKET_DATA_TAB_INTRADAY_SYMBOL_XPATH)
