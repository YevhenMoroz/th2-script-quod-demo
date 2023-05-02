import time

from test_framework.web_admin_core.pages.common_page import CommonPage
from test_framework.web_admin_core.pages.positions.cash_positions.constants import Constants
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer


class MainWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def click_on_close(self):
        self.find_by_xpath(Constants.Wizard.CLOSE_WIZARD_BUTTON).click()

    def click_on_save_changes(self):
        self.find_by_xpath(Constants.Wizard.SAVE_CHANGES_BUTTON).click()

    def click_on_revert_changes(self):
        self.find_by_xpath(Constants.Wizard.REVERT_CHANGES_BUTTON).click()

    def click_download_pdf_entity_button_and_check_pdf(self, value):
        self.clear_download_directory()
        self.find_by_xpath(Constants.Wizard.DOWNLOAD_PDF_BUTTON).click()
        time.sleep(2)
        return self.is_pdf_contains_value(value)

    def get_footer_error_text(self):
        return self.find_by_xpath(Constants.Wizard.FOOTER_ERROR_TEXT)


class ValuesTab(CommonPage):
    def set_name(self, value):
        self.set_text_by_xpath(Constants.Wizard.ValuesTab.NAME, value)

    def get_name(self):
        return self.get_text_by_xpath(Constants.Wizard.ValuesTab.NAME)

    def set_client_cash_account_id(self, value):
        self.set_text_by_xpath(Constants.Wizard.ValuesTab.CLIENT_CASH_ACCOUNT_ID, value)

    def get_client_cash_account_id(self):
        return self.get_text_by_xpath(Constants.Wizard.ValuesTab.CLIENT_CASH_ACCOUNT_ID)

    def set_venue_cash_account_id(self, value):
        self.set_text_by_xpath(Constants.Wizard.ValuesTab.VENUE_CASH_ACCOUNT_ID, value)

    def get_venue_cash_account_id(self):
        return self.get_text_by_xpath(Constants.Wizard.ValuesTab.VENUE_CASH_ACCOUNT_ID)

    def set_currency(self, value):
        self.set_combobox_value(Constants.Wizard.ValuesTab.CURRENCY, value)

    def get_currency(self):
        return self.get_text_by_xpath(Constants.Wizard.ValuesTab.CURRENCY)

    def set_client(self, value):
        self.set_combobox_value(Constants.Wizard.ValuesTab.CLIENT, value)

    def get_client(self):
        return self.get_text_by_xpath(Constants.Wizard.ValuesTab.CLIENT)

    def get_all_client_from_drop_menu_by_patter(self, value):
        self.set_text_by_xpath(Constants.Wizard.ValuesTab.CLIENT, value)
        time.sleep(1)
        return self.get_all_items_from_drop_down(Constants.Wizard.DROP_DOWN_MENU)

    def set_security_accounts(self, value):
        self.set_multiselect_field_value(Constants.Wizard.ValuesTab.SECURITY_ACCOUNTS, value)

    def select_margin_account_checkbox(self):
        self.find_by_xpath(Constants.Wizard.ValuesTab.MARGIN_ACCOUNT_CHECKBOX).click()

    def select_default_cash_position_checkbox(self):
        self.find_by_xpath(Constants.Wizard.ValuesTab.DEFAULT_CASH_POSITION_CHECKBOX).click()


class PositionsTab(CommonPage):
    def get_temporary_cash(self):
        return self.find_by_xpath(Constants.Wizard.PositionsTab.TEMPORARY_CASH).text

    def get_reserved_limit(self):
        return self.find_by_xpath(Constants.Wizard.PositionsTab.RESERVED_LIMIT).text

    def get_collateral_limit(self):
        return self.find_by_xpath(Constants.Wizard.PositionsTab.COLLATERAL_LIMIT).text


