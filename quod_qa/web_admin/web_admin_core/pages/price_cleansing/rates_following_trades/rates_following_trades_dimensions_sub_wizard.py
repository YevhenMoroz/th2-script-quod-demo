from quod_qa.web_admin.web_admin_core.pages.common_page import CommonPage
from quod_qa.web_admin.web_admin_core.pages.price_cleansing.rates_following_trades.rates_following_trades_constants import \
    RatesFollowingTradesConstants

from quod_qa.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer


class RatesFollowingTradesDimensionsSubWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def set_venue(self, value):
        self.set_combobox_value(RatesFollowingTradesConstants.DIMENSIONS_TAB_VENUE_XPATH, value)

    def get_venue(self):
        return self.get_text_by_xpath(RatesFollowingTradesConstants.DIMENSIONS_TAB_VENUE_XPATH)

    def set_listing(self, value):
        self.set_text_by_xpath(RatesFollowingTradesConstants.DIMENSIONS_TAB_LISTING_XPATH, value)

    def get_listing(self):
        return self.get_text_by_xpath(RatesFollowingTradesConstants.DIMENSIONS_TAB_LISTING_XPATH)

    def set_instr_type(self, value):
        self.set_combobox_value(RatesFollowingTradesConstants.DIMENSIONS_TAB_INSTR_TYPE_XPATH, value)

    def get_instr_type(self):
        return self.get_text_by_xpath(RatesFollowingTradesConstants.DIMENSIONS_TAB_INSTR_TYPE_XPATH)

    def set_symbol(self, value):
        self.set_combobox_value(RatesFollowingTradesConstants.DIMENSIONS_TAB_SYMBOL_XPATH, value)

    def get_symbol(self):
        return self.get_text_by_xpath(RatesFollowingTradesConstants.DIMENSIONS_TAB_SYMBOL_XPATH)
