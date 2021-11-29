import time

from test_cases.web_admin.web_admin_core.pages.common_page import CommonPage
from test_cases.web_admin.web_admin_core.pages.positions.cash_positions.cash_positions_constants import \
    CashPositionsConstants
from test_cases.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer


class CashPositionsWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def click_on_close(self):
        self.find_by_xpath(CashPositionsConstants.CLOSE_WIZARD_XPATH).click()

    def click_on_save_changes(self):
        self.find_by_xpath(CashPositionsConstants.SAVE_CHANGES_BUTTON_XPATH).click()

    def click_on_revert_changes(self):
        self.find_by_xpath(CashPositionsConstants.REVERT_CHANGES_XPATH).click()

    def click_on_go_back(self):
        self.find_by_xpath(CashPositionsConstants.GO_BACK_BUTTON_XPATH).click()

    def click_download_pdf_entity_button_and_check_pdf(self, value):
        self.clear_download_directory()
        self.find_by_xpath(CashPositionsConstants.DOWNLOAD_PDF_BUTTON_XPATH).click()
        time.sleep(2)
        return self.is_pdf_contains_value(value)

    def is_incorrect_or_missing_value_message_displayed(self):
        if self.find_by_xpath(
                CashPositionsConstants.INCORRECT_OR_MISSING_VALUES_XPATH).text == "Incorrect or missing values":
            return True
        else:
            return False

    def set_name(self, value):
        self.set_text_by_xpath(CashPositionsConstants.WIZARD_NAME_XPATH, value)

    def get_name(self):
        return self.get_text_by_xpath(CashPositionsConstants.WIZARD_NAME_XPATH)

    def set_client_cash_account_id(self, value):
        self.set_text_by_xpath(CashPositionsConstants.WIZARD_CLIENT_CASH_ACCOUNT_ID_XPATH, value)

    def get_client_cash_account_id(self):
        return self.get_text_by_xpath(CashPositionsConstants.WIZARD_CLIENT_CASH_ACCOUNT_ID_XPATH)

    def set_venue_cash_account_id(self, value):
        self.set_text_by_xpath(CashPositionsConstants.WIZARD_VENUE_CASH_ACCOUNT_ID_XPATH, value)

    def get_venue_cash_account_id(self):
        return self.get_text_by_xpath(CashPositionsConstants.WIZARD_VENUE_CASH_ACCOUNT_ID_XPATH)

    def set_currency(self, value):
        self.set_combobox_value(CashPositionsConstants.WIZARD_CURRENCY_XPATH, value)

    def get_currency(self):
        return self.get_text_by_xpath(CashPositionsConstants.WIZARD_CURRENCY_XPATH)

    def set_client(self, value):
        self.set_combobox_value(CashPositionsConstants.WIZARD_CLIENT_XPATH, value)

    def get_client(self):
        return self.get_text_by_xpath(CashPositionsConstants.WIZARD_CLIENT_XPATH)
