import time

from test_cases.web_admin.web_admin_core.pages.common_page import CommonPage
from test_cases.web_admin.web_admin_core.pages.risk_limits.cum_trading_limits.cum_trading_limits_constants import \
    CumTradingLimitsConstants

from test_cases.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer


class CumTradingLimitsPage(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def click_on_more_actions(self):
        self.find_by_xpath(CumTradingLimitsConstants.MORE_ACTIONS_XPATH).click()

    def click_on_edit(self):
        self.find_by_xpath(CumTradingLimitsConstants.EDIT_XPATH).click()

    def click_on_clone(self):
        self.find_by_xpath(CumTradingLimitsConstants.CLONE_XPATH).click()

    def click_on_delete(self, confirmation):
        self.find_by_xpath(CumTradingLimitsConstants.DELETE_XPATH).click()
        if confirmation:
            time.sleep(2)
            self.find_by_xpath(CumTradingLimitsConstants.OK_BUTTON_XPATH).click()
        else:
            self.find_by_xpath(CumTradingLimitsConstants.CANCEL_BUTTON_XPATH).click()

    def click_download_pdf_entity_button_and_check_pdf(self, value):
        self.clear_download_directory()
        self.find_by_xpath(CumTradingLimitsConstants.DOWNLOAD_PDF_BUTTON_XPATH).click()
        time.sleep(2)
        return self.is_pdf_contains_value(value)

    def click_on_pin_row(self):
        self.find_by_xpath(CumTradingLimitsConstants.PIN_ROW_XPATH).click()

    def click_on_new(self):
        self.find_by_xpath(CumTradingLimitsConstants.NEW_BUTTON_XPATH).click()

    def click_on_user_icon(self):
        self.find_by_xpath(CumTradingLimitsConstants.USER_ICON_AT_RIGHT_CORNER).click()

    def click_on_logout(self):
        self.find_by_xpath(CumTradingLimitsConstants.LOGOUT_BUTTON_XPATH).click()

    def set_description(self, value):
        self.set_text_by_xpath(CumTradingLimitsConstants.MAIN_PAGE_DESCRIPTION_FILTER_XPATH, value)

    def set_cum_trading_limit_percentage(self, value):
        self.set_text_by_xpath(CumTradingLimitsConstants.MAIN_PAGE_CUM_TRADING_LIMIT_PERCENTAGE_FILTER_XPATH, value)

    def set_max_qty(self, value):
        self.set_text_by_xpath(CumTradingLimitsConstants.MAIN_PAGE_MAX_QTY_FILTER_XPATH, value)

    def set_max_amt(self, value):
        self.set_text_by_xpath(CumTradingLimitsConstants.MAIN_PAGE_MAX_AMT_FILTER_XPATH, value)

    def set_soft_max_qty(self, value):
        self.set_text_by_xpath(CumTradingLimitsConstants.MAIN_PAGE_SOFT_MAX_QTY_FILTER_XPATH, value)

    def set_soft_max_amt(self, value):
        self.set_text_by_xpath(CumTradingLimitsConstants.MAIN_PAGE_SOFT_MAX_AMT_FILTER_XPATH, value)

    def set_currency(self, value):
        self.set_text_by_xpath(CumTradingLimitsConstants.MAIN_PAGE_CURRENCY_FILTER_XPATH, value)

    def set_max_sell_qty(self, value):
        self.set_text_by_xpath(CumTradingLimitsConstants.MAIN_PAGE_DESCRIPTION_FILTER_XPATH, value)

    def get_currency(self):
        return self.find_by_xpath(CumTradingLimitsConstants.MAIN_PAGE_CURRENCY_XPATH).text
