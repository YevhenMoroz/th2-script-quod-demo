import time

from test_framework.web_admin_core.pages.common_page import CommonPage
from test_framework.web_admin_core.pages.middle_office.allocation_matching_profiles.constants import \
    AllocationMatchingProfilesConstants

from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer


class AllocationMatchingProfilesPage(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def click_on_more_actions(self):
        self.find_by_xpath(AllocationMatchingProfilesConstants.MORE_ACTIONS_XPATH).click()

    def click_on_edit(self):
        self.find_by_xpath(AllocationMatchingProfilesConstants.EDIT_XPATH).click()

    def click_on_clone(self):
        self.find_by_xpath(AllocationMatchingProfilesConstants.CLONE_XPATH).click()

    def click_on_delete(self, confirmation):
        self.find_by_xpath(AllocationMatchingProfilesConstants.DELETE_XPATH).click()
        if confirmation:
            time.sleep(2)
            self.find_by_xpath(AllocationMatchingProfilesConstants.OK_BUTTON_XPATH).click()
        else:
            self.find_by_xpath(AllocationMatchingProfilesConstants.CANCEL_BUTTON_XPATH).click()

    def click_download_pdf_entity_button_and_check_pdf(self, value):
        self.clear_download_directory()
        self.find_by_xpath(AllocationMatchingProfilesConstants.DOWNLOAD_PDF_BUTTON_XPATH).click()
        time.sleep(2)
        return self.is_pdf_contains_value(value)

    def click_download_csv_entity_button_and_check_csv(self):
        self.clear_download_directory()
        self.find_by_xpath(AllocationMatchingProfilesConstants.MAIN_PAGE_DOWNLOAD_CSV_BUTTON_XPATH).click()
        time.sleep(2)
        return self.get_csv_context()

    def click_on_pin_row(self):
        self.find_by_xpath(AllocationMatchingProfilesConstants.PIN_ROW_XPATH).click()

    def click_on_new(self):
        self.find_by_xpath(AllocationMatchingProfilesConstants.NEW_BUTTON_XPATH).click()

    def click_on_user_icon(self):
        self.find_by_xpath(AllocationMatchingProfilesConstants.USER_ICON_AT_RIGHT_CORNER).click()

    def click_on_logout(self):
        self.find_by_xpath(AllocationMatchingProfilesConstants.LOGOUT_BUTTON_XPATH).click()

    def set_name(self, value):
        self.set_text_by_xpath(AllocationMatchingProfilesConstants.MAIN_PAGE_FIX_MATCHING_PROFILE_NAME_FILTER_XPATH, value)

    def set_instrument(self, value):
        self.set_text_by_xpath(AllocationMatchingProfilesConstants.MAIN_PAGE_INSTRUMENT_FILTER_XPATH, value)

    def set_client(self, value):
        self.set_text_by_xpath(AllocationMatchingProfilesConstants.MAIN_PAGE_CLIENT_FILTER_XPATH, value)

    def set_quantity(self, value):
        self.set_text_by_xpath(AllocationMatchingProfilesConstants.MAIN_PAGE_QUANTITY_FILTER_XPATH, value)

    def set_avg_price(self, value):
        self.set_text_by_xpath(AllocationMatchingProfilesConstants.MAIN_PAGE_AVG_PRICE_FILTER_XPATH, value)

    def set_currency(self, value):
        self.set_text_by_xpath(AllocationMatchingProfilesConstants.MAIN_PAGE_CURRENCY_FILTER_XPATH, value)

    def set_side(self, value):
        self.set_text_by_xpath(AllocationMatchingProfilesConstants.MAIN_PAGE_SIDE_FILTER_XPATH, value)

    def is_searched_entity_found_by_name(self, name):
        return self.is_element_present(AllocationMatchingProfilesConstants.DISPLAYED_ENTITY_XPATH.format(name))
