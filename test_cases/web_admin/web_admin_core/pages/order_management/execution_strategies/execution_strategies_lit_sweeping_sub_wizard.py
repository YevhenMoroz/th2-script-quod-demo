from test_cases.web_admin.web_admin_core.pages.common_page import CommonPage
from test_cases.web_admin.web_admin_core.pages.order_management.execution_strategies.execution_strategies_constants import \
    ExecutionStrategiesConstants
from test_cases.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer


class ExecutionStrategiesLitSweepingSubWizard(CommonPage):
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

    def set_parameter(self, value):
        self.set_combobox_value(ExecutionStrategiesConstants.PARAMETER_FIELD_AT_PARAMETERS_SUB_WIZARD, value)

    def get_parameter(self):
        self.get_text_by_xpath(ExecutionStrategiesConstants.PARAMETER_FIELD_AT_PARAMETERS_SUB_WIZARD)

    # checkboxes
    def set_visible_checkbox(self):
        self.find_by_xpath(ExecutionStrategiesConstants.VISIBLE_CHECKBOX_AT_PARAMETERS_SUB_WIZARD).click()

    def get_visible_checkbox(self):
        self.is_checkbox_selected(ExecutionStrategiesConstants.VISIBLE_CHECKBOX_AT_PARAMETERS_SUB_WIZARD)

    def set_editable_checkbox(self):
        self.find_by_xpath(ExecutionStrategiesConstants.EDITABLE_CHECKBOX_AT_PARAMETERS_SUB_WIZARD).click()

    def get_editable_checkbox(self):
        self.is_checkbox_selected(ExecutionStrategiesConstants.EDITABLE_CHECKBOX_AT_PARAMETERS_SUB_WIZARD)

    def set_required_checkbox(self):
        self.find_by_xpath(ExecutionStrategiesConstants.REQUIRED_CHECKBOX_AT_PARAMETERS_SUB_WIZARD).click()

    def get_required_checkbox(self):
        return self.is_checkbox_selected(
            ExecutionStrategiesConstants.REQUIRED_CHECKBOX_AT_PARAMETERS_SUB_WIZARD)

    # ----
    def set_checkbox(self):
        self.find_by_xpath(ExecutionStrategiesConstants.CHECKBOX_FOR_ALL_PARAMETERS_AT_SUB_WIZARD).click()

    def get_checkbox(self):
        self.is_checkbox_selected(ExecutionStrategiesConstants.CHECKBOX_FOR_ALL_PARAMETERS_AT_SUB_WIZARD)

    def set_value(self, value):
        self.set_text_by_xpath(ExecutionStrategiesConstants.VALUE_FIELD_AT_PARAMETERS_SUB_WIZARD, value)

    def set_value_by_dropdown_list_at_sub_wizard(self, value):
        self.set_combobox_value(ExecutionStrategiesConstants.VALUE_FIELD_AT_PARAMETERS_SUB_WIZARD, value)

    # --Actions sub wizard

    def set_venue_at_actions_sub_wizard(self, value):
        self.set_combobox_value(ExecutionStrategiesConstants.VENUE_FIELD_AT_ACTIONS_SUB_WIZARD, value)

    def get_venue_at_actions_sub_wizard(self):
        self.get_text_by_xpath(ExecutionStrategiesConstants.VENUE_FIELD_AT_ACTIONS_SUB_WIZARD)

    def click_on_plus_at_actions_sub_wizard(self):
        self.find_by_xpath(ExecutionStrategiesConstants.PLUS_BUTTON_AT_ACTIONS_SUB_WIZARD).click()

    def click_on_checkmark_at_actions_sub_wizard(self):
        self.find_by_xpath(ExecutionStrategiesConstants.CHECKMARK_BUTTON_AT_ACTIONS_SUB_WIZARD).click()

    def click_on_cancel_at_actions_sub_wizard(self):
        self.find_by_xpath(ExecutionStrategiesConstants.CANCEL_BUTTON_AT_ACTIONS_SUB_WIZARD).click()

    def click_on_delete_at_actions_sub_wizard(self):
        self.find_by_xpath(ExecutionStrategiesConstants.DELETE_BUTTON_AT_ACTIONS_SUB_WIZARD).click()