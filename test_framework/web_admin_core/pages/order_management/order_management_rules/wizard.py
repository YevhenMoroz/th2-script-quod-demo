import time

from test_framework.web_admin_core.pages.common_page import CommonPage
from test_framework.web_admin_core.pages.order_management.order_management_rules.constants import Constants


class MainWizard(CommonPage):
    def click_on_save_changes(self):
        self.find_by_xpath(Constants.Wizard.SAVE_CHANGES_BUTTON).click()

    def click_on_revert_changes(self):
        self.find_by_xpath(Constants.Wizard.REVERT_CHANGES).click()

    def click_on_close_page(self, confirmation):
        self.find_by_xpath(Constants.Wizard.CLOSE_WIZARD_BUTTON).click()
        if confirmation:
            self.find_by_xpath(Constants.Wizard.OK_BUTTON).click()
        else:
            self.find_by_xpath(Constants.Wizard.CANCEL_BUTTON).click()

    def click_download_pdf_entity_button_and_check_pdf(self, value):
        self.clear_download_directory()
        self.find_by_xpath(Constants.Wizard.DOWNLOAD_PDF_BUTTON).click()
        time.sleep(2)
        return self.is_pdf_contains_value(value)

    def get_footer_error_text(self):
        return self.find_by_xpath(Constants.Wizard.FOOTER_ERROR).text

    def is_footer_error_displayed(self):
        return self.is_element_present(Constants.Wizard.FOOTER_ERROR)


class ValuesTab(CommonPage):
    def set_name(self, value):
        self.set_text_by_xpath(Constants.ValuesTab.NAME, value)

    def get_name(self):
        return self.get_text_by_xpath(Constants.ValuesTab.NAME)

    def set_description(self, value):
        self.set_text_by_xpath(Constants.ValuesTab.DESCRIPTION, value)

    def get_description(self):
        return self.get_text_by_xpath(Constants.ValuesTab.DESCRIPTION)


class ResultTable(CommonPage):
    def click_on_plus_button_at_result(self):
        self.find_by_xpath(Constants.ResultsTable.PLUS_BUTTON).click()

    def click_on_save_checkmark_at_result(self):
        self.find_by_xpath(Constants.ResultsTable.CHECKMARK_BUTTON).click()

    def click_on_cancel_button_at_result(self):
        self.find_by_xpath(Constants.ResultsTable.CANCEL_BUTTON).click()

    def click_on_edit_button_at_result(self):
        self.find_by_xpath(Constants.ResultsTable.EDIT_BUTTON).click()

    def click_on_delete_button_at_result(self):
        self.find_by_xpath(Constants.ResultsTable.DELETE_BUTTON).click()

    def set_action_filter(self, value):
        self.set_text_by_xpath(Constants.ResultsTable.ACTION, value)

    def set_action(self, value):
        self.set_combobox_value(Constants.ResultsTable.ACTION, value)

    def get_action(self):
        self.get_text_by_xpath(Constants.ResultsTable.ACTION)

    def set_rule(self, value):
        self.set_combobox_value(Constants.ResultsTable.RULE, value)

    def get_rule(self):
        return self.get_text_by_xpath(Constants.ResultsTable.RULE)

    def set_rejection_type(self, value):
        self.set_combobox_value(Constants.ResultsTable.REJECTION_TYPE, value)

    def get_rejection_type(self):
        return self.get_text_by_xpath(Constants.ResultsTable.REJECTION_TYPE)

    def set_split(self, value):
        self.set_text_by_xpath(Constants.ResultsTable.SPLIT, value)

    def get_split(self):
        return self.get_text_by_xpath(Constants.ResultsTable.SPLIT)

    def set_price_origin(self, value):
        self.set_combobox_value(Constants.ResultsTable.PRICE_ORIGIN, value)

    def get_price_origin(self):
        return self.get_text_by_xpath(Constants.ResultsTable.PRICE_ORIGIN)

    def set_split_qty_precision(self, value):
        self.set_text_by_xpath(Constants.ResultsTable.PRICE_ORIGIN, value)

    def get_split_qty_precision(self):
        return self.get_text_by_xpath(Constants.ResultsTable.PRICE_ORIGIN)

    def set_venue(self, value):
        self.set_combobox_value(Constants.ResultsTable.VENUE, value)

    def get_venue(self):
        return self.get_text_by_xpath(Constants.ResultsTable.VENUE)

    def set_route(self, value):
        self.set_combobox_value(Constants.ResultsTable.ROUTE, value)

    def get_route(self):
        return self.get_text_by_xpath(Constants.ResultsTable.ROUTE)

    def set_execution_strategy(self, value):
        self.set_combobox_value(Constants.ResultsTable.EXECUTION_STRATEGY, value)

    def get_execution_strategy(self):
        return self.get_text_by_xpath(Constants.ResultsTable.EXECUTION_STRATEGY)

    def set_child_strategy(self, value):
        self.set_combobox_value(Constants.ResultsTable.CHILD_STRATEGY, value)

    def get_child_strategy(self):
        return self.get_text_by_xpath(Constants.ResultsTable.CHILD_STRATEGY)

    def set_property(self, value):
        if self.find_by_xpath(Constants.ResultsTable.PROPERTY_VALUE).tag_name == 'input':
            self.set_text_by_xpath(Constants.ResultsTable.PROPERTY_VALUE, value)
        elif self.find_by_xpath(Constants.ResultsTable.PROPERTY_VALUE).tag_name == 'button':
            self.set_checkbox_list(Constants.ResultsTable.PROPERTY_VALUE, value)


