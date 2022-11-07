import time

from test_framework.web_admin_core.pages.common_page import CommonPage
from test_framework.web_admin_core.pages.markets.subvenues.subvenues_constants import SubVenuesConstants
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer


class SubVenuesPage(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def click_on_more_actions(self):
        self.find_by_xpath(SubVenuesConstants.MORE_ACTIONS_XPATH).click()

    def click_on_edit(self):
        self.find_by_xpath(SubVenuesConstants.EDIT_XPATH).click()

    def click_on_clone(self):
        self.find_by_xpath(SubVenuesConstants.CLONE_XPATH).click()

    def click_on_delete(self, confirmation):
        self.find_by_xpath(SubVenuesConstants.DELETE_XPATH).click()
        if confirmation:
            time.sleep(2)
            self.find_by_xpath(SubVenuesConstants.OK_BUTTON_XPATH).click()
        else:
            self.find_by_xpath(SubVenuesConstants.CANCEL_BUTTON_XPATH).click()

    def click_download_pdf_entity_button_and_check_pdf(self, value):
        self.clear_download_directory()
        self.find_by_xpath(SubVenuesConstants.DOWNLOAD_PDF_BUTTON_XPATH).click()
        time.sleep(2)
        return self.is_pdf_contains_value(value)

    def click_on_pin_row(self):
        self.find_by_xpath(SubVenuesConstants.PIN_ROW_XPATH).click()

    def click_on_new(self):
        self.find_by_xpath(SubVenuesConstants.NEW_BUTTON_XPATH).click()

    def click_on_user_icon(self):
        self.find_by_xpath(SubVenuesConstants.USER_ICON_AT_RIGHT_CORNER).click()

    def click_on_logout(self):
        self.find_by_xpath(SubVenuesConstants.LOGOUT_BUTTON_XPATH).click()

    def set_name_filter(self, value):
        self.set_text_by_xpath(SubVenuesConstants.MAIN_PAGE_NAME_FILTER_XPATH, value)

    def set_ext_id_venue_filter(self, value):
        self.set_text_by_xpath(SubVenuesConstants.MAIN_PAGE_EXT_ID_VENUE_FILTER_XPATH, value)

    def set_venue(self, value):
        self.set_text_by_xpath(SubVenuesConstants.MAIN_PAGE_EXT_ID_VENUE_FILTER_XPATH, value)

    def set_market_data_source(self, value):
        self.set_text_by_xpath(SubVenuesConstants.MAIN_PAGE_VENUE_FILTER_XPATH, value)

    def set_default_symbol(self, value):
        self.set_text_by_xpath(SubVenuesConstants.MAIN_PAGE_DEFAULT_SYMBOL_FILTER_XPATH, value)

    def set_news(self, value):
        self.select_value_from_dropdown_list(SubVenuesConstants.MAIN_PAGE_NEWS_FILTER_XPATH, value)

    def set_news_symbol(self, value):
        self.set_text_by_xpath(SubVenuesConstants.MAIN_PAGE_NEWS_SYMBOL_FILTER_XPATH, value)

    def get_name(self):
        return self.find_by_xpath(SubVenuesConstants.MAIN_PAGE_NAME_XPATH).text

    def get_ext_id_venue(self):
        return self.find_by_xpath(SubVenuesConstants.MAIN_PAGE_EXT_ID_VENUE_XPATH).text

    def get_venue(self):
        return self.find_by_xpath(SubVenuesConstants.MAIN_PAGE_VENUE_XPATH).text

    def get_market_data_source(self):
        return self.find_by_xpath(SubVenuesConstants.MAIN_PAGE_MARKET_DATA_SOURCE_XPATH).text

    def get_default_symbol(self):
        return self.find_by_xpath(SubVenuesConstants.MAIN_PAGE_DEFAULT_SYMBOL_XPATH).text

    def get_news_symbol(self):
        return self.find_by_xpath(SubVenuesConstants.MAIN_PAGE_NEWS_SYMBOL_XPATH).text

    def is_searched_subvenue_found(self, value):
        return self.is_element_present(SubVenuesConstants.DISPLAYED_SUBVENUE_XPATH.format(value))
