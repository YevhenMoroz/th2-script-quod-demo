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


class AssignmentsTab(CommonPage):
    def set_institution(self, value):
        self.set_combobox_value(Constants.Wizard.AssignmentsTab.INSTITUTION_FIELD, value)

    def get_institution(self):
        return self.get_text_by_xpath(Constants.Wizard.AssignmentsTab.INSTITUTION_FIELD)


class CashValuesTab(CommonPage):
    def set_cash_checkbox(self):
        self.find_by_xpath(Constants.Wizard.CashValuesTab.CASH_CHECKBOX).click()

    def is_cash_checkbox_selected(self):
        return self.is_checkbox_selected(Constants.Wizard.CashValuesTab.CASH_CHECKBOX)

    def set_temporary_cash_checkbox(self):
        self.find_by_xpath(Constants.Wizard.CashValuesTab.TEMPORARY_CASH_CHECKBOX).click()

    def is_temporary_cash_checkbox_selected(self):
        return self.is_checkbox_selected(Constants.Wizard.CashValuesTab.TEMPORARY_CASH_CHECKBOX)


class SecurityValuesTab(CommonPage):
    def set_trade_on_margin_checkbox(self):
        self.find_by_xpath(Constants.Wizard.SecurityValuesTab.TRADE_ON_MARGIN_CHECKBOX).click()

    def is_trade_on_margin_checkbox_selected(self):
        return self.is_checkbox_selected(Constants.Wizard.SecurityValuesTab.TRADE_ON_MARGIN_CHECKBOX)

    def set_global_margin(self, value):
        self.set_text_by_xpath(Constants.Wizard.SecurityValuesTab.GLOBAL_MARGIN_FIELD, value)

    def get_global_margin(self):
        return self.get_text_by_xpath(Constants.Wizard.SecurityValuesTab.GLOBAL_MARGIN_FIELD)

    # Table
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

    def set_instrument_type_filter(self, value):
        self.set_text_by_xpath(Constants.Wizard.SecurityValuesTab.Table.INSTRUMENT_TYPE_FILTER, value)

    def set_instrument_group_filter(self, value):
        self.set_text_by_xpath(Constants.Wizard.SecurityValuesTab.Table.INSTRUMENT_GROUP_FILTER, value)

    def set_underlying_listing_filter(self, value):
        self.set_text_by_xpath(Constants.Wizard.SecurityValuesTab.Table.UNDERLYING_LISTING_FILTER, value)

    def set_haircut_value_filter(self, value):
        self.set_text_by_xpath(Constants.Wizard.SecurityValuesTab.Table.HAIRCUT_VALUE_FILTER, value)

    def set_instrument_type(self, value):
        self.set_combobox_value(Constants.Wizard.SecurityValuesTab.Table.INSTRUMENT_TYPE_FIELD, value)

    def get_instrument_type(self):
        return self.get_text_by_xpath(Constants.Wizard.SecurityValuesTab.Table.INSTRUMENT_TYPE_FIELD)

    def set_instrument_group(self, value):
        self.set_combobox_value(Constants.Wizard.SecurityValuesTab.Table.INSTRUMENT_GROUP_FIELD, value)

    def get_instrument_group(self):
        return self.get_text_by_xpath(Constants.Wizard.SecurityValuesTab.Table.INSTRUMENT_GROUP_FIELD)

    def set_underlying_listing(self, value):
        self.set_combobox_value(Constants.Wizard.SecurityValuesTab.Table.UNDERLYING_LISTING_FIELD, value)

    def get_underlying_listing(self):
        return self.get_text_by_xpath(Constants.Wizard.SecurityValuesTab.Table.UNDERLYING_LISTING_FIELD)

    def set_haircut_value(self, value):
        self.set_text_by_xpath(Constants.Wizard.SecurityValuesTab.Table.HAIRCUT_VALUE_FIELD, value)

    def get_haircut_value(self):
        return self.get_text_by_xpath(Constants.Wizard.SecurityValuesTab.Table.HAIRCUT_VALUE_FIELD)


