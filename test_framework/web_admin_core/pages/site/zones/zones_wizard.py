import time

from test_framework.web_admin_core.pages.common_page import CommonPage
from test_framework.web_admin_core.pages.site.zones.zones_constants import ZonesConstants

from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer


class ZonesWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def click_on_close(self):
        self.find_by_xpath(ZonesConstants.CLOSE_WIZARD_XPATH).click()

    def click_on_save_changes(self):
        self.find_by_xpath(ZonesConstants.SAVE_CHANGES_BUTTON_XPATH).click()

    def click_on_revert_changes(self):
        self.find_by_xpath(ZonesConstants.REVERT_CHANGES_XPATH).click()

    def click_on_go_back(self):
        self.find_by_xpath(ZonesConstants.GO_BACK_BUTTON_XPATH).click()

    def click_download_pdf_entity_button_and_check_pdf(self, value):
        self.clear_download_directory()
        self.find_by_xpath(ZonesConstants.DOWNLOAD_PDF_BUTTON_XPATH).click()
        time.sleep(2)
        return self.is_pdf_contains_value(value)

    def is_incorrect_or_missing_value_message_displayed(self):
        if self.find_by_xpath(
                ZonesConstants.INCORRECT_OR_MISSING_VALUES_MESSAGE_XPATH).text == "Incorrect or missing values":
            return True
        else:
            return False

    def click_on_ok_button(self):
        self.find_by_xpath(ZonesConstants.OK_BUTTON_XPATH).click()

    def click_on_no_button(self):
        self.find_by_xpath(ZonesConstants.NO_BUTTON_XPATH).click()

    def click_on_cancel(self):
        self.find_by_xpath(ZonesConstants.CANCEL_BUTTON_XPATH).click()

    def is_such_record_exists_massage_displayed(self):
        if self.find_by_xpath(
                ZonesConstants.SUCH_RECORD_ALREADY_EXISTS_MASSEGE_XPATH).text == "Such a record already exists":
            return True
        else:
            return False

    def is_wizard_open(self):
        return self.is_element_present(ZonesConstants.ZONES_WIZARD_PAGE_TITLE_XPATH)

    def is_leave_page_confirmation_pop_up_displayed(self):
        return self.is_element_present(ZonesConstants.CONFIRMATION_POP_UP)
