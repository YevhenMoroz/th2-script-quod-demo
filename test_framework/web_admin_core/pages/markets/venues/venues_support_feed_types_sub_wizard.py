from test_framework.web_admin_core.pages.common_page import CommonPage
from test_framework.web_admin_core.pages.markets.venues.venues_constants import VenuesConstants
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer


class VenuesSupportFeedTypesSubWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def click_on_status(self):
        self.find_by_xpath(VenuesConstants.SUPPORT_FEED_TYPES_TAB_STATUS_CHECKBOX_XPATH).click()

    def is_status_selected(self):
        return self.is_checkbox_selected(VenuesConstants.SUPPORT_FEED_TYPES_TAB_STATUS_CHECKBOX_XPATH)

    def click_on_quote(self):
        self.find_by_xpath(VenuesConstants.SUPPORT_FEED_TYPES_TAB_QUOTE_CHECKBOX_XPATH).click()

    def is_quote_selected(self):
        return self.is_checkbox_selected(VenuesConstants.SUPPORT_FEED_TYPES_TAB_QUOTE_CHECKBOX_XPATH)

    def click_on_quote_book(self):
        self.find_by_xpath(VenuesConstants.SUPPORT_FEED_TYPES_TAB_QUOTE_BOOK_CHECKBOX_XPATH).click()

    def is_quote_book_selected(self):
        return self.is_checkbox_selected(VenuesConstants.SUPPORT_FEED_TYPES_TAB_QUOTE_BOOK_CHECKBOX_XPATH)

    def click_on_tickers(self):
        self.find_by_xpath(VenuesConstants.SUPPORT_FEED_TYPES_TAB_TICKERS_CHECKBOX_XPATH).click()

    def is_tickers_selected(self):
        return self.is_checkbox_selected(VenuesConstants.SUPPORT_FEED_TYPES_TAB_TICKERS_CHECKBOX_XPATH)

    def click_on_market_time(self):
        self.find_by_xpath(VenuesConstants.SUPPORT_FEED_TYPES_TAB_MARKET_TIME_CHECKBOX_XPATH).click()

    def is_market_time_selected(self):
        return self.is_checkbox_selected(VenuesConstants.SUPPORT_FEED_TYPES_TAB_MARKET_TIME_CHECKBOX_XPATH)

    def click_on_discretion_inst(self):
        self.find_by_xpath(VenuesConstants.SUPPORT_FEED_TYPES_TAB_DISCRETION_INST_CHECKBOX_XPATH).click()

    def is_discretion_inst_selected(self):
        return self.is_checkbox_selected(VenuesConstants.SUPPORT_FEED_TYPES_TAB_DISCRETION_INST_CHECKBOX_XPATH)

    def click_on_broker_queue(self):
        self.find_by_xpath(VenuesConstants.SUPPORT_FEED_TYPES_TAB_BROKER_QUEUE_CHECKBOX_XPATH).click()

    def is_broker_queue(self):
        return self.is_checkbox_selected(VenuesConstants.SUPPORT_FEED_TYPES_TAB_BROKER_QUEUE_CHECKBOX_XPATH)

    def click_on_market_depth(self):
        self.find_by_xpath(VenuesConstants.SUPPORT_FEED_TYPES_TAB_MARKET_DEPTH_CHECKBOX_XPATH).click()

    def is_market_depth_selected(self):
        self.is_checkbox_selected(VenuesConstants.SUPPORT_FEED_TYPES_TAB_MARKET_DEPTH_CHECKBOX_XPATH)

    def click_on_movers(self):
        self.find_by_xpath(VenuesConstants.SUPPORT_FEED_TYPES_TAB_MARKET_DEPTH_CHECKBOX_XPATH).click()

    def is_movers_selected(self):
        return self.is_checkbox_selected(VenuesConstants.SUPPORT_FEED_TYPES_TAB_MARKET_DEPTH_CHECKBOX_XPATH)

    def click_on_news(self):
        self.find_by_xpath(VenuesConstants.SUPPORT_FEED_TYPES_TAB_NEWS_CHECKBOX_XPATH).click()

    def is_news_selected(self):
        return self.is_checkbox_selected(VenuesConstants.SUPPORT_FEED_TYPES_TAB_NEWS_CHECKBOX_XPATH)

    def click_on_term_quote_request(self):
        self.find_by_xpath(VenuesConstants.SUPPORT_FEED_TYPES_TAB_TERM_QUOTE_REQUEST_CHECKBOX_XPATH).click()

    def is_term_quote_request_selected(self):
        return self.is_checkbox_selected(VenuesConstants.SUPPORT_FEED_TYPES_TAB_TERM_QUOTE_REQUEST_CHECKBOX_XPATH)

    def click_on_quote_cancel(self):
        self.find_by_xpath(VenuesConstants.SUPPORT_FEED_TYPES_TAB_QUOTE_CANCEL_CHECKBOX_XPATH).click()

    def is_quote_cancel_selected(self):
        self.is_checkbox_selected(VenuesConstants.SUPPORT_FEED_TYPES_TAB_QUOTE_CANCEL_CHECKBOX_XPATH)

    def click_on_intraday(self):
        self.find_by_xpath(VenuesConstants.SUPPORT_FEED_TYPES_TAB_INTRADAY_CHECKBOX_XPATH).click()

    def is_intraday_selected(self):
        return self.is_checkbox_selected(VenuesConstants.SUPPORT_FEED_TYPES_TAB_INTRADAY_CHECKBOX_XPATH)

    def click_on_order_book(self):
        self.find_by_xpath(VenuesConstants.SUPPORT_FEED_TYPES_TAB_ORDER_BOOK_CHECKBOX_XPATH).click()

    def is_order_book_selected(self):
        return self.is_checkbox_selected(VenuesConstants.SUPPORT_FEED_TYPES_TAB_ORDER_BOOK_CHECKBOX_XPATH)

    def click_on_times_and_sales(self):
        self.find_by_xpath(VenuesConstants.SUPPORT_FEED_TYPES_TAB_TIMES_AND_SALES_CHECKBOX_XPATH).click()

    def is_times_and_sales_selected(self):
        return self.is_checkbox_selected(VenuesConstants.SUPPORT_FEED_TYPES_TAB_TIMES_AND_SALES_CHECKBOX_XPATH)

    def click_on_trade(self):
        self.find_by_xpath(VenuesConstants.SUPPORT_FEED_TYPES_TAB_TRADE_CHECKBOX_XPATH).click()

    def is_trade_selected(self):
        return self.is_checkbox_selected(VenuesConstants.SUPPORT_FEED_TYPES_TAB_TRADE_CHECKBOX_XPATH)

    def click_on_sized_md_request(self):
        self.find_by_xpath(VenuesConstants.SUPPORT_FEED_TYPES_TAB_SIZED_MD_REQUEST_CHECKBOX_XPATH).click()

    def is_sized_md_request_selected(self):
        return self.is_checkbox_selected(VenuesConstants.SUPPORT_FEED_TYPES_TAB_SIZED_MD_REQUEST_CHECKBOX_XPATH)
