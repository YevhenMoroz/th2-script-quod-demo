import time

from test_framework.web_admin_core.pages.common_page import CommonPage
from test_framework.web_admin_core.pages.general.entitlements.constants import \
    EntitlementsConstants
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer


class EntitlementsWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def click_on_close(self):
        self.find_by_xpath(EntitlementsConstants.CLOSE_WIZARD_XPATH).click()

    def click_on_save_changes(self):
        self.find_by_xpath(EntitlementsConstants.SAVE_CHANGES_BUTTON_XPATH).click()

    def click_on_revert_changes(self):
        self.find_by_xpath(EntitlementsConstants.REVERT_CHANGES_XPATH).click()

    def click_download_pdf_entity_button_and_check_pdf(self, value):
        self.clear_download_directory()
        self.find_by_xpath(EntitlementsConstants.DOWNLOAD_PDF_BUTTON_XPATH).click()
        time.sleep(2)
        return self.is_pdf_contains_value(value)

    def is_both_desk_and_location_can_be_filled_message_displayed(self):
        return 'Both Desk and Location can not be filled' in self.find_by_xpath(
            EntitlementsConstants.BOTH_DESK_AND_LOCATION_CAN_NOT_BE_FILLED_MESSAGE_XPATH).text
