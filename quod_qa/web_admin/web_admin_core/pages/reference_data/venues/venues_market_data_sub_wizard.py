from quod_qa.web_admin.web_admin_core.pages.common_page import CommonPage
from quod_qa.web_admin.web_admin_core.pages.reference_data.venues.venues_constants import VenuesConstants
from quod_qa.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer


class VenuesMarketDataSubWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def set_default_md_symbol(self, value):
        self.set_text_by_xpath(VenuesConstants.MARKET_DATA_TAB_DEFAULT_MD_SYMBOL_XPATH, value)

    def get_default_md_symbol(self):
        return self.get_text_by_xpath(VenuesConstants.MARKET_DATA_TAB_DEFAULT_MD_SYMBOL_XPATH)

    def set_ticker_md_symbol(self, value):
        self.set_text_by_xpath(VenuesConstants.MARKET_DATA_TAB_TICKER_MD_SYMBOL_XPATH, value)

    def get_ticker_md_symbol(self):
        return self.get_text_by_xpath(VenuesConstants.MARKET_DATA_TAB_TICKER_MD_SYMBOL_XPATH)

    def set_md_source(self, value):
        self.set_text_by_xpath(VenuesConstants.MARKET_DATA_TAB_MD_SOURCE_XPATH, value)

    def get_md_source(self):
        return self.get_text_by_xpath(VenuesConstants.MARKET_DATA_TAB_MD_SOURCE_XPATH)

    def set_trading_phase(self, value):
        self.set_combobox_value(VenuesConstants.MARKET_DATA_TAB_TRADING_PHASE_XPATH, value)

    def get_trading_phase(self):
        return self.get_text_by_xpath(VenuesConstants.MARKET_DATA_TAB_TRADING_PHASE_XPATH)

    def set_times_sales_md_symbol(self, value):
        self.set_text_by_xpath(VenuesConstants.MARKET_DATA_TAB_TIMES_SALES_MD_SYMBOL_XPATH, value)

    def get_times_sales_md_symbol(self, value):
        self.get_text_by_xpath(VenuesConstants.MARKET_DATA_TAB_TIMES_SALES_MD_SYMBOL_XPATH)

    def set_market_time_md_symbol(self, value):
        self.set_text_by_xpath(VenuesConstants.MARKET_DATA_TAB_MARKET_TIME_MD_SYMBOL_XPATH, value)

    def get_market_time_md_symbol(self):
        return self.get_text_by_xpath(VenuesConstants.MARKET_DATA_TAB_MARKET_TIME_MD_SYMBOL_XPATH)

    def set_feed_source(self, value):
        self.set_combobox_value(VenuesConstants.MARKET_DATA_TAB_FEED_SOURCE_XPATH, value)

    def get_feed_source(self):
        return self.get_text_by_xpath(VenuesConstants.MARKET_DATA_TAB_FEED_SOURCE_XPATH)

    def set_trading_status(self, value):
        self.set_combobox_value(VenuesConstants.MARKET_DATA_TAB_FEED_SOURCE_XPATH, value)

    def get_trading_status(self):
        return self.get_text_by_xpath(VenuesConstants.MARKET_DATA_TAB_TRADING_STATUS_XPATH)

    def set_news_md_symbols(self, value):
        self.set_text_by_xpath(VenuesConstants.MARKET_DATA_TAB_NEWS_MD_SYMBOLS_XPATH, value)

    def get_news_md_symbols(self):
        return self.get_text_by_xpath(VenuesConstants.MARKET_DATA_TAB_NEWS_MD_SYMBOLS_XPATH)

    def set_movers_md_symbol(self, value):
        self.set_text_by_xpath(VenuesConstants.MARKET_DATA_TAB_MOVERS_MD_SYMBOL_XPATH, value)

    def get_movers_md_symbol(self):
        return self.get_text_by_xpath(VenuesConstants.MARKET_DATA_TAB_MOVERS_MD_SYMBOL_XPATH)

    def set_trading_session(self, value):
        self.set_text_by_xpath(VenuesConstants.MARKET_DATA_TAB_TRADING_SESSION_XPATH, value)

    def get_trading_session(self):
        return self.get_text_by_xpath(VenuesConstants.MARKET_DATA_TAB_TRADING_SESSION_XPATH)
