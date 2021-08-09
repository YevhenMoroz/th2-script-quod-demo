import time

from quod_qa.web_admin.web_admin_core.pages.common_page import CommonPage
from quod_qa.web_admin.web_admin_core.pages.positions.wash_book_rules.wash_book_rules_constants import \
    WashBookRulesConstants
from quod_qa.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer


class WashBookRulesWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def click_on_save_changes(self):
        self.find_by_xpath(WashBookRulesConstants.SAVE_CHANGES_XPATH).click()

    def click_on_clear_changes(self):
        self.find_by_xpath(WashBookRulesConstants.CLEAR_CHANGES_XPATH).click()

    def click_download_pdf_entity_button_and_check_pdf(self, value):
        self.clear_download_directory()
        self.find_by_xpath(WashBookRulesConstants.WIZARD_DOWNLOAD_PDF_XPATH).click()
        time.sleep(2)
        return self.is_pdf_contains_value(value)

    def click_on_close_wizard(self):
        self.find_by_xpath(WashBookRulesConstants.WIZARD_CLOSE_BUTTON_XPATH).click()

    def click_on_ok_button(self):
        self.find_by_xpath(WashBookRulesConstants.OK_BUTTON_XPATH).click()

    def click_on_no_button(self):
        self.find_by_xpath(WashBookRulesConstants.NO_BUTTON_XPATH).click()

    def click_on_cancel_button(self):
        self.find_by_xpath(WashBookRulesConstants.CANCEL_BUTTON_XPATH).click()

    # set
    def set_name(self, value):
        self.set_text_by_xpath(WashBookRulesConstants.WIZARD_NAME_XPATH, value)

    def get_name(self):
        return self.get_text_by_xpath(WashBookRulesConstants.WIZARD_NAME_XPATH)

    def set_instr_type(self, value):
        self.set_combobox_value(WashBookRulesConstants.WIZARD_INSTR_TYPE_XPATH, value)

    def get_instr_type(self):
        return self.get_text_by_xpath(WashBookRulesConstants.WIZARD_INSTR_TYPE_XPATH)

    def set_execution_policy(self, value):
        self.set_combobox_value(WashBookRulesConstants.WIZARD_EXECUTION_POLICY_XPATH, value)

    def get_execution_policy(self):
        return self.get_text_by_xpath(WashBookRulesConstants.WIZARD_EXECUTION_POLICY_XPATH)

    def set_account(self, value):
        self.set_combobox_value(WashBookRulesConstants.WIZARD_ACCOUNT_XPATH, value)

    def get_account(self):
        return self.get_text_by_xpath(WashBookRulesConstants.WIZARD_ACCOUNT_XPATH)

    def set_client(self, value):
        self.set_combobox_value(WashBookRulesConstants.WIZARD_CLIENT_XPATH, value)

    def get_client(self):
        return self.get_text_by_xpath(WashBookRulesConstants.WIZARD_CLIENT_XPATH)

    def set_user(self, value):
        self.set_combobox_value(WashBookRulesConstants.WIZARD_USER_XPATH, value)

    def get_user(self):
        return self.get_text_by_xpath(WashBookRulesConstants.WIZARD_USER_XPATH)

    def set_desk(self, value):
        self.set_combobox_value(WashBookRulesConstants.WIZARD_DESK_XPATH, value)

    def get_desk(self):
        return self.get_text_by_xpath(WashBookRulesConstants.WIZARD_DESK_XPATH)

    def is_name_field_enabled(self):
        return self.is_field_enabled(WashBookRulesConstants.WIZARD_NAME_XPATH)

    def is_incorrect_or_missing_value_message_displayed(self):
        if self.find_by_xpath(WashBookRulesConstants.INCORECT_VALUE_MESSAGE).text == "Incorrect or missing values":
            return True
        else:
            return False
