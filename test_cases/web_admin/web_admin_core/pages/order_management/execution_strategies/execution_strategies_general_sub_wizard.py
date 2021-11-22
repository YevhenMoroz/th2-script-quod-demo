from test_cases.web_admin.web_admin_core.pages.common_page import CommonPage
from test_cases.web_admin.web_admin_core.pages.order_management.execution_strategies.execution_strategies_constants import \
    ExecutionStrategiesConstants
from test_cases.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer


class ExecutionStrategiesGeneralSubWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def click_on_plus_button(self):
        self.find_by_xpath(ExecutionStrategiesConstants.PLUS_BUTTON_AT_PARAMETERS_SUB_WIZARD).click()

    def click_on_cancel_button(self):
        self.find_by_xpath(ExecutionStrategiesConstants.CANCEL_BUTTON_AT_PARAMETERS_SUB_WIZARD).click()

    def click_on_checkmark_button(self):
        self.find_by_xpath(ExecutionStrategiesConstants.CHECKMARK_BUTTON_AT_PARAMETERS_SUB_WIZARD).click()

    def click_on_delete_button(self):
        self.find_by_xpath(ExecutionStrategiesConstants.DELETE_BUTTON_AT_PARAMETERS_SUB_WIZARD).click()

    def click_on_go_back_button(self):
        self.find_by_xpath(ExecutionStrategiesConstants.GO_BACK_BUTTON_AT_SUB_WIZARD).click()

    def click_on_ok_button(self):
        self.find_by_xpath(ExecutionStrategiesConstants.OK_BUTTON_XPATH).click()

    # checkboxes
    def set_on_visible_checkbox(self):
        self.find_by_xpath(ExecutionStrategiesConstants.VISIBLE_CHECKBOX_AT_PARAMETERS_SUB_WIZARD).click()

    def set_on_editable_checkbox(self):
        self.find_by_xpath(ExecutionStrategiesConstants.EDITABLE_CHECKBOX_AT_PARAMETERS_SUB_WIZARD).click()

    def set_on_required_checkbox(self):
        self.find_by_xpath(ExecutionStrategiesConstants.REQUIRED_CHECKBOX_AT_PARAMETERS_SUB_WIZARD).click()

    # data at right corner
    def set_parameter(self, value):
        self.set_combobox_value(ExecutionStrategiesConstants.PARAMETER_FIELD_AT_PARAMETERS_SUB_WIZARD, value)

    def set_value_at_sub_wizard(self, value):
        self.set_text_by_xpath(ExecutionStrategiesConstants.VALUE_FIELD_AT_PARAMETERS_SUB_WIZARD, value)

    def set_value_by_dropdown_list_at_sub_wizard(self, value):
        self.set_combobox_value(ExecutionStrategiesConstants.VALUE_FIELD_AT_PARAMETERS_SUB_WIZARD, value)

    def get_value_at_sub_wizard(self):
        return self.get_text_by_xpath(ExecutionStrategiesConstants.VALUE_FIELD_AT_PARAMETERS_SUB_WIZARD)

    def set_checkbox_at_sub_wizard(self):
        self.find_by_xpath(ExecutionStrategiesConstants.CHECKBOX_FOR_ALL_PARAMETERS_AT_SUB_WIZARD).click()

    def get_checkbox_value_at_sub_wizard(self):
        self.is_checkbox_selected(ExecutionStrategiesConstants.CHECKBOX_FOR_ALL_PARAMETERS_AT_SUB_WIZARD)

    def set_start_time_at_sub_wizard(self, value):
        self.set_combobox_value(ExecutionStrategiesConstants.START_TIME_AT_SUB_WIZARD, value)

    def get_start_time_at_sub_wizard(self):
        self.get_text_by_xpath(ExecutionStrategiesConstants.START_TIME_AT_SUB_WIZARD)

    def set_plus_or_minus_at_sub_wizard(self, value):
        self.set_text_by_xpath(ExecutionStrategiesConstants.PLUS_AND_MINUS_AT_SUB_WIZARD, value)

    def set_offset_at_sub_wizard(self, value):
        self.set_text_by_xpath(ExecutionStrategiesConstants.OFFSET_AT_SUB_WIZARD, value)

    def get_offset_at_sub_wizard(self):
        self.get_text_by_xpath(ExecutionStrategiesConstants.OFFSET_AT_SUB_WIZARD)

    def set_absolute_value_at_sub_wizard(self, value):
        self.set_text_by_xpath(ExecutionStrategiesConstants.ABSOLUTE_VALUE_AT_SUB_WIZARD, value)

    def get_absolute_value_at_sub_wizard(self):
        self.get_text_by_xpath(ExecutionStrategiesConstants.ABSOLUTE_VALUE_AT_SUB_WIZARD)

    def get_error_type_after_empty_saved(self):
        return self.find_by_xpath(ExecutionStrategiesConstants.INCORRECT_OR_MISSING_VALUES_ERROR).text