class ConditionsTab(ResultTable):
    def click_on_plus_button(self):
        self.find_by_xpath(Constants.ConditionsTab.PLUS_BUTTON).click()

    def click_on_save_checkmark(self):
        self.find_by_xpath(Constants.ConditionsTab.SAVE_BUTTON).click()

    def click_on_cancel_button(self):
        self.find_by_xpath(Constants.ConditionsTab.CANCEL_BUTTON).click()

    def click_on_edit_button(self):
        self.find_by_xpath(Constants.ConditionsTab.EDIT_BUTTON).click()

    def click_on_toggle_button(self, confirmation: bool):
        self.find_by_xpath(Constants.ConditionsTab.TOGGLE_BUTTON).click()
        if confirmation:
            self.find_by_xpath(Constants.Wizard.OK_BUTTON).click()

    def is_condition_enabled(self):
        return self.is_toggle_button_enabled(Constants.ConditionsTab.TOGGLE_BUTTON)

    def click_on_up_button(self):
        self.find_by_xpath(Constants.ConditionsTab.UP_BUTTON).click()

    def click_on_down_button(self):
        self.find_by_xpath(Constants.ConditionsTab.DOWN_BUTTON).click()

    def set_name_filter(self, value):
        self.set_text_by_xpath(Constants.ConditionsTab.NAME_FILTER, value)

    def set_name(self, value):
        self.set_text_by_xpath(Constants.ConditionsTab.NAME, value)

    def get_name(self):
        return self.get_text_by_xpath(Constants.ConditionsTab.NAME)

    def click_on_add_condition_button(self):
        self.find_by_xpath(Constants.ConditionLogic.ADD_CONDITION_BUTTON).click()

    def click_on_add_condition_set_button(self):
        self.find_by_xpath(Constants.ConditionLogic.ADD_CONDITION_SET_BUTTON).click()

    def set_condition_criteria(self, value):
        self.select_value_from_dropdown_list(Constants.ConditionLogic.CRITERIA, value)

    def get_condition_criteria(self):
        return self.get_text_by_xpath(Constants.ConditionLogic.CRITERIA)

    def set_condition_logic(self, value):
        self.select_value_from_dropdown_list(Constants.ConditionLogic.LOGIC, value)

    def get_condition_logic(self):
        return self.get_text_by_xpath(Constants.ConditionLogic.LOGIC)

    def set_condition_value(self, value):
        if self.is_element_present(Constants.ConditionLogic.VALUE):
            if self.find_by_xpath(Constants.ConditionLogic.VALUE).get_attribute('type') == 'number':
                self.set_text_by_xpath(Constants.ConditionLogic.VALUE, value)
            else:
                self.set_combobox_value(Constants.ConditionLogic.VALUE, value)
        else:
            self.set_checkbox_list(Constants.ConditionLogic.VALUE_CHECKBOXES, value)

    def get_condition_value(self):
        if self.is_element_present(Constants.ConditionLogic.VALUE):
            return self.get_text_by_xpath(Constants.ConditionLogic.VALUE)
        return self.get_text_by_xpath(Constants.ConditionLogic.VALUE_CHECKBOXES)

    def click_on_close_condition_button(self):
        self.find_by_xpath(Constants.ConditionLogic.CLOSE_BUTTON).click()


class DefaultResultEntity(ResultTable):
    def click_on_edit_button(self):
        self.find_by_xpath(Constants.DefaultResult.EDIT_BUTTON).click()

    def click_on_save_checkmark(self):
        self.find_by_xpath(Constants.DefaultResult.CHECKMARK_BUTTON).click()

    def click_on_cancel_button(self):
        self.find_by_xpath(Constants.DefaultResult.CANCEL_BUTTON).click()

    def set_name(self, value):
        self.set_text_by_xpath(Constants.DefaultResult.NAME, value)

    def get_name(self):
        return self.get_text_by_xpath(Constants.DefaultResult.NAME)
