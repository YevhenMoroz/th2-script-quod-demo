from test_framework.web_admin_core.pages.common_page import CommonPage
from test_framework.web_admin_core.pages.markets.venues.venues_constants import VenuesConstants
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer


class VenuesDefaultSubWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def set_prefered_listing(self, value):
        self.set_text_by_xpath(VenuesConstants.DEFAULT_TAB_PREFERED_LISTING_XPATH, value)

    def get_prefered_listing(self):
        return self.get_text_by_xpath(VenuesConstants.DEFAULT_TAB_PREFERED_LISTING_XPATH)

    def set_quotereq_res_time(self, value):
        self.set_text_by_xpath(VenuesConstants.DEFAULT_TAB_QUOTEREQ_RES_TIME_XPATH, value)

    def get_quotereq_res_time(self):
        return self.get_text_by_xpath(VenuesConstants.DEFAULT_TAB_QUOTEREQ_RES_TIME_XPATH)

    def set_quote_msg_id_format(self, value):
        self.set_text_by_xpath(VenuesConstants.DEFAULT_TAB_QUOTE_MSG_ID_FORMAT_XPATH, value)

    def get_quote_msg_id_format(self):
        return self.get_text_by_xpath(VenuesConstants.DEFAULT_TAB_QUOTE_MSG_ID_FORMAT_XPATH)

    def set_trade_report_id_format(self, value):
        self.set_text_by_xpath(VenuesConstants.DEFAULT_TAB_TRADE_REPORT_ID_FORMAT_XPATH, value)

    def get_trade_report_id_format(self):
        self.get_text_by_xpath(VenuesConstants.DEFAULT_TAB_TRADE_REPORT_ID_FORMAT_XPATH)

    def set_quote_side_responce_level(self, value):
        self.set_combobox_value(VenuesConstants.DEFAULT_TAB_QUOTE_SIDE_RESPONCE_LEVEL_XPATH, value)

    def get_quote_side_responce_level(self):
        return self.get_text_by_xpath(VenuesConstants.DEFAULT_TAB_QUOTE_SIDE_RESPONCE_LEVEL_XPATH)

    def click_on_support_broken_date_feed(self):
        self.find_by_xpath(VenuesConstants.DEFAULT_TAB_SUPPORT_BROKEN_DATE_FEED_CHECKBOX_XPATH).click()

    def is_support_broken_date_feed(self):
        return self.is_checkbox_selected(VenuesConstants.DEFAULT_TAB_SUPPORT_BROKEN_DATE_FEED_CHECKBOX_XPATH)

    def set_quote_ttl(self, value):
        self.set_text_by_xpath(VenuesConstants.DEFAULT_TAB_QUOTE_TTL_XPATH, value)

    def get_quote_ttl(self):
        return self.get_text_by_xpath(VenuesConstants.DEFAULT_TAB_QUOTE_TTL_XPATH)

    def set_clquotereq_id_format(self, value):
        self.set_text_by_xpath(VenuesConstants.DEFAULT_TAB_CLQUOTEREQ_ID_FORMAT_XPATH, value)

    def get_clquotereq_id_format(self):
        return self.get_text_by_xpath(VenuesConstants.DEFAULT_TAB_CLQUOTEREQ_ID_FORMAT_XPATH)

    def set_clord_id_format(self, value):
        self.set_text_by_xpath(VenuesConstants.DEFAULT_TAB_CLORD_ID_FORMAT_XPATH, value)

    def get_clord_id_format(self):
        return self.get_text_by_xpath(VenuesConstants.DEFAULT_TAB_CLORD_ID_FORMAT_XPATH)

    def set_default_settl_type(self, value):
        self.set_combobox_value(VenuesConstants.DEFAULT_TAB_DEFAULT_SETTL_TYPE_XPATH, value)

    def get_default_settl_type(self):
        self.get_text_by_xpath(VenuesConstants.DEFAULT_TAB_DEFAULT_SETTL_TYPE_XPATH)

    def click_on_generate_bid_id(self):
        self.find_by_xpath(VenuesConstants.DEFAULT_TAB_GENERATE_BID_ID_CHECKBOX_XPATH).click()

    def is_generate_bid_id_selected(self):
        self.is_checkbox_selected(VenuesConstants.DEFAULT_TAB_GENERATE_BID_ID_CHECKBOX_XPATH)

    def set_quotereq_ttl(self, value):
        self.set_text_by_xpath(VenuesConstants.DEFAULT_TAB_QUOTEREQ_TTL_XPATH, value)

    def get_quotereq_ttl(self):
        return self.get_text_by_xpath(VenuesConstants.DEFAULT_TAB_QUOTEREQ_TTL_XPATH)

    def set_legref_id_format(self, value):
        self.set_text_by_xpath(VenuesConstants.DEFAULT_TAB_LEGREF_ID_FORMAT_XPATH, value)

    def get_legref_id_format(self):
        return self.get_text_by_xpath(VenuesConstants.DEFAULT_TAB_LEGREF_ID_FORMAT_XPATH)

    def set_client_quote_id_format(self, value):
        self.set_text_by_xpath(VenuesConstants.DEFAULT_TAB_CLIENT_QUOTE_ID_FORMAT_XPATH, value)

    def get_client_quote_id_format(self):
        self.get_text_by_xpath(VenuesConstants.DEFAULT_TAB_CLIENT_QUOTE_ID_FORMAT_XPATH)

    def set_default_settl_currency(self, value):
        self.set_combobox_value(VenuesConstants.DEFAULT_TAB_DEFAULT_SETTL_CURRENCY_XPATH, value)

    def get_default_settl_currency(self):
        return self.get_text_by_xpath(VenuesConstants.DEFAULT_TAB_DEFAULT_SETTL_CURRENCY_XPATH)

    def click_on_generate_quote_id(self):
        self.find_by_xpath(VenuesConstants.DEFAULT_TAB_GENERATE_QUOTE_ID_CHECKBOX_XPATH).click()

    def is_generate_quote_id_selected(self):
        self.is_checkbox_selected(VenuesConstants.DEFAULT_TAB_GENERATE_QUOTE_ID_CHECKBOX_XPATH)
