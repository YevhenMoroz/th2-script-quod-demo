import time

from test_framework.web_admin_core.pages.common_page import CommonPage
from test_framework.web_admin_core.pages.markets.venues.venues_constants import VenuesConstants
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer


class VenuesPage(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def click_on_more_actions(self):
        self.find_by_xpath(VenuesConstants.MORE_ACTIONS_XPATH).click()

    def click_on_edit(self):
        self.find_by_xpath(VenuesConstants.EDIT_XPATH).click()

    def click_on_clone(self):
        self.find_by_xpath(VenuesConstants.CLONE_XPATH).click()

    def click_download_pdf_entity_button_and_check_pdf(self, value):
        self.clear_download_directory()
        self.find_by_xpath(VenuesConstants.DOWNLOAD_PDF_AT_MORE_ACTION_BUTTON_XPATH).click()
        time.sleep(2)
        return self.is_pdf_contains_value(value)

    def click_on_pin_row(self):
        self.find_by_xpath(VenuesConstants.PIN_ROW_XPATH).click()

    def click_on_new(self):
        self.find_by_xpath(VenuesConstants.NEW_BUTTON_XPATH).click()

    def click_on_user_icon(self):
        self.find_by_xpath(VenuesConstants.USER_ICON_AT_RIGHT_CORNER).click()

    def click_on_logout(self):
        self.find_by_xpath(VenuesConstants.LOGOUT_BUTTON_XPATH).click()

    def set_name_filter(self, value):
        self.set_text_by_xpath(VenuesConstants.MAIN_PAGE_NAME_FILTER_XPATH, value)

    def get_name(self):
        return self.find_by_xpath(VenuesConstants.MAIN_PAGE_NAME_XPATH).text

    def set_id_filter(self, value):
        self.set_text_by_xpath(VenuesConstants.MAIN_PAGE_ID_FILTER_XPATH, value)

    def get_id(self):
        return self.find_by_xpath(VenuesConstants.MAIN_PAGE_ID_XPATH).text

    def set_mic(self, value):
        self.set_text_by_xpath(VenuesConstants.MAIN_PAGE_MIC_FILTER_XPATH, value)

    def get_mic(self):
        return self.find_by_xpath(VenuesConstants.MAIN_PAGE_MIC_XPATH)

    def set_country(self, value):
        self.find_by_xpath(VenuesConstants.MAIN_PAGE_COUNTRY_FILTER_XPATH, value)

    def get_country(self):
        return self.find_by_xpath(VenuesConstants.MAIN_PAGE_COUNTRY_XPATH).text

    def set_category(self, value):
        self.set_text_by_xpath(VenuesConstants.MAIN_PAGE_CATEGORY_FILTER_XPATH, value)

    def get_category(self):
        return self.find_by_xpath(VenuesConstants.MAIN_PAGE_CATEGORY_XPATH).text

    def set_qualifier(self, value):
        self.set_text_by_xpath(VenuesConstants.MAIN_PAGE_QUALIFIER_FILTER_XPATH, value)

    def get_qualifier(self):
        return self.find_by_xpath(VenuesConstants.MAIN_PAGE_QUALIFIER_XPATH).text

    def set_anti_crossing_period(self, value):
        self.set_text_by_xpath(VenuesConstants.MAIN_PAGE_ANTI_CROSSING_FILTER_XPATH, value)

    def get_anti_crossing_period(self):
        return self.find_by_xpath(VenuesConstants.MAIN_PAGE_ANTI_CROSSING_XPATH).text

    def set_counterpart(self, value):
        self.set_text_by_xpath(VenuesConstants.MAIN_PAGE_COUNTERPART_FILTER_XPATH, value)

    def get_counterpart(self):
        return self.find_by_xpath(VenuesConstants.MAIN_PAGE_COUNTERPART_XPATH).text

    def is_searched_venue_found(self, value):
        return self.is_element_present(VenuesConstants.DISPLAYED_VENUE_XPATH.format(value))
