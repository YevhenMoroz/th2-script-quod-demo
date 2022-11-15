from test_framework.web_admin_core.pages.common_page import CommonPage
from test_framework.web_admin_core.pages.markets.listings.listings_constants import ListingsConstants
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer


class ListingsValidationsSubWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def set_price_limit_profile(self, value):
        self.set_combobox_value(ListingsConstants.VALIDATIONS_TAB_PRICE_LIMIT_XPATH, value)

    def get_price_limit_profile(self):
        return self.get_text_by_xpath(ListingsConstants.VALIDATIONS_TAB_PRICE_LIMIT_XPATH)

    def set_min_trade_vol(self, value):
        self.set_text_by_xpath(ListingsConstants.VALIDATIONS_TAB_MIN_TRADE_VOL_XPATH, value)

    def get_min_trade_vol(self):
        return self.get_text_by_xpath(ListingsConstants.VALIDATIONS_TAB_MIN_TRADE_VOL_XPATH)

    def set_previous_total_traded_qty(self, value):
        self.set_text_by_xpath(ListingsConstants.VALIDATIONS_TAB_PREVIOUS_TOTAL_TRADED_QTY_XPATH, value)

    def get_previous_total_traded_qty(self):
        return self.get_text_by_xpath(ListingsConstants.VALIDATIONS_TAB_PREVIOUS_TOTAL_TRADED_QTY_XPATH)

    def set_pre_trade_lis_qty(self, value):
        self.set_text_by_xpath(ListingsConstants.VALIDATIONS_TAB_PRE_TRADE_LIS_QTY_XPATH, value)

    def get_pre_trade_lis_qty(self):
        return self.get_text_by_xpath(ListingsConstants.VALIDATIONS_TAB_PRE_TRADE_LIS_QTY_XPATH)

    def set_tick_size_profile(self, value):
        self.set_combobox_value(ListingsConstants.VALIDATIONS_TAB_TICK_SIZE_PROFILE_XPATH, value)

    def get_tick_size_profile(self):
        return self.get_text_by_xpath(ListingsConstants.VALIDATIONS_TAB_TICK_SIZE_PROFILE_XPATH)

    def set_max_trade_vol(self, value):
        self.set_text_by_xpath(ListingsConstants.VALIDATIONS_TAB_MAX_TRADE_VOL_XPATH, value)

    def get_max_trade_vol(self):
        return self.get_text_by_xpath(ListingsConstants.VALIDATIONS_TAB_MAX_TRADE_VOL_XPATH)

    def set_max_spread(self, value):
        self.set_text_by_xpath(ListingsConstants.VALIDATIONS_TAB_MAX_SPREAD_XPATH, value)

    def get_max_spread(self):
        return self.get_text_by_xpath(ListingsConstants.VALIDATIONS_TAB_MAX_SPREAD_XPATH)

    def set_previous_close_price(self, value):
        self.set_text_by_xpath(ListingsConstants.VALIDATIONS_TAB_PREVIOUS_CLOSE_PRICE_XPATH, value)

    def get_previous_close_price(self):
        return self.get_text_by_xpath(ListingsConstants.VALIDATIONS_TAB_PREVIOUS_CLOSE_PRICE_XPATH)

    def set_round_lot(self, value):
        self.set_text_by_xpath(ListingsConstants.VALIDATIONS_TAB_ROUND_LOT_XPATH, value)

    def get_round_lot(self):
        return self.get_text_by_xpath(ListingsConstants.VALIDATIONS_TAB_ROUND_LOT_XPATH)

    def click_on_manage_price_limit_profile(self):
        self.find_by_xpath(ListingsConstants.VALIDATIONS_TAB_MANAGE_PRICE_LIMIT_PROFILE_XPATH).click()

    def click_on_manage_tick_size_profile(self):
        self.find_by_xpath(ListingsConstants.VALIDATIONS_TAB_TICK_SIZE_PROFILE_XPATH).click()

