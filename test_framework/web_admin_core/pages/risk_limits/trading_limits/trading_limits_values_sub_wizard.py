import time
from test_framework.web_admin_core.pages.common_page import CommonPage
from test_framework.web_admin_core.pages.risk_limits.trading_limits.trading_limits_constants import \
    TradingLimitsConstants

from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer


class TradingLimitsValuesSubWizardPage(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def set_description(self, value):
        self.set_text_by_xpath(TradingLimitsConstants.VALUES_TAB_DESCRIPTION_XPATH, value)

    def get_description(self):
        return self.get_text_by_xpath(TradingLimitsConstants.VALUES_TAB_DESCRIPTION_XPATH)

    def set_external_id(self, value):
        self.set_text_by_xpath(TradingLimitsConstants.VALUES_TAB_EXTERNAL_ID_XPATH, value)

    def get_external_id(self):
        return self.get_text_by_xpath(TradingLimitsConstants.VALUES_TAB_EXTERNAL_ID_XPATH)

    def set_currency(self, value):
        self.set_combobox_value(TradingLimitsConstants.VALUES_TAB_CURRENCY_XPATH, value)

    def get_currency(self):
        return self.get_text_by_xpath(TradingLimitsConstants.VALUES_TAB_CURRENCY_XPATH)

    def get_all_currency_from_drop_menu(self):
        self.set_text_by_xpath(TradingLimitsConstants.VALUES_TAB_CURRENCY_XPATH, "")
        time.sleep(1)
        return self.get_all_items_from_drop_down(TradingLimitsConstants.DROP_DOWN_MENU_XPATH)

    def set_max_quantity(self, value):
        self.set_text_by_xpath(TradingLimitsConstants.VALUES_TAB_MAX_QUANTITY_XPATH, value)

    def get_max_quantity(self):
        return self.get_text_by_xpath(TradingLimitsConstants.VALUES_TAB_MAX_QUANTITY_XPATH)

    def set_max_amount(self, value):
        self.set_text_by_xpath(TradingLimitsConstants.VALUES_TAB_MAX_AMOUNT_XPATH, value)

    def get_max_amount(self):
        return self.get_text_by_xpath(TradingLimitsConstants.VALUES_TAB_MAX_AMOUNT_XPATH)

    def set_max_soft_quantity(self, value):
        self.set_text_by_xpath(TradingLimitsConstants.VALUES_TAB_MAX_SOFT_QUANTITY_XPATH, value)

    def get_max_soft_quantity(self):
        return self.get_text_by_xpath(TradingLimitsConstants.VALUES_TAB_MAX_SOFT_QUANTITY_XPATH)

    def set_max_soft_amount(self, value):
        self.set_text_by_xpath(TradingLimitsConstants.VALUES_TAB_MAX_SOFT_AMOUNT_XPATH, value)

    def get_max_soft_amount(self):
        return self.get_text_by_xpath(TradingLimitsConstants.VALUES_TAB_MAX_SOFT_AMOUNT_XPATH)

    def set_min_display(self, value):
        self.set_text_by_xpath(TradingLimitsConstants.VALUES_TAB_MIN_DISPLAY_XPATH, value)

    def get_min_display(self):
        return self.get_text_by_xpath(TradingLimitsConstants.VALUES_TAB_MIN_DISPLAY_XPATH)

    def set_max_display(self, value):
        self.set_text_by_xpath(TradingLimitsConstants.VALUES_TAB_MAX_DISPLAY_XPATH, value)

    def get_max_display(self):
        return self.get_text_by_xpath(TradingLimitsConstants.VALUES_TAB_MAX_DISPLAY_XPATH)

    def set_min_display_percentage(self, value):
        self.set_text_by_xpath(TradingLimitsConstants.VALUES_TAB_MIN_DISPLAY_PERCENTAGE_XPATH, value)

    def get_min_display_percentage(self):
        return self.get_text_by_xpath(TradingLimitsConstants.VALUES_TAB_MIN_DISPLAY_PERCENTAGE_XPATH)


