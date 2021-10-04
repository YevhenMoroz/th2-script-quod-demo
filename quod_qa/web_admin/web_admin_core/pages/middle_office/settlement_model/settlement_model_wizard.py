import time

from quod_qa.web_admin.web_admin_core.pages.common_page import CommonPage
from quod_qa.web_admin.web_admin_core.pages.middle_office.settlement_model.settlement_model_constants import \
    SettlementModelConstants

from quod_qa.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer


class SettlementModelWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def click_on_close(self):
        self.find_by_xpath(SettlementModelConstants.CLOSE_WIZARD_XPATH).click()

    def click_on_save_changes(self):
        self.find_by_xpath(SettlementModelConstants.SAVE_CHANGES_BUTTON_XPATH).click()

    def click_on_revert_changes(self):
        self.find_by_xpath(SettlementModelConstants.REVERT_CHANGES_XPATH).click()

    def click_on_go_back(self):
        self.find_by_xpath(SettlementModelConstants.GO_BACK_BUTTON_XPATH).click()

    def click_download_pdf_entity_button_and_check_pdf(self, value):
        self.clear_download_directory()
        self.find_by_xpath(SettlementModelConstants.DOWNLOAD_PDF_BUTTON_XPATH).click()
        time.sleep(2)
        return self.is_pdf_contains_value(value)

    def get_incorrect_or_missing_values_exception(self):
        return self.find_by_xpath(SettlementModelConstants.INCORRECT_OR_MISSING_VALUES_EXCEPTION).text
