import time

from quod_qa.web_admin.web_admin_core.pages.common_page import CommonPage
from quod_qa.web_admin.web_admin_core.pages.positions.cash_positions.cash_positions_constants import \
    CashPositionsConstants
from quod_qa.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer


class CashPositionsPage(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def click_on_more_actions(self):
        self.find_by_xpath(CashPositionsConstants.MORE_ACTIONS_XPATH).click()

    def click_on_edit(self):
        self.find_by_xpath(CashPositionsConstants.EDIT_XPATH).click()

    def click_on_clone(self):
        self.find_by_xpath(CashPositionsConstants.CLONE_XPATH).click()

    def click_on_delete(self, confirmation):
        self.find_by_xpath(CashPositionsConstants.DELETE_XPATH).click()
        if confirmation:
            time.sleep(2)
            self.find_by_xpath(CashPositionsConstants.OK_BUTTON_XPATH).click()
        else:
            self.find_by_xpath(CashPositionsConstants.CANCEL_BUTTON_XPATH).click()

    def click_download_pdf_entity_button_and_check_pdf(self, value):
        self.clear_download_directory()
        self.find_by_xpath(CashPositionsConstants.DOWNLOAD_PDF_BUTTON_XPATH).click()
        time.sleep(2)
        return self.is_pdf_contains_value(value)

    def click_download_csv_entity_button_and_check_csv(self):
        self.clear_download_directory()
        self.find_by_xpath(CashPositionsConstants.MAIN_PAGE_DOWNLOAD_CSV_BUTTON_XPATH).click()
        time.sleep(2)
        return self.get_csv_context()

    def click_on_pin_row(self):
        self.find_by_xpath(CashPositionsConstants.PIN_ROW_XPATH).click()

    def click_on_new(self):
        self.find_by_xpath(CashPositionsConstants.NEW_BUTTON_XPATH).click()

    def click_on_user_icon(self):
        self.find_by_xpath(CashPositionsConstants.USER_ICON_AT_RIGHT_CORNER).click()

    def click_on_logout(self):
        self.find_by_xpath(CashPositionsConstants.LOGOUT_BUTTON_XPATH).click()

    def set_name(self, value):
        self.set_text_by_xpath(CashPositionsConstants.MAIN_PAGE_NAME_FILTER_XPATH, value)

    def set_currency(self, value):
        self.set_text_by_xpath(CashPositionsConstants.MAIN_PAGE_CURRENCY_FILTER_XPATH, value)

    def set_client(self, value):
        self.set_text_by_xpath(CashPositionsConstants.MAIN_PAGE_CLIENT_FILTER_XPATH, value)

    def set_venue_cash_account_id(self, value):
        self.set_text_by_xpath(CashPositionsConstants.MAIN_PAGE_VENUE_CASH_ACCOUNT_ID_FILTER_XPATH, value)

    def set_client_cash_account_id(self, value):
        self.set_text_by_xpath(CashPositionsConstants.MAIN_PAGE_CLIENT_CASH_ACCOUNT_ID_FILTER_XPATH, value)

    def get_name(self):
        return self.find_by_xpath(CashPositionsConstants.MAIN_PAGE_NAME_XPATH).text

    def get_currency(self):
        return self.find_by_xpath(CashPositionsConstants.MAIN_PAGE_CURRENCY_XPATH).text

    def get_client(self):
        return self.find_by_xpath(CashPositionsConstants.MAIN_PAGE_CLIENT_XPATH).text

    def get_venue_cash_account_id(self):
        return self.find_by_xpath(CashPositionsConstants.MAIN_PAGE_VENUE_CASH_ACCOUNT_ID_XPATH)

    def get_client_cash_account_id(self):
        return self.find_by_xpath(CashPositionsConstants.MAIN_PAGE_CLIENT_CASH_ACCOUNT_ID_XPATH).text
