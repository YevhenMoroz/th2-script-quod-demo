import time

from test_framework.web_admin_core.pages.common_page import CommonPage
from test_framework.web_admin_core.pages.risk_limits.cum_trading_limit_counters.constants import \
    CumTradingLimitCountersConstants
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer


class CumTradingLimitCountersWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def click_on_close(self):
        self.find_by_xpath(CumTradingLimitCountersConstants.CLOSE_WIZARD_XPATH).click()

    def click_on_save_changes(self):
        self.find_by_xpath(CumTradingLimitCountersConstants.SAVE_CHANGES_BUTTON_XPATH).click()

    def click_on_revert_changes(self):
        self.find_by_xpath(CumTradingLimitCountersConstants.REVERT_CHANGES_XPATH).click()

    def click_on_go_back(self):
        self.find_by_xpath(CumTradingLimitCountersConstants.GO_BACK_BUTTON_XPATH).click()

    def click_download_pdf_entity_button_and_check_pdf(self, value):
        self.clear_download_directory()
        self.find_by_xpath(CumTradingLimitCountersConstants.DOWNLOAD_PDF_BUTTON_XPATH).click()
        time.sleep(2)
        return self.is_pdf_contains_value(value)

    def is_incorrect_or_missing_value_message_displayed(self):
        if self.find_by_xpath(
                CumTradingLimitCountersConstants.INCORRECT_OR_MISSING_VALUES_XPATH).text == "Incorrect or missing values":
            return True
        else:
            return False

    def set_cum_trading_limit(self, value):
        self.set_combobox_value(CumTradingLimitCountersConstants.WIZARD_CUM_TRADING_LIMIT_XPATH, value)

    def get_cum_trading_limit(self):
        return self.get_text_by_xpath(CumTradingLimitCountersConstants.WIZARD_CUM_TRADING_LIMIT_XPATH)

    def get_all_cum_trading_limit_from_drop_menu(self):
        self.set_text_by_xpath(CumTradingLimitCountersConstants.WIZARD_CUM_TRADING_LIMIT_XPATH, "")
        time.sleep(1)
        return self.get_all_items_from_drop_down(CumTradingLimitCountersConstants.DROP_DOWN_MENU)

    def set_cum_buy_ord_qty(self, value):
        self.set_text_by_xpath(CumTradingLimitCountersConstants.WIZARD_CUM_BUY_ORD_QTY_XPATH, value)

    def get_cum_buy_ord_qty(self):
        return self.get_text_by_xpath(CumTradingLimitCountersConstants.WIZARD_CUM_BUY_ORD_QTY_XPATH)

    def set_cum_ord_amt(self, value):
        self.set_text_by_xpath(CumTradingLimitCountersConstants.WIZARD_CUM_ORD_AMT_XPATH, value)

    def get_cum_ord_amt(self):
        return self.get_text_by_xpath(CumTradingLimitCountersConstants.WIZARD_CUM_ORD_AMT_XPATH)

    def set_cum_sell_ord_qty(self, value):
        self.set_text_by_xpath(CumTradingLimitCountersConstants.WIZARD_CUM_SELL_ORD_QTY_XPATH, value)

    def get_cum_sell_ord_qty(self):
        return self.get_text_by_xpath(CumTradingLimitCountersConstants.WIZARD_CUM_SELL_ORD_QTY_XPATH)

    def set_cum_buy_ord_amt(self, value):
        self.set_text_by_xpath(CumTradingLimitCountersConstants.WIZARD_CUM_BUY_ORD_AMT_XPATH, value)

    def get_cum_buy_ord_amt(self):
        return self.get_text_by_xpath(CumTradingLimitCountersConstants.WIZARD_CUM_BUY_ORD_AMT_XPATH)

    def set_cum_ord_qty(self, value):
        self.set_text_by_xpath(CumTradingLimitCountersConstants.WIZARD_CUM_ORD_QTY_XPATH, value)

    def get_cum_ord_qty(self):
        return self.get_text_by_xpath(CumTradingLimitCountersConstants.WIZARD_CUM_ORD_QTY_XPATH)

    def set_cum_sell_ord_amt(self, value):
        self.set_text_by_xpath(CumTradingLimitCountersConstants.WIZARD_CUM_SELL_ORD_AMT_XPATH, value)

    def get_sell_ord_amt(self):
        return self.get_text_by_xpath(CumTradingLimitCountersConstants.WIZARD_CUM_SELL_ORD_AMT_XPATH)

    def set_cum_leaves_ord_amt(self, value):
        self.set_text_by_xpath(CumTradingLimitCountersConstants.WIZARD_CUM_LEAVES_ORD_AMT_XPATH, value)

    def get_cum_leaves_ord_amt(self):
        return self.get_text_by_xpath(CumTradingLimitCountersConstants.WIZARD_CUM_LEAVES_ORD_AMT_XPATH)
