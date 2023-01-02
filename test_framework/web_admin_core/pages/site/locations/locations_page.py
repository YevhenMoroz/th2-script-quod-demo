import time

from test_framework.web_admin_core.pages.common_page import CommonPage
from test_framework.web_admin_core.pages.site.locations.locations_constants import LocationsConstants
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer


class LocationsPage(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def click_on_more_actions(self):
        self.find_by_xpath(LocationsConstants.MORE_ACTIONS_XPATH).click()

    def click_on_edit(self):
        self.find_by_xpath(LocationsConstants.EDIT_XPATH).click()

    def click_on_clone(self):
        self.find_by_xpath(LocationsConstants.CLONE_XPATH).click()

    def click_on_enable_disable_button(self):
        self.find_by_xpath(LocationsConstants.ENABLE_DISABLE_BUTTON_XPATH).click()
        time.sleep(2)
        self.find_by_xpath(LocationsConstants.OK_BUTTON_XPATH).click()

    def click_on_delete(self, confirmation):
        self.find_by_xpath(LocationsConstants.DELETE_XPATH).click()
        if confirmation:
            time.sleep(2)
            self.find_by_xpath(LocationsConstants.OK_BUTTON_XPATH).click()
        else:
            self.find_by_xpath(LocationsConstants.CANCEL_BUTTON_XPATH).click()

    def click_download_pdf_entity_button_and_check_pdf(self, value):
        self.clear_download_directory()
        self.find_by_xpath(LocationsConstants.DOWNLOAD_PDF_BUTTON_XPATH).click()
        time.sleep(2)
        return self.is_pdf_contains_value(value)

    def click_on_pin_row(self):
        self.find_by_xpath(LocationsConstants.PIN_ROW_XPATH).click()

    def click_on_new(self):
        self.find_by_xpath(LocationsConstants.NEW_BUTTON_XPATH).click()

    def click_on_user_icon(self):
        self.find_by_xpath(LocationsConstants.USER_ICON_AT_RIGHT_CORNER).click()

    def click_on_logout(self):
        self.find_by_xpath(LocationsConstants.LOGOUT_BUTTON_XPATH).click()

    def set_name(self, value):
        self.set_text_by_xpath(LocationsConstants.MAIN_PAGE_NAME_FILTER_XPATH, value)

    def set_zone(self, value):
        self.set_text_by_xpath(LocationsConstants.MAIN_PAGE_ZONE_FILTER_XPATH, value)

    def set_enabled(self, value):
        self.select_value_from_dropdown_list(LocationsConstants.MAIN_PAGE_ENABLED_FILTER_XPATH, value)

    def is_searched_location_found(self, value):
        return self.is_element_present(LocationsConstants.DISPLAYED_ENTITY_XPATH.format(value))

    def get_list_of_all_zones(self):
        return self.get_all_items_from_table_column(LocationsConstants.ZONES_NAME_COLUMN_XPATH)

    def get_list_of_all_locations_name(self):
        return self.get_all_items_from_table_column(LocationsConstants.LOCATIONS_NAME_COLUMN_XPATH)
