from quod_qa.web_admin.web_admin_core.pages.common_page import CommonPage
from quod_qa.web_admin.web_admin_core.pages.reference_data.listings.listings_constants import ListingsConstants
from quod_qa.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer


class ListingsMarketIdentifiersSubWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def set_source(self, value):
        self.set_text_by_xpath(ListingsConstants.MARKET_DATA_TAB_SOURCE_XPATH, value)

    def set_security_id(self,value):
        self.set_text_by_xpath(ListingsConstants.MARKET_IDENTIFIERS_TAB_SECURITY_ID_XPATH,value)

    def get_security_id(self):
        return self.get_text_by_xpath(ListingsConstants.MARKET_IDENTIFIERS_TAB_SECURITY_ID_XPATH)

    def set_sedol_id(self, value):
        self.set_text_by_xpath(ListingsConstants.MARKET_IDENTIFIERS_TAB_SEDOL_ID_XPATH, value)

    def get_sedol_id(self):
        return self.get_text_by_xpath(ListingsConstants.MARKET_IDENTIFIERS_TAB_SEDOL_ID_XPATH)

    def set_ric_id(self, value):
        self.set_text_by_xpath(ListingsConstants.MARKET_IDENTIFIERS_TAB_RIC_ID_XPATH, value)

    def get_ric_id(self):
        return self.get_text_by_xpath(ListingsConstants.MARKET_IDENTIFIERS_TAB_RIC_ID_XPATH)

    def set_cta_id(self, value):
        self.set_text_by_xpath(ListingsConstants.MARKET_IDENTIFIERS_TAB_CTA_ID_XPATH, value)

    def get_cta_id(self):
        return self.get_text_by_xpath(ListingsConstants.MARKET_IDENTIFIERS_TAB_CTA_ID_XPATH)

    def set_dutch_id(self, value):
        self.set_text_by_xpath(ListingsConstants.MARKET_IDENTIFIERS_TAB_DUTCH_ID_XPATH, value)

    def get_dutch_id(self):
        return self.get_text_by_xpath(ListingsConstants.MARKET_IDENTIFIERS_TAB_DUTCH_ID_XPATH)

    def set_belgian_id(self, value):
        self.set_text_by_xpath(ListingsConstants.MARKET_IDENTIFIERS_TAB_BELGIAN_ID_XPATH, value)

    def get_belgian_id(self):
        return self.get_text_by_xpath(ListingsConstants.MARKET_IDENTIFIERS_TAB_BELGIAN_ID_XPATH)

    def set_isda_id(self, value):
        self.set_text_by_xpath(ListingsConstants.MARKET_IDENTIFIERS_TAB_ISDA_ID_XPATH, value)

    def get_isda_id(self):
        return self.get_text_by_xpath(ListingsConstants.MARKET_IDENTIFIERS_TAB_ISDA_ID_XPATH)

    def set_interactive_data_id(self, value):
        self.set_text_by_xpath(ListingsConstants.MARKET_IDENTIFIERS_TAB_INTERACTIVE_DATA_ID_XPATH, value)

    def get_interactive_data_id(self):
        return self.get_text_by_xpath(ListingsConstants.MARKET_IDENTIFIERS_TAB_INTERACTIVE_DATA_ID_XPATH)

    def set_security_id_source(self, value):
        self.set_text_by_xpath(ListingsConstants.MARKET_IDENTIFIERS_TAB_SECURITY_ID_SOURCE_XPATH, value)

    def get_security_id_source(self):
        return self.get_text_by_xpath(ListingsConstants.MARKET_IDENTIFIERS_TAB_SECURITY_ID_SOURCE_XPATH)

    def set_quik_id(self, value):
        self.set_text_by_xpath(ListingsConstants.MARKET_IDENTIFIERS_TAB_QUIK_ID_XPATH, value)

    def get_quik_id(self):
        return self.get_text_by_xpath(ListingsConstants.MARKET_IDENTIFIERS_TAB_QUIK_ID_XPATH)

    def set_iso_id(self, value):
        self.set_text_by_xpath(ListingsConstants.MARKET_IDENTIFIERS_TAB_ISO_ID_XPATH, value)

    def get_iso_id(self):
        return self.get_text_by_xpath(ListingsConstants.MARKET_IDENTIFIERS_TAB_ISO_ID_XPATH)

    def set_bloomberg_id(self, value):
        self.set_text_by_xpath(ListingsConstants.MARKET_IDENTIFIERS_TAB_BLOOMBERG_ID_XPATH, value)

    def get_bloomberg_id(self):
        return self.get_text_by_xpath(ListingsConstants.MARKET_IDENTIFIERS_TAB_BLOOMBERG_ID_XPATH)

    def set_valoren_id(self, value):
        self.set_text_by_xpath(ListingsConstants.MARKET_IDENTIFIERS_TAB_VALOREN_ID_XPATH, value)

    def get_valoren_id(self):
        return self.get_text_by_xpath(ListingsConstants.MARKET_IDENTIFIERS_TAB_VALOREN_ID_XPATH)

    def set_common_id(self, value):
        self.set_text_by_xpath(ListingsConstants.MARKET_IDENTIFIERS_TAB_COMMON_ID_XPATH, value)

    def get_common_id(self):
        return self.get_text_by_xpath(ListingsConstants.MARKET_IDENTIFIERS_TAB_COMMON_ID_XPATH)

    def set_option_prc_reporting_auth_id(self, value):
        self.set_text_by_xpath(ListingsConstants.MARKET_IDENTIFIERS_TAB_OPTION_PRC_REPORTING_AUTH__ID_XPATH, value)

    def get_option_prc_reporting_auth_id(self):
        return self.get_text_by_xpath(ListingsConstants.MARKET_IDENTIFIERS_TAB_OPTION_PRC_REPORTING_AUTH__ID_XPATH)

    def set_market_data_key_id(self, value):
        self.set_text_by_xpath(ListingsConstants.MARKET_IDENTIFIERS_TAB_MARKET_DATA_KEY_ID_XPATH, value)

    def get_market_data_key_id(self):
        return self.get_text_by_xpath(ListingsConstants.MARKET_IDENTIFIERS_TAB_MARKET_DATA_KEY_ID_XPATH)

    def set_cusip_id(self, value):
        self.set_text_by_xpath(ListingsConstants.MARKET_IDENTIFIERS_TAB_CUSIP_ID_XPATH, value)

    def get_cusip_id(self):
        return self.get_text_by_xpath(ListingsConstants.MARKET_IDENTIFIERS_TAB_CUSIP_ID_XPATH)

    def set_isin_id(self, value):
        self.set_text_by_xpath(ListingsConstants.MARKET_IDENTIFIERS_TAB_ISIN_ID_XPATH, value)

    def get_isin_id(self):
        return self.get_text_by_xpath(ListingsConstants.MARKET_IDENTIFIERS_TAB_ISIN_ID_XPATH)

    def set_exchange_symbol_id(self, value):
        self.set_text_by_xpath(ListingsConstants.MARKET_IDENTIFIERS_TAB_EXCHANGE_SYMBOL_ID_XPATH, value)

    def get_exchange_symbol_id(self):
        return self.get_text_by_xpath(ListingsConstants.MARKET_IDENTIFIERS_TAB_EXCHANGE_SYMBOL_ID_XPATH)

    def set__id(self, value):
        self.set_text_by_xpath(ListingsConstants.MARKET_IDENTIFIERS_TAB_WERTPAPIER_ID_XPATH, value)

    def get_wertpapier_id(self):
        return self.get_text_by_xpath(ListingsConstants.MARKET_IDENTIFIERS_TAB_WERTPAPIER_ID_XPATH)

    def set_sicovam_id(self, value):
        self.set_text_by_xpath(ListingsConstants.MARKET_IDENTIFIERS_TAB_SICOVAM_ID_XPATH, value)

    def get_sicovam_id(self):
        return self.get_text_by_xpath(ListingsConstants.MARKET_IDENTIFIERS_TAB_SICOVAM_ID_XPATH)

    def set_clearing_id(self, value):
        self.set_text_by_xpath(ListingsConstants.MARKET_IDENTIFIERS_TAB_CLEARING_ID_XPATH, value)

    def get_clearing_id(self):
        return self.get_text_by_xpath(ListingsConstants.MARKET_IDENTIFIERS_TAB_CLEARING_ID_XPATH)

    def set_gl_trade_id(self, value):
        self.set_text_by_xpath(ListingsConstants.MARKET_IDENTIFIERS_TAB_GL_TRADE_ID_XPATH, value)

    def get_gl_trade_id(self):
        return self.get_text_by_xpath(ListingsConstants.MARKET_IDENTIFIERS_TAB_GL_TRADE_ID_XPATH)

