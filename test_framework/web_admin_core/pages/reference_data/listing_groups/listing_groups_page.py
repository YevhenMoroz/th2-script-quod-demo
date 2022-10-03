import time

from test_framework.web_admin_core.pages.common_page import CommonPage
from test_framework.web_admin_core.pages.reference_data.listing_groups.listing_groups_constants import \
    ListingGroupsConstants
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer


class ListingGroupsPage(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def click_on_more_actions(self):
        self.find_by_xpath(ListingGroupsConstants.MORE_ACTIONS_XPATH).click()

    def click_on_edit(self):
        self.find_by_xpath(ListingGroupsConstants.EDIT_XPATH).click()

    def click_on_clone(self):
        self.find_by_xpath(ListingGroupsConstants.CLONE_XPATH).click()

    def click_download_pdf_entity_button_and_check_pdf(self, value):
        self.clear_download_directory()
        self.find_by_xpath(ListingGroupsConstants.DOWNLOAD_PDF_BUTTON_XPATH).click()
        time.sleep(2)
        return self.is_pdf_contains_value(value)

    def click_on_delete(self, confirmation):
        self.find_by_xpath(ListingGroupsConstants.DELETE_XPATH).click()
        if confirmation:
            time.sleep(2)
            self.find_by_xpath(ListingGroupsConstants.OK_BUTTON_XPATH).click()
        else:
            self.find_by_xpath(ListingGroupsConstants.CANCEL_BUTTON_XPATH).click()

    def click_on_pin_row(self):
        self.find_by_xpath(ListingGroupsConstants.PIN_ROW_XPATH).click()

    def click_on_new(self):
        self.find_by_xpath(ListingGroupsConstants.NEW_BUTTON_XPATH).click()

    def click_on_user_icon(self):
        self.find_by_xpath(ListingGroupsConstants.USER_ICON_AT_RIGHT_CORNER).click()

    def click_on_logout(self):
        self.find_by_xpath(ListingGroupsConstants.LOGOUT_BUTTON_XPATH).click()

    def set_name(self, value):
        self.set_text_by_xpath(ListingGroupsConstants.MAIN_PAGE_NAME_FILTER_XPATH, value)

    def get_name(self):
        return self.find_by_xpath(ListingGroupsConstants.MAIN_PAGE_NAME_XPATH).text

    def set_ext_id_venue(self, value):
        self.set_text_by_xpath(ListingGroupsConstants.MAIN_PAGE_EXT_ID_VENUE_FILTER_XPATH, value)

    def get_ext_id_venue(self):
        return self.find_by_xpath(ListingGroupsConstants.MAIN_PAGE_EXT_ID_VENUE_XPATH)

    def set_sub_venue(self, value):
        self.set_text_by_xpath(ListingGroupsConstants.MAIN_PAGE_SUB_VENUE_FILTER_XPATH, value)

    def get_sub_venue(self):
        return self.find_by_xpath(ListingGroupsConstants.MAIN_PAGE_SUB_VENUE_XPATH).text

    def set_market_data_source(self, value):
        self.set_text_by_xpath(ListingGroupsConstants.MAIN_PAGE_MARKET_DATA_SOURCE_FILTER_XPATH, value)

    def get_market_data_source(self):
        return self.find_by_xpath(ListingGroupsConstants.MAIN_PAGE_MARKET_DATA_SOURCE_XPATH).text

    def set_feed_source(self, value):
        self.set_text_by_xpath(ListingGroupsConstants.MAIN_PAGE_FEED_SOURCE_FILTER_XPATH, value)

    def get_feed_source(self):
        return self.get_text_by_xpath(ListingGroupsConstants.MAIN_PAGE_FEED_SOURCE_XPATH)

    def is_feed_source_field_editable(self):
        return self.is_field_enabled(ListingGroupsConstants.MAIN_PAGE_FEED_SOURCE_XPATH)
