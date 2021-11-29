import time

from test_cases.web_admin.web_admin_core.pages.common_page import CommonPage
from test_cases.web_admin.web_admin_core.pages.risk_limits.position_limits.position_limits_constants import \
    PositionsLimitsConstants
from test_cases.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer


class PositionLimitsPage(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def click_on_more_actions(self):
        self.find_by_xpath(PositionsLimitsConstants.MORE_ACTIONS_XPATH).click()

    def click_on_edit(self):
        self.find_by_xpath(PositionsLimitsConstants.EDIT_XPATH).click()

    def click_on_clone(self):
        self.find_by_xpath(PositionsLimitsConstants.CLONE_XPATH).click()

    def click_on_delete(self, confirmation):
        self.find_by_xpath(PositionsLimitsConstants.DELETE_XPATH).click()
        if confirmation:
            time.sleep(2)
            self.find_by_xpath(PositionsLimitsConstants.OK_BUTTON_XPATH).click()
        else:
            self.find_by_xpath(PositionsLimitsConstants.CANCEL_BUTTON_XPATH).click()

    def click_download_pdf_entity_button_and_check_pdf(self, value):
        self.clear_download_directory()
        self.find_by_xpath(PositionsLimitsConstants.DOWNLOAD_PDF_BUTTON_XPATH).click()
        time.sleep(2)
        return self.is_pdf_contains_value(value)

    def click_download_csv_entity_button_and_check_csv(self):
        self.clear_download_directory()
        self.find_by_xpath(PositionsLimitsConstants.MAIN_PAGE_DOWNLOAD_CSV_BUTTON_XPATH).click()
        time.sleep(2)
        return self.get_csv_context()

    def click_on_pin_row(self):
        self.find_by_xpath(PositionsLimitsConstants.PIN_ROW_XPATH).click()

    def click_on_new(self):
        self.find_by_xpath(PositionsLimitsConstants.NEW_BUTTON_XPATH).click()

    def click_on_user_icon(self):
        self.find_by_xpath(PositionsLimitsConstants.USER_ICON_AT_RIGHT_CORNER).click()

    def click_on_logout(self):
        self.find_by_xpath(PositionsLimitsConstants.LOGOUT_BUTTON_XPATH).click()

    def set_min_soft_qty(self, value):
        self.set_text_by_xpath(PositionsLimitsConstants.MAIN_PAGE_MIN_SOFT_QTY_FILTER_XPATH, value)

    def get_min_soft_qty(self):
        return self.find_by_xpath(PositionsLimitsConstants.MAIN_PAGE_MIN_SOFT_QTY_FILTER_XPATH).text

    def set_min_soft_amt(self, value):
        self.set_text_by_xpath(PositionsLimitsConstants.MAIN_PAGE_MIN_SOFT_AMT_FILTER_XPATH, value)

    def get_min_soft_amt(self):
        return self.find_by_xpath(PositionsLimitsConstants.MAIN_PAGE_MIN_SOFT_AMT_XPATH).text

    def set_max_soft_qty(self, value):
        self.set_text_by_xpath(PositionsLimitsConstants.MAIN_PAGE_MAX_SOFT_QTY_FILTER_XPATH, value)

    def get_max_soft_qty(self):
        return self.find_by_xpath(PositionsLimitsConstants.MAIN_PAGE_MAX_SOFT_QTY_XPATH).text

    def set_max_soft_amt(self, value):
        self.set_text_by_xpath(PositionsLimitsConstants.MAIN_PAGE_MAX_SOFT_AMT_FILTER_XPATH, value)

    def get_max_soft_amt(self):
        return self.find_by_xpath(PositionsLimitsConstants.MAIN_PAGE_MAX_SOFT_AMT_XPATH).text

    def set_min_qty(self, value):
        self.set_text_by_xpath(PositionsLimitsConstants.MAIN_PAGE_MIN_QTY_FILTER_XPATH, value)

    def get_min_qty(self):
        return self.find_by_xpath(PositionsLimitsConstants.MAIN_PAGE_MIN_QTY_XPATH).text

    def set_min_amt(self, value):
        self.set_text_by_xpath(PositionsLimitsConstants.MAIN_PAGE_MIN_AMT_FILTER_XPATH, value)

    def get_min_amt(self):
        return self.find_by_xpath(PositionsLimitsConstants.MAIN_PAGE_MIN_AMT_XPATH).text

    def set_max_qty(self, value):
        self.set_text_by_xpath(PositionsLimitsConstants.MAIN_PAGE_MAX_QTY_FILTER_XPATH, value)

    def get_max_qty(self):
        return self.find_by_xpath(PositionsLimitsConstants.MAIN_PAGE_MAX_QTY_XPATH).text

    def set_max_amt(self, value):
        self.set_text_by_xpath(PositionsLimitsConstants.MAIN_PAGE_MAX_AMT_FILTER_XPATH, value)

    def get_max_amt(self):
        return self.find_by_xpath(PositionsLimitsConstants.MAIN_PAGE_MAX_AMT_XPATH).text
