import time

from test_framework.web_admin_core.pages.common_page import CommonPage
from test_framework.web_admin_core.pages.positions.cash_positions.constants import Constants
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer


class MainPage(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def click_on_more_actions(self):
        self.find_by_xpath(Constants.MainPage.MORE_ACTIONS_BUTTON).click()

    def click_on_edit(self):
        self.find_by_xpath(Constants.MainPage.EDIT_BUTTON).click()

    def click_on_clone(self):
        self.find_by_xpath(Constants.MainPage.CLONE_BUTTON).click()

    def click_download_pdf_entity_button_and_check_pdf(self, value):
        self.clear_download_directory()
        self.find_by_xpath(Constants.MainPage.DOWNLOAD_PDF_BUTTON).click()
        time.sleep(2)
        return self.is_pdf_contains_value(value)

    def click_download_csv_entity_button_and_check_csv(self):
        self.clear_download_directory()
        self.find_by_xpath(Constants.MainPage.DOWNLOAD_CSV_BUTTON).click()
        time.sleep(2)
        return self.get_csv_context()

    def click_on_pin_row(self):
        self.find_by_xpath(Constants.MainPage.PIN_ROW_BUTTON).click()

    def click_on_transaction(self):
        self.find_by_xpath(Constants.MainPage.TRANSACTION_BUTTON).click()

    def set_transaction_type(self, value):
        self.select_value_from_dropdown_list(Constants.MainPage.TRANSACTION_TYPE, value)

    def set_amount(self, value):
        self.set_text_by_xpath(Constants.MainPage.AMOUNT, value)

    def set_reference(self, value):
        self.set_text_by_xpath(Constants.MainPage.REFERENCE, value)

    def click_on_ok_button(self):
        self.find_by_xpath(Constants.MainPage.OK_BUTTON).click()

    def click_on_cancel_button(self):
        self.find_by_xpath(Constants.MainPage.CANCEL_BUTTON).click()

    def is_transaction_pop_up_displayed(self):
        return self.is_element_present(Constants.MainPage.TRANSACTION_POP_UP)

    def click_on_new(self):
        self.find_by_xpath(Constants.MainPage.NEW_BUTTON).click()

    def set_name(self, value):
        self.set_text_by_xpath(Constants.MainPage.NAME_FILTER, value)

    def set_currency(self, value):
        self.set_text_by_xpath(Constants.MainPage.CURRENCY_FILTER, value)

    def set_client(self, value):
        self.set_text_by_xpath(Constants.MainPage.CLIENT_FILTER, value)

    def set_venue_cash_account_id(self, value):
        self.set_text_by_xpath(Constants.MainPage.VENUE_CASH_ACCOUNT_ID_FILTER, value)

    def set_client_cash_account_id(self, value):
        self.set_text_by_xpath(Constants.MainPage.CLIENT_CASH_ACCOUNT_ID_FILTER, value)

    def get_name(self):
        return self.find_by_xpath(Constants.MainPage.NAME).text

    def get_currency(self):
        return self.find_by_xpath(Constants.MainPage.CURRENCY).text

    def get_client(self):
        return self.find_by_xpath(Constants.MainPage.CLIENT).text

    def get_venue_cash_account_id(self):
        return self.find_by_xpath(Constants.MainPage.VENUE_CASH_ACCOUNT_ID).text

    def get_client_cash_account_id(self):
        return self.find_by_xpath(Constants.MainPage.CLIENT_CASH_ACCOUNT_ID).text

    def is_searched_cash_account_found(self, value):
        return self.is_element_present(Constants.MainPage.DISPLAYED_CASH_POSITIONS.format(value))

    def click_on_enable_disable_button(self):
        self.find_by_xpath(Constants.MainPage.TOGGLE_BUTTON).click()