class RiskMarginTab(CommonPage):
    # Table
    def click_on_plus_in_table(self):
        self.find_by_xpath(Constants.Wizard.RiskMarginTab.Table.PLUS_BUTTON).click()

    def click_on_save_checkmark_in_table(self):
        self.find_by_xpath(Constants.Wizard.RiskMarginTab.Table.SAVE_CHECKMARK_BUTTON).click()

    def click_on_cancel_in_table(self):
        self.find_by_xpath(Constants.Wizard.RiskMarginTab.Table.CANCEL_BUTTON).click()

    def click_on_edit_in_table(self):
        self.find_by_xpath(Constants.Wizard.RiskMarginTab.Table.EDIT_BUTTON).click()

    def click_on_delete_in_table(self):
        self.find_by_xpath(Constants.Wizard.RiskMarginTab.Table.DELETE_BUTTON).click()

    def set_margin_method_filter(self, value):
        self.set_text_by_xpath(Constants.Wizard.RiskMarginTab.Table.MARGIN_METHOD_FILTER, value)

    def set_initial_margin_filter(self, value):
        self.set_text_by_xpath(Constants.Wizard.RiskMarginTab.Table.INITIAL_MARGIN_FILTER, value)

    def set_maintenance_margin_filter(self, value):
        self.set_text_by_xpath(Constants.Wizard.RiskMarginTab.Table.MAINTENANCE_MARGIN_FILTER, value)

    def set_instrument_type_filter(self, value):
        self.set_text_by_xpath(Constants.Wizard.RiskMarginTab.Table.INSTRUMENT_TYPE_FILTER, value)

    def set_instrument_group_filter(self, value):
        self.set_text_by_xpath(Constants.Wizard.RiskMarginTab.Table.INSTRUMENT_GROUP_FILTER, value)

    def set_instrument_filter(self, value):
        self.set_text_by_xpath(Constants.Wizard.RiskMarginTab.Table.INSTRUMENT_FILTER, value)

    def set_underlying_instrument_filter(self, value):
        self.set_text_by_xpath(Constants.Wizard.RiskMarginTab.Table.UNDERLYING_INSTRUMENT_FILTER, value)

    def set_margin_method(self, value):
        self.set_combobox_value(Constants.Wizard.RiskMarginTab.Table.MARGIN_METHOD_FIELD, value)

    def get_margin_method(self):
        return self.get_text_by_xpath(Constants.Wizard.RiskMarginTab.Table.MARGIN_METHOD_FIELD)

    def set_initial_margin(self, value):
        self.set_text_by_xpath(Constants.Wizard.RiskMarginTab.Table.INITIAL_MARGIN_FIELD, value)

    def get_initial_margin(self):
        return self.get_text_by_xpath(Constants.Wizard.RiskMarginTab.Table.INITIAL_MARGIN_FIELD)

    def set_maintenance_margin(self, value):
        self.set_text_by_xpath(Constants.Wizard.RiskMarginTab.Table.MAINTENANCE_MARGIN_FIELD, value)

    def get_maintenance_margin(self):
        return self.get_text_by_xpath(Constants.Wizard.RiskMarginTab.Table.MAINTENANCE_MARGIN_FIELD)

    def set_instrument_type(self, value):
        self.set_combobox_value(Constants.Wizard.RiskMarginTab.Table.INSTRUMENT_TYPE_FIELD, value)

    def get_instrument_type(self):
        return self.get_text_by_xpath(Constants.Wizard.RiskMarginTab.Table.INSTRUMENT_TYPE_FIELD)

    def set_instrument_group(self, value):
        self.set_combobox_value(Constants.Wizard.RiskMarginTab.Table.INSTRUMENT_GROUP_FIELD, value)

    def get_instrument_group(self):
        return self.get_text_by_xpath(Constants.Wizard.RiskMarginTab.Table.INSTRUMENT_GROUP_FIELD)

    def set_instrument(self, value):
        self.set_combobox_value(Constants.Wizard.RiskMarginTab.Table.INSTRUMENT_FIELD, value)

    def get_instrument(self):
        return self.get_text_by_xpath(Constants.Wizard.RiskMarginTab.Table.INSTRUMENT_FIELD)

    def set_underlying_instrument(self, value):
        self.set_combobox_value(Constants.Wizard.RiskMarginTab.Table.UNDERLYING_INSTRUMENT_FIELD, value)

    def get_underlying_instrument(self):
        return self.get_text_by_xpath(Constants.Wizard.RiskMarginTab.Table.UNDERLYING_INSTRUMENT_FIELD)
