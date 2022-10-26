import time

from test_framework.web_admin_core.pages.common_page import CommonPage
from test_framework.web_admin_core.pages.markets.venue_lists.constants import VenueListsConstants
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer


class VenuesListsWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def click_on_download_pdf(self):
        self.find_by_xpath(VenueListsConstants.Wizard.DOWNLOAD_PDF_BUTTON_XPATH).click()

    def click_download_pdf_entity_button_and_check_pdf(self, value):
        self.clear_download_directory()
        self.find_by_xpath(VenueListsConstants.Wizard.DOWNLOAD_PDF_BUTTON_XPATH).click()
        time.sleep(2)
        return self.is_pdf_contains_value(value)

    def click_on_close(self):
        self.find_by_xpath(VenueListsConstants.Wizard.CLOSE_BUTTON_XPATH).click()

    def click_on_save_changes(self):
        self.find_by_xpath(VenueListsConstants.Wizard.SAVE_CHANGES_BUTTON_XPATH).click()

    def click_on_clear_changes(self):
        self.find_by_xpath(VenueListsConstants.Wizard.CLEAR_CHANGES_BUTTON_XPATH).click()

    def set_name(self, value):
        self.set_text_by_xpath(VenueListsConstants.Wizard.NAME_XPATH, value)

    def get_name(self):
        return self.get_text_by_xpath(VenueListsConstants.Wizard.NAME_XPATH)

    def set_description(self, value):
        self.set_text_by_xpath(VenueListsConstants.Wizard.DESCRIPTION_XPATH, value)

    def get_description(self):
        return self.get_text_by_xpath(VenueListsConstants.Wizard.DESCRIPTION_XPATH)

    def set_venue_list(self, value: list):
        self.set_checkbox_list(VenueListsConstants.Wizard.VENUE_LIST_XPATH, value)

    def get_venue_list(self):
        return self.get_text_by_xpath(VenueListsConstants.Wizard.VENUE_LIST_XPATH)
