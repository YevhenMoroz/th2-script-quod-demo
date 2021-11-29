import time

from test_cases.web_admin.web_admin_core.pages.common_page import CommonPage
from test_cases.web_admin.web_admin_core.pages.risk_limits.trading_limits.trading_limits_constants import \
    TradingLimitsConstants

from test_cases.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer


class TradingLimitsPage(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def click_on_more_actions(self):
        self.find_by_xpath(TradingLimitsConstants.MORE_ACTIONS_XPATH).click()

    def click_on_edit(self):
        self.find_by_xpath(TradingLimitsConstants.EDIT_XPATH).click()

    def click_on_clone(self):
        self.find_by_xpath(TradingLimitsConstants.CLONE_XPATH).click()

    def click_on_delete(self, confirmation):
        self.find_by_xpath(TradingLimitsConstants.DELETE_XPATH).click()
        if confirmation:
            time.sleep(2)
            self.find_by_xpath(TradingLimitsConstants.OK_BUTTON_XPATH).click()
        else:
            self.find_by_xpath(TradingLimitsConstants.CANCEL_BUTTON_XPATH).click()

    def click_download_pdf_entity_button_and_check_pdf(self, value):
        self.clear_download_directory()
        self.find_by_xpath(TradingLimitsConstants.DOWNLOAD_PDF_BUTTON_XPATH).click()
        time.sleep(2)
        return self.is_pdf_contains_value(value)

    def click_download_csv_entity_button_and_check_csv(self):
        self.clear_download_directory()
        self.find_by_xpath(TradingLimitsConstants.MAIN_PAGE_DOWNLOAD_CSV_BUTTON_XPATH).click()
        time.sleep(2)
        return self.get_csv_context()

    def click_on_pin_row(self):
        self.find_by_xpath(TradingLimitsConstants.PIN_ROW_XPATH).click()

    def click_on_new(self):
        self.find_by_xpath(TradingLimitsConstants.NEW_BUTTON_XPATH).click()

    def click_on_user_icon(self):
        self.find_by_xpath(TradingLimitsConstants.USER_ICON_AT_RIGHT_CORNER).click()

    def click_on_logout(self):
        self.find_by_xpath(TradingLimitsConstants.LOGOUT_BUTTON_XPATH).click()

    def set_description(self, value):
        self.set_text_by_xpath(TradingLimitsConstants.MAIN_PAGE_DESCRIPTION_FILTER_XPATH, value)

    def get_description(self):
        return self.find_by_xpath(TradingLimitsConstants.MAIN_PAGE_DESCRIPTION_XPATH).text

    def set_external_id(self, value):
        self.set_text_by_xpath(TradingLimitsConstants.MAIN_PAGE_EXTERNAL_ID_FILTER_XPATH, value)

    def get_external_id(self):
        return self.find_by_xpath(TradingLimitsConstants.MAIN_PAGE_EXTERNAL_ID_XPATH).text

    def set_currency(self, value):
        self.set_text_by_xpath(TradingLimitsConstants.MAIN_PAGE_CURRENCY_FILTER_XPATH, value)

    def get_currency(self):
        return self.find_by_xpath(TradingLimitsConstants.MAIN_PAGE_CURRENCY_XPATH).text

    def set_max_qty(self, value):
        self.set_text_by_xpath(TradingLimitsConstants.MAIN_PAGE_MAX_QTY_FILTER_XPATH, value)

    def get_max_qty(self):
        return self.find_by_xpath(TradingLimitsConstants.MAIN_PAGE_MAX_QTY_XPATH).text

    def set_max_amt(self, value):
        self.set_text_by_xpath(TradingLimitsConstants.MAIN_PAGE_MAX_AMT_FILTER_XPATH, value)

    def get_max_amt(self):
        return self.find_by_xpath(TradingLimitsConstants.MAIN_PAGE_MAX_AMT_XPATH).text

    def set_max_soft_qty(self, value):
        self.set_text_by_xpath(TradingLimitsConstants.MAIN_PAGE_MAX_SOFT_QTY_FILTER_XPATH, value)

    def get_max_soft_qty(self):
        return self.find_by_xpath(TradingLimitsConstants.MAIN_PAGE_MAX_SOFT_QTY_XPATH).text

    def set_max_soft_amt(self, value):
        self.set_text_by_xpath(TradingLimitsConstants.MAIN_PAGE_MAX_SOFT_AMT_FILTER_XPATH, value)

    def get_max_soft_amt(self):
        return self.find_by_xpath(TradingLimitsConstants.MAIN_PAGE_MAX_SOFT_AMT_XPATH).text
