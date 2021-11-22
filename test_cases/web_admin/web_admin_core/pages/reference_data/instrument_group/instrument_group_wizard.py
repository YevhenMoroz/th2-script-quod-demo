import time

from test_cases.web_admin.web_admin_core.pages.common_page import CommonPage
from test_cases.web_admin.web_admin_core.pages.reference_data.instrument_group.instrument_group_constants import \
    InstrumentGroupConstants

from test_cases.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer


class InstrumentGroupWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def click_on_close_page(self):
        self.find_by_xpath(InstrumentGroupConstants.CLOSE_WIZARD_XPATH).click()

    def click_on_save_changes(self):
        self.find_by_xpath(InstrumentGroupConstants.SAVE_CHANGES_BUTTON_XPATH).click()

    def click_on_revert_changes(self):
        self.find_by_xpath(InstrumentGroupConstants.REVERT_CHANGES_XPATH).click()

    def click_download_pdf_entity_button_and_check_pdf(self, value):
        self.clear_download_directory()
        self.find_by_xpath(InstrumentGroupConstants.DOWNLOAD_PDF_BUTTON_XPATH).click()
        time.sleep(2)
        return self.is_pdf_contains_value(value)

    def click_on_go_back_button(self):
        self.find_by_xpath(InstrumentGroupConstants.GO_BACK_BUTTON_XPATH).click()

    def set_instrument_group_name(self, value):
        self.set_text_by_xpath(InstrumentGroupConstants.WIZARD_INSTRUMENT_GROUP_NAME_XPATH, value)

    def get_instrument_group_name(self):
        return self.get_text_by_xpath(InstrumentGroupConstants.WIZARD_INSTRUMENT_GROUP_NAME_XPATH)

    def set_instr_group_description(self, value):
        self.set_text_by_xpath(InstrumentGroupConstants.WIZARD_INSTR_GROUP_DESCRIPTION_XPATH, value)

    def get_instr_group_description(self):
        return self.get_text_by_xpath(InstrumentGroupConstants.WIZARD_INSTR_GROUP_DESCRIPTION_XPATH)

    def click_on_plus(self):
        self.find_by_xpath(InstrumentGroupConstants.WIZARD_PLUS_BUTTON_XPATH).click()

    def click_on_edit(self):
        self.find_by_xpath(InstrumentGroupConstants.WIZARD_EDIT_XPATH).click()

    def click_on_delete(self):
        self.find_by_xpath(InstrumentGroupConstants.WIZARD_DELETE_XPATH).click()

    def click_on_checkmark(self):
        self.find_by_xpath(InstrumentGroupConstants.WIZARD_CHECKMARK_XPATH).click()

    def click_on_close(self):
        self.find_by_xpath(InstrumentGroupConstants.WIZARD_CLOSE_XPATH).click()

    def set_instrument_filter(self, value):
        self.set_text_by_xpath(InstrumentGroupConstants.WIZARD_INSTRUMENT_FILTER_XPATH, value)

    def set_instrument(self, value):
        self.set_combobox_value(InstrumentGroupConstants.WIZARD_INSTRUMENT_XPATH, value)

    def get_instrument(self):
        return self.get_text_by_xpath(InstrumentGroupConstants.WIZARD_INSTRUMENT_XPATH)
