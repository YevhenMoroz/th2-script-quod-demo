import time
from test_framework.web_admin_core.pages.common_page import CommonPage
from test_framework.web_admin_core.pages.markets.venue_lists.constants import VenueListsConstants
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer


class VenueListsPage(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def click_on_user_icon(self):
        self.find_by_xpath(VenueListsConstants.MainPage.USER_ICON_AT_RIGHT_CORNER).click()

    def click_on_logout(self):
        self.find_by_xpath(VenueListsConstants.MainPage.LOGOUT_BUTTON_XPATH).click()

    def click_on_download_csv_button(self):
        self.find_by_xpath(VenueListsConstants.MainPage.DOWNLOAD_CSV_BUTTON_XPATH).click()

    def click_on_full_screen_button(self):
        self.find_by_xpath(VenueListsConstants.MainPage.FULL_SCREEN_BUTTON_XPATH).click()

    def click_on_refresh_button(self):
        self.find_by_xpath(VenueListsConstants.MainPage.REFRESH_PAGE_BUTTON_XPATH).click()

    def click_on_new(self):
        self.find_by_xpath(VenueListsConstants.MainPage.NEW_BUTTON_XPATH).click()

    def set_name_filter(self, value):
        self.set_text_by_xpath(VenueListsConstants.MainPage.NAME_FILTER_XPATH, value)

    def set_description_filter(self, value):
        self.set_text_by_xpath(VenueListsConstants.MainPage.DESCRIPTION_FILTER_XPATH, value)

    def click_on_more_actions(self):
        self.find_by_xpath(VenueListsConstants.MainPage.MORE_ACTIONS_BUTTON_XPATH).click()

    def click_on_edit(self):
        self.find_by_xpath(VenueListsConstants.MainPage.EDIT_BUTTON_XPATH).click()

    def click_on_delete(self, confirmation: bool):
        self.find_by_xpath(VenueListsConstants.MainPage.DELETE_BUTTON_XPATH).click()
        time.sleep(1)
        if confirmation:
            self.find_by_xpath(VenueListsConstants.MainPage.OK_BUTTON_XPATH).click()
        else:
            self.find_by_xpath(VenueListsConstants.MainPage.CANCEL_BUTTON_XPATH).click()

    def click_download_pdf_entity_button_and_check_pdf(self, value):
        self.clear_download_directory()
        self.find_by_xpath(VenueListsConstants.MainPage.DOWNLOAD_PDF_BUTTON_XPATH).click()
        time.sleep(2)
        return self.is_pdf_contains_value(value)

    def click_on_pin_row(self):
        self.find_by_xpath(VenueListsConstants.MainPage.PIN_ROW_BUTTON_XPATH).click()

    def is_searched_venue_list_found(self, value):
        return self.is_element_present(VenueListsConstants.MainPage.DISPLAYED_VENUE_LIST_XPATH.format(value))
