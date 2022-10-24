import time

from test_framework.web_admin_core.pages.common_page import CommonPage
from test_framework.web_admin_core.pages.risk_limits.cum_trading_limits.cum_trading_limits_constants import \
    CumTradingLimitsConstants
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer


class CumTradingLimitsValuesSubWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def set_description(self, value):
        self.set_text_by_xpath(CumTradingLimitsConstants.VALUES_TAB_DESCRIPTION_XPATH, value)

    def get_description(self):
        return self.get_text_by_xpath(CumTradingLimitsConstants.VALUES_TAB_DESCRIPTION_XPATH)

    def set_external_id(self, value):
        self.set_text_by_xpath(CumTradingLimitsConstants.VALUES_TAB_EXTERNAL_ID_XPATH, value)

    def get_external_id(self):
        return self.get_text_by_xpath(CumTradingLimitsConstants.VALUES_TAB_EXTERNAL_ID_XPATH)

    def set_currency(self, value):
        self.set_combobox_value(CumTradingLimitsConstants.VALUES_TAB_CURRENCY_XPATH, value)

    def get_currency(self):
        return self.get_text_by_xpath(CumTradingLimitsConstants.VALUES_TAB_CURRENCY_XPATH)

    def get_all_currency_from_drop_menu(self):
        self.set_text_by_xpath(CumTradingLimitsConstants.VALUES_TAB_CURRENCY_XPATH, "")
        time.sleep(1)
        return self.get_all_items_from_drop_down(CumTradingLimitsConstants.DROP_DOWN_MENU_XPATH)

    def set_max_quantity(self, value):
        self.set_text_by_xpath(CumTradingLimitsConstants.VALUES_TAB_MAX_QUANTITY_XPATH, value)

    def get_max_quantity(self):
        return self.get_text_by_xpath(CumTradingLimitsConstants.VALUES_TAB_MAX_QUANTITY_XPATH)

    def set_soft_max_quantity(self, value):
        self.set_text_by_xpath(CumTradingLimitsConstants.VALUES_TAB_SOFT_MAX_QTY_XPATH, value)

    def get_soft_max_quantity(self):
        return self.get_text_by_xpath(CumTradingLimitsConstants.VALUES_TAB_SOFT_MAX_QTY_XPATH)

    def set_max_amount(self, value):
        self.set_text_by_xpath(CumTradingLimitsConstants.VALUES_TAB_MAX_AMOUNT_XPATH, value)

    def get_max_amount(self):
        return self.get_text_by_xpath(CumTradingLimitsConstants.VALUES_TAB_MAX_AMOUNT_XPATH)

    def set_soft_max_amt(self, value):
        self.set_text_by_xpath(CumTradingLimitsConstants.VALUES_TAB_SOFT_MAX_AMT_XPATH, value)

    def get_soft_max_amt(self):
        return self.get_text_by_xpath(CumTradingLimitsConstants.VALUES_TAB_SOFT_MAX_AMT_XPATH)

    def set_max_buy_qty(self, value):
        self.set_text_by_xpath(CumTradingLimitsConstants.VALUES_TAB_MAX_BUY_QTY_XPATH, value)

    def get_max_buy_qty(self):
        return self.get_text_by_xpath(CumTradingLimitsConstants.VALUES_TAB_MAX_BUY_QTY_XPATH)

    def set_soft_max_buy_qty(self, value):
        self.set_text_by_xpath(CumTradingLimitsConstants.VALUES_TAB_SOFT_MAX_BUY_QTY_XPATH, value)

    def get_soft_max_buy_qty(self):
        return self.get_text_by_xpath(CumTradingLimitsConstants.VALUES_TAB_SOFT_MAX_BUY_QTY_XPATH)

    def set_max_buy_amt(self, value):
        self.set_text_by_xpath(CumTradingLimitsConstants.VALUES_TAB_MAX_BUY_AMT_XPATH, value)

    def get_max_buy_amt(self):
        return self.get_text_by_xpath(CumTradingLimitsConstants.VALUES_TAB_MAX_BUY_AMT_XPATH)

    def set_soft_buy_amt(self, value):
        self.set_text_by_xpath(CumTradingLimitsConstants.VALUES_TAB_SOFT_MAX_BUY_AMT_XPATH, value)

    def get_soft_buy_amt(self):
        return self.get_text_by_xpath(CumTradingLimitsConstants.VALUES_TAB_SOFT_MAX_BUY_AMT_XPATH)

    def set_soft_max_buy_amt(self, value):
        self.set_text_by_xpath(CumTradingLimitsConstants.VALUES_TAB_SOFT_MAX_BUY_AMT_XPATH, value)

    def get_soft_max_buy_amt(self):
        return self.get_text_by_xpath(CumTradingLimitsConstants.VALUES_TAB_SOFT_MAX_BUY_AMT_XPATH)

    def set_max_sell_qty(self, value):
        self.set_text_by_xpath(CumTradingLimitsConstants.VALUES_TAB_MAX_SELL_QTY_XPATH, value)

    def get_max_sell_qty(self):
        return self.get_text_by_xpath(CumTradingLimitsConstants.VALUES_TAB_MAX_SELL_QTY_XPATH)

    def set_soft_max_sell_qty(self, value):
        self.set_text_by_xpath(CumTradingLimitsConstants.VALUES_TAB_SOFT_MAX_SELL_QTY_XPATH, value)

    def get_soft_max_sell_qty(self):
        return self.get_text_by_xpath(CumTradingLimitsConstants.VALUES_TAB_SOFT_MAX_SELL_QTY_XPATH)

    def set_max_sell_amt(self, value):
        self.set_text_by_xpath(CumTradingLimitsConstants.VALUES_TAB_MAX_SELL_AMT_XPATH, value)

    def get_max_sell_amt(self):
        return self.get_text_by_xpath(CumTradingLimitsConstants.VALUES_TAB_MAX_SELL_AMT_XPATH)

    def set_soft_max_sell_amt(self, value):
        self.set_text_by_xpath(CumTradingLimitsConstants.VALUES_TAB_SOFT_MAX_SELL_AMT_XPATH, value)

    def get_soft_max_sell_amt(self):
        return self.get_text_by_xpath(CumTradingLimitsConstants.VALUES_TAB_SOFT_MAX_SELL_AMT_XPATH)

    def set_max_open_order_amount(self, value):
        self.set_text_by_xpath(CumTradingLimitsConstants.VALUES_TAB_MAX_OPEN_ORDER_AMOUNT_XPATH, value)

    def get_max_open_order_amount(self):
        return self.get_text_by_xpath(CumTradingLimitsConstants.VALUES_TAB_MAX_OPEN_ORDER_AMOUNT_XPATH)

    def clear_currency(self, value):
        self.set_text_by_xpath(CumTradingLimitsConstants.VALUES_TAB_CURRENCY_XPATH, value)
