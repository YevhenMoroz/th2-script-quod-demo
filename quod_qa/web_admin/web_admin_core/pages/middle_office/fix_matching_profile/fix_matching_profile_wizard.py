import time

from quod_qa.web_admin.web_admin_core.pages.common_page import CommonPage
from quod_qa.web_admin.web_admin_core.pages.middle_office.fix_matching_profile.fix_matching_profile_constants import \
    FixMatchingProfileConstants
from quod_qa.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer


class FixMatchingProfileWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def click_on_close(self):
        self.find_by_xpath(FixMatchingProfileConstants.CLOSE_WIZARD_XPATH).click()

    def click_on_save_changes(self):
        self.find_by_xpath(FixMatchingProfileConstants.SAVE_CHANGES_BUTTON_XPATH).click()

    def click_on_revert_changes(self):
        self.find_by_xpath(FixMatchingProfileConstants.REVERT_CHANGES_XPATH).click()

    def click_on_go_back(self):
        self.find_by_xpath(FixMatchingProfileConstants.GO_BACK_BUTTON_XPATH).click()

    def click_download_pdf_entity_button_and_check_pdf(self, value):
        self.clear_download_directory()
        self.find_by_xpath(FixMatchingProfileConstants.DOWNLOAD_PDF_BUTTON_XPATH).click()
        time.sleep(2)
        return self.is_pdf_contains_value(value)

    def is_incorrect_or_missing_value_message_displayed(self):
        if self.find_by_xpath(
                FixMatchingProfileConstants.INCORRECT_OR_MISSING_VALUES_XPATH).text == "Incorrect or missing values":
            return True
        else:
            return False

    def set_fix_matching_profile_name(self, value):
        self.set_text_by_xpath(FixMatchingProfileConstants.WIZARD_FIX_MATCHING_PROFILE_NAME_XPATH, value)

    def get_fix_matching_profile_name(self):
        return self.get_text_by_xpath(FixMatchingProfileConstants.WIZARD_FIX_MATCHING_PROFILE_NAME_XPATH)

    def set_avg_price_precision(self, value):
        self.set_text_by_xpath(FixMatchingProfileConstants.WIZARD_AVG_PRICE_PRECISION_XPATH, value)

    def get_avg_price_precision(self):
        return self.get_text_by_xpath(FixMatchingProfileConstants.WIZARD_AVG_PRICE_PRECISION_XPATH)

    def set_gross_tolerance(self, value):
        self.set_text_by_xpath(FixMatchingProfileConstants.WIZARD_GROSS_TOLERANCE_XPATH, value)

    def get_gross_tolerance(self):
        return self.get_text_by_xpath(FixMatchingProfileConstants.WIZARD_GROSS_TOLERANCE_XPATH)

    def set_net_tolerance(self, value):
        self.set_text_by_xpath(FixMatchingProfileConstants.WIZARD_GROSS_TOLERANCE_XPATH, value)

    def get_net_tolerance(self):
        return self.get_text_by_xpath(FixMatchingProfileConstants.WIZARD_GROSS_TOLERANCE_XPATH)

    def set_tolerance_currency(self, value):
        self.set_combobox_value(FixMatchingProfileConstants.WIZARD_TOLERANCE_CURRENCY_XPATH, value)

    def get_tolerance_currency(self):
        return self.get_text_by_xpath(FixMatchingProfileConstants.WIZARD_TOLERANCE_CURRENCY_XPATH)

    def set_net_tolerance_currency(self, value):
        self.set_combobox_value(FixMatchingProfileConstants.WIZARD_NET_TOLERANCE_CURRENCY_XPATH, value)

    def get_net_tolerance_currency(self):
        return self.get_text_by_xpath(FixMatchingProfileConstants.WIZARD_NET_TOLERANCE_CURRENCY_XPATH)

    def click_on_gross_amount(self):
        self.find_by_xpath(FixMatchingProfileConstants.WIZARD_GROSS_AMOUNT_CHECKBOX_XPATH).click()

    def click_on_net_amount(self):
        self.find_by_xpath(FixMatchingProfileConstants.WIZARD_NET_AMOUNT_CHECKBOX_XPATH).click()

    def click_on_settl_amount(self):
        self.find_by_xpath(FixMatchingProfileConstants.WIZARD_SETTL_AMOUNT_CHECKBOX_XPATH).click()

    def click_in_client_lei(self):
        self.find_by_xpath(FixMatchingProfileConstants.WIZARD_CLIENT_LEI_CHECKBOX_XPATH).click()

    def click_on_settl_date(self):
        self.find_by_xpath(FixMatchingProfileConstants.WIZARD_SETTL_DATE_CHECKBOX_XPATH).click()

    def click_on_client_bic(self):
        self.find_by_xpath(FixMatchingProfileConstants.WIZARD_CLIENT_BIC_CHECKBOX_XPATH).click()

    def click_on_client_commission(self):
        self.find_by_xpath(FixMatchingProfileConstants.WIZARD_CLIENT_COMMISSION_CHECKBOX_XPATH).click()

    def click_on_trade_date(self):
        self.find_by_xpath(FixMatchingProfileConstants.WIZARD_TRADE_DATE_CHECKBOX_XPATH).click()

    def is_gross_amount_selected(self):
        return self.is_checkbox_selected(FixMatchingProfileConstants.WIZARD_GROSS_AMOUNT_CHECKBOX_XPATH)

    def is_net_amount_selected(self):
        return self.is_checkbox_selected(FixMatchingProfileConstants.WIZARD_NET_AMOUNT_CHECKBOX_XPATH)

    def is_settl_amount_selected(self):
        return self.is_checkbox_selected(FixMatchingProfileConstants.WIZARD_SETTL_AMOUNT_CHECKBOX_XPATH)

    def is_client_lei_selected(self):
        return self.is_checkbox_selected(FixMatchingProfileConstants.WIZARD_CLIENT_LEI_CHECKBOX_XPATH)

    def is_settl_date_selected(self):
        return self.is_checkbox_selected(FixMatchingProfileConstants.WIZARD_SETTL_DATE_CHECKBOX_XPATH)

    def is_client_bic_selected(self):
        return self.is_checkbox_selected(FixMatchingProfileConstants.WIZARD_CLIENT_BIC_CHECKBOX_XPATH)

    def is_client_commission_selected(self):
        return self.is_checkbox_selected(FixMatchingProfileConstants.WIZARD_CLIENT_COMMISSION_CHECKBOX_XPATH)

    def is_trade_date_selected(self):
        return self.is_checkbox_selected(FixMatchingProfileConstants.WIZARD_TRADE_DATE_CHECKBOX_XPATH)
