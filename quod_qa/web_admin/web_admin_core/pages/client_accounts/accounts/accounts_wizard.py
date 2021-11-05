import time

from quod_qa.web_admin.web_admin_core.pages.client_accounts.accounts.accounts_constants import AccountsConstants
from quod_qa.web_admin.web_admin_core.pages.common_page import CommonPage
from quod_qa.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer


class AccountsWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def set_id(self, value: str):
        self.set_text_by_xpath(AccountsConstants.WIZARD_ID_INPUT_XPATH, value)

    def get_id(self):
        return self.get_text_by_xpath(AccountsConstants.WIZARD_ID_INPUT_XPATH)

    def set_ext_id_client(self, value: str):
        self.set_text_by_xpath(AccountsConstants.WIZARD_EXT_ID_CLIENT_INPUT_XPATH, value)

    def get_ext_id_client(self):
        return self.get_text_by_xpath(AccountsConstants.WIZARD_EXT_ID_CLIENT_INPUT_XPATH)

    def set_client(self, value: str):
        self.set_combobox_value(AccountsConstants.WIZARD_CLIENT_COMBOBOX_XPATH, value)

    def get_client(self):
        return self.get_text_by_xpath(AccountsConstants.WIZARD_CLIENT_COMBOBOX_XPATH)

    def set_description(self, value: str):
        self.set_text_by_xpath(AccountsConstants.WIZARD_DESCRIPTION_INPUT_XPATH, value)

    def get_description(self):
        return self.get_text_by_xpath(AccountsConstants.WIZARD_DESCRIPTION_INPUT_XPATH)

    def set_position_source(self, value: str):
        self.set_combobox_value(AccountsConstants.WIZARD_POSITION_SOURCE_COMBOBOX_XPATH, value)

    def get_position_source(self):
        return self.get_text_by_xpath(AccountsConstants.WIZARD_POSITION_SOURCE_COMBOBOX_XPATH)

    def set_clearing_account_type(self, value: str):
        self.set_combobox_value(AccountsConstants.WIZARD_CLEARING_ACCOUNT_TYPE_COMBOBOX_XPATH, value)

    def get_clearing_account_type(self):
        return self.get_text_by_xpath(AccountsConstants.WIZARD_CLEARING_ACCOUNT_TYPE_COMBOBOX_XPATH)

    def set_client_id_source(self, value: str):
        self.set_combobox_value(AccountsConstants.WIZARD_CLIENT_ID_SOURCE_COMBOBOX_XPATH, value)

    def get_client_id_source(self):
        return self.get_text_by_xpath(AccountsConstants.WIZARD_CLIENT_ID_SOURCE_COMBOBOX_XPATH)

    def toggle_default_account(self):
        self.toggle_checkbox(AccountsConstants.WIZARD_DEFAULT_ACCOUNT_CHECKBOX_XPATH)

    def is_default_account_checked(self):
        return self.is_checkbox_selected(AccountsConstants.WIZARD_DEFAULT_ACCOUNT_CHECKBOX_XPATH)

    def toggle_trade_confirm_eligibility(self):
        self.toggle_checkbox(AccountsConstants.WIZARD_TRADE_CONFIRM_ELIGIBILITY_CHECKBOX_XPATH)

    def is_trade_confirm_eligibility_checked(self):
        return self.is_checkbox_selected(AccountsConstants.WIZARD_TRADE_CONFIRM_ELIGIBILITY_CHECKBOX_XPATH)

    def set_client_matching_id(self, value: str):
        self.set_text_by_xpath(AccountsConstants.WIZARD_CLIENT_MATCHING_ID_INPUT_XPATH, value)

    def get_client_matching_id(self):
        return self.get_text_by_xpath(AccountsConstants.WIZARD_CLIENT_MATCHING_ID_INPUT_XPATH)

    def set_bo_field_1(self, value: str):
        self.set_text_by_xpath(AccountsConstants.WIZARD_BO_FILED_1_INPUT_XPATH, value)

    def get_bo_field_1(self):
        return self.get_text_by_xpath(AccountsConstants.WIZARD_BO_FILED_1_INPUT_XPATH)

    def set_bo_field_2(self, value: str):
        self.set_text_by_xpath(AccountsConstants.WIZARD_BO_FILED_2_INPUT_XPATH, value)

    def get_bo_field_2(self):
        return self.get_text_by_xpath(AccountsConstants.WIZARD_BO_FILED_2_INPUT_XPATH)

    def set_bo_field_3(self, value: str):
        self.set_text_by_xpath(AccountsConstants.WIZARD_BO_FILED_3_INPUT_XPATH, value)

    def get_bo_field_3(self):
        return self.get_text_by_xpath(AccountsConstants.WIZARD_BO_FILED_3_INPUT_XPATH)

    def set_bo_field_4(self, value: str):
        self.set_text_by_xpath(AccountsConstants.WIZARD_BO_FILED_4_INPUT_XPATH, value)

    def get_bo_field_4(self):
        return self.get_text_by_xpath(AccountsConstants.WIZARD_BO_FILED_4_INPUT_XPATH)

    def set_bo_field_5(self, value: str):
        self.set_text_by_xpath(AccountsConstants.WIZARD_BO_FILED_5_INPUT_XPATH, value)

    def get_bo_field_5(self):
        return self.get_text_by_xpath(AccountsConstants.WIZARD_BO_FILED_5_INPUT_XPATH)

    def toggle_commission_exemption(self):
        self.toggle_checkbox(AccountsConstants.WIZARD_COMMISSION_EXEMPTION_CHECKBOX_XPATH)

    def is_commission_exemption_checked(self):
        return self.is_checkbox_selected(AccountsConstants.WIZARD_COMMISSION_EXEMPTION_CHECKBOX_XPATH)

    def set_counterpart(self, value: str):
        self.set_combobox_value(AccountsConstants.WIZARD_COUNTERPART_COMBOBOX_XPATH, value)

    def get_counterpart(self):
        return self.get_text_by_xpath(AccountsConstants.WIZARD_COUNTERPART_COMBOBOX_XPATH)

    def click_save_button(self):
        self.find_by_xpath(AccountsConstants.WIZARD_SAVE_BUTTON_XPATH).click()
        time.sleep(2)

    def click_download_pdf_entity_button_and_check_pdf(self, value):
        self.clear_download_directory()
        self.find_by_xpath(AccountsConstants.DOWNLOAD_PDF_BUTTON_XPATH).click()
        time.sleep(2)
        return self.is_pdf_contains_value(value)

    def is_incorrect_or_missing_value_message_displayed(self):
        if self.find_by_xpath(
                AccountsConstants.INCORRECT_OR_MISSING_VALUES_XPATH).text == "Incorrect or missing values":
            return True
        else:
            return False
