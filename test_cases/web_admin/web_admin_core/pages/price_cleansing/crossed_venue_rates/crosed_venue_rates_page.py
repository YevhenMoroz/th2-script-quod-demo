import time

from test_cases.web_admin.web_admin_core.pages.common_page import CommonPage
from test_cases.web_admin.web_admin_core.pages.price_cleansing.crossed_venue_rates.crossed_venue_rates_constants import \
    CrossedVenueRatesConstants
from test_cases.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer


class CrossedVenueRatesPage(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def click_on_more_actions(self):
        self.find_by_xpath(CrossedVenueRatesConstants.MORE_ACTIONS_XPATH).click()

    def click_on_edit(self):
        self.find_by_xpath(CrossedVenueRatesConstants.EDIT_XPATH).click()

    def click_on_clone(self):
        self.find_by_xpath(CrossedVenueRatesConstants.CLONE_XPATH).click()

    def click_on_delete(self, confirmation):
        self.find_by_xpath(CrossedVenueRatesConstants.DELETE_XPATH).click()
        if confirmation:
            time.sleep(2)
            self.find_by_xpath(CrossedVenueRatesConstants.OK_BUTTON_XPATH).click()
        else:
            self.find_by_xpath(CrossedVenueRatesConstants.CANCEL_BUTTON_XPATH).click()

    def click_download_pdf_entity_button_and_check_pdf(self, value):
        self.clear_download_directory()
        self.find_by_xpath(CrossedVenueRatesConstants.DOWNLOAD_PDF_BUTTON_XPATH).click()
        time.sleep(2)
        return self.is_pdf_contains_value(value)

    def click_download_csv_entity_button_and_check_csv(self):
        self.clear_download_directory()
        self.find_by_xpath(CrossedVenueRatesConstants.MAIN_PAGE_DOWNLOAD_CSV_BUTTON_XPATH).click()
        time.sleep(2)
        return self.get_csv_context()

    def click_on_pin_row(self):
        self.find_by_xpath(CrossedVenueRatesConstants.PIN_ROW_XPATH).click()

    def click_on_new(self):
        self.find_by_xpath(CrossedVenueRatesConstants.NEW_BUTTON_XPATH).click()

    def click_on_user_icon(self):
        self.find_by_xpath(CrossedVenueRatesConstants.USER_ICON_AT_RIGHT_CORNER).click()

    def click_on_logout(self):
        self.find_by_xpath(CrossedVenueRatesConstants.LOGOUT_BUTTON_XPATH).click()

    def set_name(self, value):
        self.set_text_by_xpath(CrossedVenueRatesConstants.MAIN_PAGE_NAME_FILTER_XPATH, value)

    def set_venue(self, value):
        self.set_text_by_xpath(CrossedVenueRatesConstants.MAIN_PAGE_VENUE_FILTER_XPATH, value)

    def set_listing(self, value):
        self.set_text_by_xpath(CrossedVenueRatesConstants.MAIN_PAGE_LISTING_FILTER_XPATH, value)

    def set_symbol(self, value):
        self.set_text_by_xpath(CrossedVenueRatesConstants.MAIN_PAGE_SYMBOL_FILTER_XPATH, value)

    def set_instr_type(self, value):
        self.set_text_by_xpath(CrossedVenueRatesConstants.MAIN_PAGE_INSTR_TYPE_FILTER_XPATH, value)

    def get_name(self):
        return self.find_by_xpath(CrossedVenueRatesConstants.MAIN_PAGE_NAME_XPATH).text

    def get_venue(self):
        return self.find_by_xpath(CrossedVenueRatesConstants.MAIN_PAGE_VENUE_XPATH).text

    def get_listing(self):
        return self.find_by_xpath(CrossedVenueRatesConstants.MAIN_PAGE_LISTING_XPATH).text

    def get_symbol(self):
        return self.find_by_xpath(CrossedVenueRatesConstants.MAIN_PAGE_SYMBOL_XPATH).text

    def get_instr_type(self):
        return self.find_by_xpath(CrossedVenueRatesConstants.MAIN_PAGE_INSTR_TYPE_XPATH).text
