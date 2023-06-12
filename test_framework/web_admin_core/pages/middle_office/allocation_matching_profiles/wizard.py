import time

from test_framework.web_admin_core.pages.common_page import CommonPage
from test_framework.web_admin_core.pages.middle_office.allocation_matching_profiles.constants import \
    Constants
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer


class AllocationMatchingProfilesWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def click_on_close(self):
        self.find_by_xpath(Constants.Wizard.CLOSE_WIZARD).click()

    def click_on_save_changes(self):
        self.find_by_xpath(Constants.Wizard.SAVE_CHANGES_BUTTON).click()

    def click_on_revert_changes(self):
        self.find_by_xpath(Constants.Wizard.REVERT_CHANGES).click()

    def click_download_pdf_entity_button_and_check_pdf(self, value):
        self.clear_download_directory()
        self.find_by_xpath(Constants.Wizard.DOWNLOAD_PDF_BUTTON).click()
        time.sleep(2)
        return self.is_pdf_contains_value(value)

    def is_incorrect_or_missing_value_message_displayed(self):
        if self.find_by_xpath(
                Constants.Wizard.INCORRECT_OR_MISSING_VALUES).text == "Incorrect or missing values":
            return True
        return False

    def set_name(self, value):
        self.set_text_by_xpath(Constants.ValuesTab.NAME, value)

    def get_name(self):
        return self.get_text_by_xpath(Constants.ValuesTab.NAME)

    def set_avg_price_precision(self, value):
        self.set_text_by_xpath(Constants.MatchingFieldsTab.AVG_PRICE_PRECISION, value)

    def get_avg_price_precision(self):
        return self.get_text_by_xpath(Constants.MatchingFieldsTab.AVG_PRICE_PRECISION)

    def set_gross_tolerance(self, value):
        self.set_text_by_xpath(Constants.MatchingFieldsTab.GROSS_TOLERANCE, value)

    def get_gross_tolerance(self):
        return self.get_text_by_xpath(Constants.MatchingFieldsTab.GROSS_TOLERANCE)

    def set_net_tolerance(self, value):
        self.set_text_by_xpath(Constants.MatchingFieldsTab.NET_TOLERANCE, value)

    def get_net_tolerance(self):
        return self.get_text_by_xpath(Constants.MatchingFieldsTab.NET_TOLERANCE)

    def set_tolerance_currency(self, value):
        self.set_combobox_value(Constants.MatchingFieldsTab.TOLERANCE_CURRENCY, value)

    def get_tolerance_currency(self):
        return self.get_text_by_xpath(Constants.MatchingFieldsTab.TOLERANCE_CURRENCY)

    def set_net_tolerance_currency(self, value):
        self.set_combobox_value(Constants.MatchingFieldsTab.NET_TOLERANCE_CURRENCY, value)

    def get_net_tolerance_currency(self):
        return self.get_text_by_xpath(Constants.MatchingFieldsTab.NET_TOLERANCE_CURRENCY)

    def click_on_gross_amount_checkbox(self):
        self.find_by_xpath(Constants.MatchingFieldsTab.GROSS_AMOUNT_CHECKBOX).click()

    def click_on_net_amount_checkbox(self):
        self.find_by_xpath(Constants.MatchingFieldsTab.NET_AMOUNT_CHECKBOX).click()

    def click_on_settl_amount_checkbox(self):
        self.find_by_xpath(Constants.MatchingFieldsTab.SETTL_AMOUNT_CHECKBOX).click()

    def click_in_client_lei_checkbox(self):
        self.find_by_xpath(Constants.MatchingFieldsTab.CLIENT_LEI_CHECKBOX).click()

    def click_on_settl_date_checkbox(self):
        self.find_by_xpath(Constants.MatchingFieldsTab.SETTL_DATE_CHECKBOX).click()

    def click_on_client_bic_checkbox(self):
        self.find_by_xpath(Constants.MatchingFieldsTab.CLIENT_BIC_CHECKBOX).click()

    def click_on_client_commission_checkbox(self):
        self.find_by_xpath(Constants.MatchingFieldsTab.CLIENT_COMMISSION_CHECKBOX).click()

    def click_on_trade_date_checkbox(self):
        self.find_by_xpath(Constants.MatchingFieldsTab.TRADE_DATE_CHECKBOX).click()

    def is_gross_amount_checkbox_selected(self):
        return self.is_checkbox_selected(Constants.MatchingFieldsTab.GROSS_AMOUNT_CHECKBOX)

    def is_net_amount_checkbox_selected(self):
        return self.is_checkbox_selected(Constants.MatchingFieldsTab.NET_AMOUNT_CHECKBOX)

    def is_settl_amount_checkbox_selected(self):
        return self.is_checkbox_selected(Constants.MatchingFieldsTab.SETTL_AMOUNT_CHECKBOX)

    def is_client_lei_checkbox_selected(self):
        return self.is_checkbox_selected(Constants.MatchingFieldsTab.CLIENT_LEI_CHECKBOX)

    def is_settl_date_checkbox_selected(self):
        return self.is_checkbox_selected(Constants.MatchingFieldsTab.SETTL_DATE_CHECKBOX)

    def is_client_bic_checkbox_selected(self):
        return self.is_checkbox_selected(Constants.MatchingFieldsTab.CLIENT_BIC_CHECKBOX)

    def is_client_commission_checkbox_selected(self):
        return self.is_checkbox_selected(Constants.MatchingFieldsTab.CLIENT_COMMISSION_CHECKBOX)

    def is_trade_date_checkbox_selected(self):
        return self.is_checkbox_selected(Constants.MatchingFieldsTab.TRADE_DATE_CHECKBOX)
