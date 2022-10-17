import time

from test_framework.web_admin_core.pages.common_page import CommonPage
from test_framework.web_admin_core.pages.risk_limits.buying_power.constants import Constants
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer


class MainWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def click_on_close(self):
        self.find_by_xpath(Constants.Wizard.CLOSE_BUTTON).click()

    def click_on_ok_button(self):
        self.find_by_xpath(Constants.Wizard.OK_BUTTON).click()

    def click_on_cancel_button(self):
        self.find_by_xpath(Constants.Wizard.CANCEL_BUTTON).click()

    def click_on_save_changes(self):
        self.find_by_xpath(Constants.Wizard.SAVE_CHANGES_BUTTON).click()

    def click_on_revert_changes(self):
        self.find_by_xpath(Constants.Wizard.REVERT_CHANGES).click()

    def click_on_clear_changes(self):
        self.find_by_xpath(Constants.Wizard.CLEAR_CHANGES_BUTTON).click()

    def click_download_pdf_entity_button_and_check_pdf(self, value):
        self.clear_download_directory()
        self.find_by_xpath(Constants.Wizard.DOWNLOAD_PDF_BUTTON).click()
        time.sleep(1)
        return self.is_pdf_contains_value(value)


class ValuesTab(CommonPage):
    def set_name(self, value):
        self.set_text_by_xpath(Constants.Wizard.ValuesTab.NAME_FIELD, value)

    def get_name(self):
        return self.get_text_by_xpath(Constants.Wizard.ValuesTab.NAME_FIELD)

    def set_description(self, value):
        self.set_text_by_xpath(Constants.Wizard.ValuesTab.DESCRIPTION_FIELD, value)

    def get_description(self):
        return self.get_text_by_xpath(Constants.Wizard.ValuesTab.DESCRIPTION_FIELD)


class CashValuesTab(CommonPage):
    def set_cash_checkbox(self):
        self.find_by_xpath(Constants.Wizard.CashValuesTab.CASH_CHECKBOX).click()

    def is_cash_checkbox_selected(self):
        return self.is_checkbox_selected(Constants.Wizard.CashValuesTab.CASH_CHECKBOX)

    def set_temporary_cash_checkbox(self):
        self.find_by_xpath(Constants.Wizard.CashValuesTab.TEMPORARY_CASH_CHECKBOX).click()

    def is_temporary_cash_checkbox_selected(self):
        return self.is_checkbox_selected(Constants.Wizard.CashValuesTab.TEMPORARY_CASH_CHECKBOX)

    def set_cash_loan_checkbox(self):
        self.find_by_xpath(Constants.Wizard.CashValuesTab.CASH_LOAN_CHECKBOX).click()

    def is_cash_loan_checkbox_selected(self):
        return self.is_checkbox_selected(Constants.Wizard.CashValuesTab.CASH_LOAN_CHECKBOX)

    def set_collateral_checkbox(self):
        self.find_by_xpath(Constants.Wizard.CashValuesTab.COLLATERAL_CHECKBOX).click()

    def is_collateral_checkbox_selected(self):
        return self.is_checkbox_selected(Constants.Wizard.CashValuesTab.COLLATERAL_CHECKBOX)

    def set_allow_collateral_on_negative_ledger_checkbox(self):
        self.find_by_xpath(Constants.Wizard.CashValuesTab.ALLOW_COLLATERAL_ON_NEGATIVE_LEADER_CHECKBOX).click()

    def is_allow_collateral_on_negative_ledger_checkbox_selected(self):
        return self.is_checkbox_selected(Constants.Wizard.CashValuesTab.ALLOW_COLLATERAL_ON_NEGATIVE_LEADER_CHECKBOX)


