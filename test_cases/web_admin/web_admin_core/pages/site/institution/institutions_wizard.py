import time

from test_cases.web_admin.web_admin_core.pages.common_page import CommonPage
from test_cases.web_admin.web_admin_core.pages.site.institution.institutions_constants import InstitutionsConstants
from test_cases.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer


class InstitutionsWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def click_on_close(self):
        self.find_by_xpath(InstitutionsConstants.CLOSE_WIZARD_XPATH).click()

    def click_on_save_changes(self):
        self.find_by_xpath(InstitutionsConstants.SAVE_CHANGES_BUTTON_XPATH).click()

    def click_on_revert_changes(self):
        self.find_by_xpath(InstitutionsConstants.REVERT_CHANGES_XPATH).click()

    def click_on_go_back(self):
        self.find_by_xpath(InstitutionsConstants.GO_BACK_BUTTON_XPATH).click()

    def click_download_pdf_entity_button_and_check_pdf(self, value):
        self.clear_download_directory()
        self.find_by_xpath(InstitutionsConstants.DOWNLOAD_PDF_BUTTON_XPATH).click()
        time.sleep(2)
        return self.is_pdf_contains_value(value)

    def is_such_record_exists_massage_displayed(self):
        if self.find_by_xpath(
                InstitutionsConstants.SUCH_RECORD_ALREADY_EXISTS_MASSEGE_XPATH).text == "Such a record already exists":
            return True
        else:
            return False

    def click_on_ok_button(self):
        self.find_by_xpath(InstitutionsConstants.OK_BUTTON_XPATH).click()

    def click_on_no_button(self):
        self.find_by_xpath(InstitutionsConstants.NO_BUTTON_XPATH).click()

    def click_on_cancel(self):
        self.find_by_xpath(InstitutionsConstants.CANCEL_BUTTON_XPATH).click()
