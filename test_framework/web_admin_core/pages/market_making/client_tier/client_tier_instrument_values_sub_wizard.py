from test_framework.web_admin_core.pages.common_page import CommonPage
from test_framework.web_admin_core.pages.market_making.client_tier.client_tier_constants import \
    ClientTierConstants
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer


class ClientTierInstrumentValuesSubWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def set_symbol(self, value):
        self.set_combobox_value(ClientTierConstants.CLIENT_TIER_INSTRUMENTS_VALUES_TAB_SYMBOL_XPATH, value)

    def get_symbol(self):
        return self.get_text_by_xpath(ClientTierConstants.CLIENT_TIER_INSTRUMENTS_VALUES_TAB_SYMBOL_XPATH)

    def is_symbol_filed_contains_asterisk_symbol(self):
        label = self.find_by_xpath(ClientTierConstants.CLIENT_TIER_INSTRUMENTS_VALUES_TAB_SYMBOL_LABEL_XPATH).text
        return True if '*' in label else False

    def set_rfq_response_stream_ttl(self, value):
        self.set_text_by_xpath(ClientTierConstants.CLIENT_TIER_INSTRUMENTS_VALUES_TAB_RFQ_RESPONSE_TTL_XPATH,
                               value)

    def get_rfq_response_stream_ttl(self):
        return self.get_text_by_xpath(ClientTierConstants.CLIENT_TIER_INSTRUMENTS_VALUES_TAB_RFQ_RESPONSE_TTL_XPATH)

    def set_core_spot_price_strategy(self, value):
        self.set_combobox_value(ClientTierConstants.CLIENT_TIER_VALUES_TAB_CORE_SPOT_PRICE_STRATEGY_XPATH, value)

    def get_core_spot_price_strategy(self):
        return self.get_text_by_xpath(ClientTierConstants.CLIENT_TIER_VALUES_TAB_CORE_SPOT_PRICE_STRATEGY_XPATH)

    def set_tod_end_time(self, value):
        self.set_text_by_xpath(ClientTierConstants.CLIENT_TIER_VALUES_TAB_TOD_END_TIME, value)