class SecurityValuesTab(CommonPage):
    def set_include_securities_checkbox(self):
        self.find_by_xpath(Constants.Wizard.SecurityValuesTab.INCLUDE_SECURITIES_CHECKBOX).click()

    def is_include_securities_checkbox_selected(self):
        return self.is_checkbox_selected(Constants.Wizard.SecurityValuesTab.INCLUDE_SECURITIES_CHECKBOX)

    def set_reference_value(self, value):
        self.set_combobox_value(Constants.Wizard.SecurityValuesTab.REFERENCE_VALUE_FIELD, value)

    def get_reference_value(self):
        return self.get_text_by_xpath(Constants.Wizard.SecurityValuesTab.REFERENCE_VALUE_FIELD)

    def get_all_reference_value_from_drop_menu(self):
        self.set_text_by_xpath(Constants.Wizard.SecurityValuesTab.REFERENCE_VALUE_FIELD, "")
        time.sleep(1)
        return self.get_all_items_from_drop_down(Constants.Wizard.DROP_DOWN_MENU)

    def clear_reference_value(self):
        self.set_text_by_xpath(Constants.Wizard.SecurityValuesTab.REFERENCE_VALUE_FIELD, "")

    def is_reference_value_field_empty(self):
        return False if "has-value" in self.find_by_xpath(Constants.Wizard.SecurityValuesTab.REFERENCE_VALUE_FIELD)\
            .get_attribute("class") else True

    def set_holdings_ratio(self, value):
        self.set_text_by_xpath(Constants.Wizard.SecurityValuesTab.HOLDINGS_RATIO_FIELD, value)

    def get_holding_ratio(self):
        return self.get_text_by_xpath(Constants.Wizard.SecurityValuesTab.HOLDINGS_RATIO_FIELD)

    def is_holding_ratio_field_empty(self):
        return False if "has-value" in self.find_by_xpath(Constants.Wizard.SecurityValuesTab.HOLDINGS_RATIO_FIELD)\
            .get_attribute("class") else True

    def set_allow_securities_on_negative_ledgers_checkbox(self):
        self.find_by_xpath(Constants.Wizard.SecurityValuesTab.ALLOW_SECURITIES_ON_NEGATIVE_LEDGERS_CHECKBOX).click()

    def is_allow_securities_on_negative_ledgers_checkbox_selected(self):
        return self.is_checkbox_selected(Constants.Wizard.SecurityValuesTab.ALLOW_SECURITIES_ON_NEGATIVE_LEDGERS_CHECKBOX)

    def set_disallow_for_same_listing_checkbox(self):
        self.find_by_xpath(Constants.Wizard.SecurityValuesTab.DISALLOW_FOR_SAME_LISTING_CHECKBOX).click()

    def is_disallow_for_same_listing_checkbox_selected(self):
        return self.is_checkbox_selected(Constants.Wizard.SecurityValuesTab.DISALLOW_FOR_SAME_LISTING_CHECKBOX)

    def set_disallow_for_deliverable_contracts_checkbox(self):
        self.find_by_xpath(Constants.Wizard.SecurityValuesTab.DISALLOW_FOR_DELIVERABLE_CONTRACTS_CHECKBOX).click()

    def is_disallow_for_deliverable_contracts_checkbox_selected(self):
        return self.is_checkbox_selected(Constants.Wizard.SecurityValuesTab.DISALLOW_FOR_DELIVERABLE_CONTRACTS_CHECKBOX)

    # Security Values table
    def click_on_plus_in_table(self):
        self.find_by_xpath(Constants.Wizard.SecurityValuesTab.Table.PLUS_BUTTON).click()

    def click_on_save_checkmark_in_table(self):
        self.find_by_xpath(Constants.Wizard.SecurityValuesTab.Table.SAVE_CHECKMARK_BUTTON).click()

    def click_on_cancel_in_table(self):
        self.find_by_xpath(Constants.Wizard.SecurityValuesTab.Table.CANCEL_BUTTON).click()

    def click_on_edit_in_table(self):
        self.find_by_xpath(Constants.Wizard.SecurityValuesTab.Table.EDIT_BUTTON).click()

    def click_on_delete_in_table(self):
        self.find_by_xpath(Constants.Wizard.SecurityValuesTab.Table.DELETE_BUTTON).click()

    def set_settlement_period_filter(self, value):
        self.set_text_by_xpath(Constants.Wizard.SecurityValuesTab.Table.SETTLEMENT_PERIOD_FILTER, value)

    def set_position_validity_filter(self, value):
        self.set_text_by_xpath(Constants.Wizard.SecurityValuesTab.Table.POSITION_VALIDITY_FILTER, value)

    def set_margin_method_filter(self, value):
        self.set_text_by_xpath(Constants.Wizard.SecurityValuesTab.Table.MARGIN_METHOD_FILTER, value)

    def set_custom_percentage_filter(self, value):
        self.set_text_by_xpath(Constants.Wizard.SecurityValuesTab.Table.CUSTOM_PERCENTAGE_FILTER, value)

    def set_settlement_period(self, value):
        self.set_combobox_value(Constants.Wizard.SecurityValuesTab.Table.SETTLEMENT_PERIOD_FIELD, value)

    def get_settlement_period(self):
        return self.get_text_by_xpath(Constants.Wizard.SecurityValuesTab.Table.SETTLEMENT_PERIOD_FIELD)

    def set_position_validity(self, value):
        self.set_combobox_value(Constants.Wizard.SecurityValuesTab.Table.POSITION_VALIDITY_FIELD, value)

    def get_position_validity(self):
        return self.get_text_by_xpath(Constants.Wizard.SecurityValuesTab.Table.POSITION_VALIDITY_FIELD)

    def set_margin_method(self, value):
        self.set_combobox_value(Constants.Wizard.SecurityValuesTab.Table.MARGIN_METHOD_FIELD, value)

    def get_margin_method(self):
        return self.get_text_by_xpath(Constants.Wizard.SecurityValuesTab.Table.MARGIN_METHOD_FIELD)

    def set_custom_percentage(self, value):
        self.set_text_by_xpath(Constants.Wizard.SecurityValuesTab.Table.CUSTOM_PERCENTAGE_FIELD, value)

    def get_custom_percentage(self):
        self.get_text_by_xpath(Constants.Wizard.SecurityValuesTab.Table.CUSTOM_PERCENTAGE_FIELD)
