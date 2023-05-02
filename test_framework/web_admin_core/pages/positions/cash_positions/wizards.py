import time

from test_framework.web_admin_core.pages.common_page import CommonPage
from test_framework.web_admin_core.pages.positions.cash_positions.constants import Constants
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer


class MainWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def click_on_close(self):
        self.find_by_xpath(Constants.Wizard.CLOSE_WIZARD_BUTTON).click()

    def click_on_ok_button(self):
        self.find_by_xpath(Constants.Wizard.OK_BUTTON).click()

    def is_confirmation_of_leave_wizard_displayed(self):
        return self.is_element_present(Constants.Wizard.LEAVE_CONFIRMATION_POP_UP)

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

    def get_security_accounts(self):
        return self.find_by_xpath(Constants.Wizard.ValuesTab.SECURITY_ACCOUNTS_VALUES).text

    def is_security_account_displayed_by_pattern(self, sec_acc_name=None):
        if not self.is_element_present(Constants.Wizard.MULTISELECT_FORM_LOOK_UP):
            self.find_by_xpath(Constants.Wizard.ValuesTab.SECURITY_ACCOUNTS).click()
        if sec_acc_name is None:
            return self.is_element_present(Constants.Wizard.MULTISELECT_FORM_NO_RESULT_TEXT)
        else:
            self.set_text_by_xpath(Constants.Wizard.MULTISELECT_FORM_LOOK_UP, sec_acc_name)
            time.sleep(1)
            return self.is_element_present(Constants.Wizard.MULTISELECT_FORM_ITEM)

    def select_margin_account_checkbox(self):
        self.find_by_xpath(Constants.Wizard.ValuesTab.MARGIN_ACCOUNT_CHECKBOX).click()

    def is_margin_account_checkbox_selected(self):
        return self.is_checkbox_selected(Constants.Wizard.ValuesTab.MARGIN_ACCOUNT_CHECKBOX)

    def is_margin_account_checkbox_enabled(self):
        return self.is_checkbox_enabled(Constants.Wizard.ValuesTab.MARGIN_ACCOUNT_CHECKBOX)

    def select_default_cash_position_checkbox(self):
        self.find_by_xpath(Constants.Wizard.ValuesTab.DEFAULT_CASH_POSITION_CHECKBOX).click()

    def is_default_cash_position_checkbox_selected(self):
        return self.is_checkbox_selected(Constants.Wizard.ValuesTab.DEFAULT_CASH_POSITION_CHECKBOX)

    def get_warning_message(self):
        return self.find_by_xpath(Constants.Wizard.ValuesTab.WARNING_MESSAGE).text

    def is_warning_message_displayed(self):
        return self.is_element_present(Constants.Wizard.ValuesTab.WARNING_MESSAGE)


class PositionsTab(CommonPage):
    def get_actual_balance(self):
        return self.find_by_xpath(Constants.Wizard.PositionsTab.ACTUAL_BALANCE).text

    def get_initial_balance(self):
        return self.find_by_xpath(Constants.Wizard.PositionsTab.INITIAL_BALANCE).text

    def get_unsettled_sell_amount(self):
        return self.find_by_xpath(Constants.Wizard.PositionsTab.UNSETTLED_SELL_AMOUNT).text

    def get_cash_deposited(self):
        return self.find_by_xpath(Constants.Wizard.PositionsTab.CASH_DEPOSITED).text

    def get_cash_loan(self):
        return self.find_by_xpath(Constants.Wizard.PositionsTab.CASH_LOAN).text

    def get_temporary_cash(self):
        return self.find_by_xpath(Constants.Wizard.PositionsTab.TEMPORARY_CASH).text

    def get_collateral(self):
        return self.find_by_xpath(Constants.Wizard.PositionsTab.COLLATERAL).text

    def get_available_balance(self):
        return self.find_by_xpath(Constants.Wizard.PositionsTab.AVAILABLE_BALANCE).text

    def get_reserved_amount(self):
        return self.find_by_xpath(Constants.Wizard.PositionsTab.RESERVED_AMOUNT).text

    def get_unsettled_buy_amount(self):
        return self.find_by_xpath(Constants.Wizard.PositionsTab.UNSETTLED_BUY_AMOUNT).text

    def get_cash_withdrawn(self):
        return self.find_by_xpath(Constants.Wizard.PositionsTab.CASH_WITHDRAWN).text

    def get_cash_held_by_transactions(self):
        return self.find_by_xpath(Constants.Wizard.PositionsTab.CASH_HELD_BY_TRANSACTIONS).text

    def get_booked_cash_loan(self):
        return self.find_by_xpath(Constants.Wizard.PositionsTab.BOOKED_CASH_LOAN).text

    def get_booked_temporary_cash(self):
        return self.find_by_xpath(Constants.Wizard.PositionsTab.BOOKED_TEMPORARY_CASH).text

    def get_booked_collateral(self):
        return self.find_by_xpath(Constants.Wizard.PositionsTab.BOOKED_COLLATERAL).text
