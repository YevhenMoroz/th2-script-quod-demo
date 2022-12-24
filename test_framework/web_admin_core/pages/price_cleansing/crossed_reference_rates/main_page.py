import time

from test_framework.web_admin_core.pages.common_page import CommonPage
from test_framework.web_admin_core.pages.price_cleansing.crossed_reference_rates.constants import Constants
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer


class MainPage(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def click_on_more_actions(self):
        self.find_by_xpath(Constants.MainPage.MoreActions.MORE_ACTIONS_BUTTON).click()

    def click_on_edit(self):
        self.find_by_xpath(Constants.MainPage.MoreActions.EDIT_BUTTON).click()

    def click_on_clone(self):
        self.find_by_xpath(Constants.MainPage.MoreActions.CLONE_BUTTON).click()

    def click_on_delete(self, confirmation: bool):
        self.find_by_xpath(Constants.MainPage.MoreActions.DELETE_BUTTON).click()
        if confirmation:
            time.sleep(2)
            self.find_by_xpath(Constants.MainPage.OK_BUTTON).click()
        else:
            self.find_by_xpath(Constants.MainPage.CANCEL_BUTTON).click()

    def click_download_pdf_entity_button_and_check_pdf(self, value):
        self.clear_download_directory()
        self.find_by_xpath(Constants.MainPage.MoreActions.DOWNLOAD_PDF_BUTTON).click()
        time.sleep(2)
        return self.is_pdf_contains_value(value)

    def click_download_csv_entity_button_and_check_csv(self):
        self.clear_download_directory()
        self.find_by_xpath(Constants.MainPage.DOWNLOAD_CSV_BUTTON).click()
        time.sleep(2)
        return self.get_csv_context()

    def click_on_pin_row(self):
        self.find_by_xpath(Constants.MainPage.MoreActions.PIN_BUTTON).click()

    def click_on_new(self):
        self.find_by_xpath(Constants.MainPage.NEW_BUTTON).click()

    def set_name_filter(self, value):
        self.set_text_by_xpath(Constants.MainPage.Filters.NAME, value)

    def set_remove_detected_price_update_filter(self, confirmation: bool):
        self.find_by_xpath(Constants.MainPage.Filters.REMOVE_DETECTED_PRICE_UPDATES).click()
        if confirmation:
            self.find_by_xpath(Constants.MainPage.Filters.SELECT_OPTION_TRUE).click()
        else:
            self.find_by_xpath(Constants.MainPage.Filters.SELECT_OPTION_FALSE).click()

    def set_venue_filter(self, value):
        self.set_text_by_xpath(Constants.MainPage.Filters.VENUE, value)

    def set_listing_filter(self, value):
        self.set_text_by_xpath(Constants.MainPage.Filters.LISTING, value)

    def set_instr_type(self, value):
        self.set_text_by_xpath(Constants.MainPage.Filters.INSTR_TYPE, value)

    def set_symbol(self, value):
        self.set_text_by_xpath(Constants.MainPage.Filters.SYMBOL, value)

    def is_searched_entity_found_by_name(self, name):
        return self.is_element_present(Constants.MainPage.SEARCHED_ENTITY.format(name))
