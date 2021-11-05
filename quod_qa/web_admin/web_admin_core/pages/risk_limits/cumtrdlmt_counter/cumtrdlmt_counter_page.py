import time

from quod_qa.web_admin.web_admin_core.pages.common_page import CommonPage
from quod_qa.web_admin.web_admin_core.pages.risk_limits.cumtrdlmt_counter.cumtrdlmt_counter_constants import \
    CumTrdLmtCounterConstants
from quod_qa.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer


class CumTrdLmtPage(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def click_on_more_actions(self):
        self.find_by_xpath(CumTrdLmtCounterConstants.MORE_ACTIONS_XPATH).click()

    def click_on_edit(self):
        self.find_by_xpath(CumTrdLmtCounterConstants.EDIT_XPATH).click()

    def click_on_clone(self):
        self.find_by_xpath(CumTrdLmtCounterConstants.CLONE_XPATH).click()

    def click_on_delete(self, confirmation):
        self.find_by_xpath(CumTrdLmtCounterConstants.DELETE_XPATH).click()
        if confirmation:
            time.sleep(2)
            self.find_by_xpath(CumTrdLmtCounterConstants.OK_BUTTON_XPATH).click()
        else:
            self.find_by_xpath(CumTrdLmtCounterConstants.CANCEL_BUTTON_XPATH).click()

    def click_download_pdf_entity_button_and_check_pdf(self, value):
        self.clear_download_directory()
        self.find_by_xpath(CumTrdLmtCounterConstants.DOWNLOAD_PDF_BUTTON_XPATH).click()
        time.sleep(2)
        return self.is_pdf_contains_value(value)

    def click_download_csv_entity_button_and_check_csv(self):
        self.clear_download_directory()
        self.find_by_xpath(CumTrdLmtCounterConstants.MAIN_PAGE_DOWNLOAD_CSV_BUTTON_XPATH).click()
        time.sleep(2)
        return self.get_csv_context()

    def click_on_pin_row(self):
        self.find_by_xpath(CumTrdLmtCounterConstants.PIN_ROW_XPATH).click()

    def click_on_new(self):
        self.find_by_xpath(CumTrdLmtCounterConstants.NEW_BUTTON_XPATH).click()

    def click_on_user_icon(self):
        self.find_by_xpath(CumTrdLmtCounterConstants.USER_ICON_AT_RIGHT_CORNER).click()

    def click_on_logout(self):
        self.find_by_xpath(CumTrdLmtCounterConstants.LOGOUT_BUTTON_XPATH).click()

    def set_cum_trading_limit(self, value):
        self.set_text_by_xpath(CumTrdLmtCounterConstants.MAIN_PAGE_CUM_TRADING_LIMIT_FILTER_XPATH, value)

    def set_cum_buy_ord_qty(self, value):
        self.set_text_by_xpath(CumTrdLmtCounterConstants.MAIN_PAGE_CUM_BUY_ORD_QTY_FILTER_XPATH, value)

    def set_cum_ord_amt(self, value):
        self.set_text_by_xpath(CumTrdLmtCounterConstants.MAIN_PAGE_CUM_ORD_AMT_FILTER_XPATH, value)

    def set_cum_sell_ord_qty(self, value):
        self.set_text_by_xpath(CumTrdLmtCounterConstants.MAIN_PAGE_CUM_SELL_ORD_AMT_FILTER_XPATH, value)

    def set_cum_buy_ord_amt(self, value):
        self.set_text_by_xpath(CumTrdLmtCounterConstants.MAIN_PAGE_CUM_BUY_ORD_AMT_FILTER_XPATH, value)

    def set_cum_ord_qty(self, value):
        self.set_text_by_xpath(CumTrdLmtCounterConstants.MAIN_PAGE_CUM_ORD_QTY_FILTER_XPATH, value)

    def set_cum_sell_ord_amt(self, value):
        self.set_text_by_xpath(CumTrdLmtCounterConstants.MAIN_PAGE_CUM_SELL_ORD_AMT_FILTER_XPATH, value)
