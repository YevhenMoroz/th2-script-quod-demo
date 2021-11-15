from quod_qa.web_admin.web_admin_core.pages.common_page import CommonPage
from quod_qa.web_admin.web_admin_core.pages.order_management.execution_strategies.execution_strategies_constants import \
    ExecutionStrategiesConstants
from quod_qa.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer


class ExecutionStrategiesWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    # VALUES TAB
    def set_sub_venue(self, value):
        self.set_combobox_value(ExecutionStrategiesConstants.SUB_VENUE_AT_VALUES_TAB_XPATH, value)

    def set_name(self, value):
        self.set_text_by_xpath(ExecutionStrategiesConstants.NAME_AT_VALUES_TAB_XPATH, value)

    def get_name(self):
        return self.get_text_by_xpath(ExecutionStrategiesConstants.NAME_AT_VALUES_TAB_XPATH)

    def set_strategy_type(self, value):
        self.set_combobox_value(ExecutionStrategiesConstants.STRATEGY_TYPE_AT_VALUES_TAB_XPATH, value)

    def get_strategy_type(self):
        return self.get_text_by_xpath(ExecutionStrategiesConstants.STRATEGY_TYPE_AT_VALUES_TAB_XPATH)

    def set_description(self, value):
        self.set_text_by_xpath(ExecutionStrategiesConstants.DESCRIPTION_AT_VALUES_TAB_XPATH, value)

    def get_description(self):
        return self.get_text_by_xpath(ExecutionStrategiesConstants.DESCRIPTION_AT_VALUES_TAB_XPATH)

    def set_user(self, value):
        self.set_combobox_value(ExecutionStrategiesConstants.USER_AT_VALUES_TAB_XPATH, value)

    def get_user(self):
        return self.get_text_by_xpath(ExecutionStrategiesConstants.USER_AT_VALUES_TAB_XPATH)

    def set_client(self, value):
        self.set_combobox_value(ExecutionStrategiesConstants.CLIENT_AT_VALUES_TAB_XPATH, value)

    def get_client(self):
        return self.get_text_by_xpath(ExecutionStrategiesConstants.CLIENT_AT_VALUES_TAB_XPATH)

    def set_ext_id_client(self, value):
        self.set_text_by_xpath(ExecutionStrategiesConstants.EXT_ID_CLIENT_AT_VALUES_TAB_XPATH, value)

    def get_ext_id_client(self):
        return self.get_text_by_xpath(ExecutionStrategiesConstants.EXT_ID_CLIENT_AT_VALUES_TAB_XPATH)

    def set_ext_id_venue(self, value):
        self.set_text_by_xpath(ExecutionStrategiesConstants.EXT_ID_VENUE_AT_VALUES_TAB_XPATH, value)

    def get_ext_id_venue(self):
        return self.get_text_by_xpath(ExecutionStrategiesConstants.EXT_ID_VENUE_AT_VALUES_TAB_XPATH)

    def set_aggressor_indicator(self, value):
        self.set_combobox_value(ExecutionStrategiesConstants.AGGRESSOR_INDICATOR_AT_VALUES_TAB_XPATH, value)

    def get_aggressor_indicator(self):
        return self.get_text_by_xpath(ExecutionStrategiesConstants.AGGRESSOR_INDICATOR_AT_VALUES_TAB_XPATH)

    def set_default_tif(self, value):
        self.set_combobox_value(ExecutionStrategiesConstants.DEFAULT_TIF_AT_VALUES_TAB_XPATH, value)

    def get_default_tif(self):
        return self.get_text_by_xpath(ExecutionStrategiesConstants.DEFAULT_TIF_AT_VALUES_TAB_XPATH)

    def set_default_ord_type(self, value):
        self.set_combobox_value(ExecutionStrategiesConstants.DEFAULT_ORD_TYPE_AT_VALUES_TAB_XPATH, value)

    def get_default_ord_type(self):
        return self.get_text_by_xpath(ExecutionStrategiesConstants.DEFAULT_ORD_TYPE_AT_VALUES_TAB_XPATH)

    def set_on_pegged(self):
        self.find_by_xpath(ExecutionStrategiesConstants.PEGGED_AT_VALUES_TAB_XPATH).click()

    def get_pegged(self):
        return self.is_checkbox_selected(ExecutionStrategiesConstants.PEGGED_AT_VALUES_TAB_XPATH)

    def click_on_general(self):
        self.find_by_xpath(ExecutionStrategiesConstants.GENERAL_AT_PARAMETERS_TAB_XPATH).click()

    def click_on_dark_block(self):
        self.find_by_xpath(ExecutionStrategiesConstants.DARK_AT_PARAMETERS_TAB_XPATH).click()

    def click_on_lit_general(self):
        self.find_by_xpath(ExecutionStrategiesConstants.GENERAL_IN_LIT_BLOCK_AT_PARAMETERS_TAB_XPATH).click()

    def click_on_lit_aggressive(self):
        self.find_by_xpath(ExecutionStrategiesConstants.AGGRESSIVE_IN_LIT_BLOCK_AT_PARAMETERS_TAB_XPATH).click()

    def click_on_lit_passive(self):
        self.find_by_xpath(ExecutionStrategiesConstants.PASSIVE_IN_LIT_BLOCK_AT_PARAMETERS_TAB_XPATH).click()

    def click_on_lit_sweeping(self):
        self.find_by_xpath(ExecutionStrategiesConstants.SWEEPING_IN_LIT_BLOCK_AT_PARAMETERS_TAB_XPATH).click()

    def click_on_lit_dark(self):
        self.find_by_xpath(ExecutionStrategiesConstants.DARK_IN_LIT_BLOCK_AT_PARAMETERS_TAB_XPATH).click()

    def click_on_save_changes(self):
        self.find_by_xpath(ExecutionStrategiesConstants.SAVE_CHANGES_AT_WIZARD).click()

    def click_on_revert_changes(self):
        self.find_by_xpath(ExecutionStrategiesConstants.REVERT_CHANGES_AT_WIZARD).click()

    def click_on_close_button(self):
        self.find_by_xpath(ExecutionStrategiesConstants.CLOSE_WIZARD).click()

    def get_parameter_name_at_dark_block(self):
        return self.find_by_xpath(ExecutionStrategiesConstants.PARAMETER_NAME_AT_DARK_BLOCK).text

    def get_parameter_value_at_dark_block(self):
        return self.find_by_xpath(ExecutionStrategiesConstants.PARAMETER_VALUE_AT_DARK_BLOCK).text

    def get_parameter_name_at_lit_general_block(self):
        return self.find_by_xpath(ExecutionStrategiesConstants.PARAMETER_NAME_AT_LIT_GENERAL_BLOCK).text

    def get_parameter_value_at_lit_general_block(self):
        return self.find_by_xpath(ExecutionStrategiesConstants.PARAMETER_VALUE_AT_LIT_GENERAL_BLOCK).text

    def get_parameter_name_at_lit_dark_block(self):
        return self.find_by_xpath(ExecutionStrategiesConstants.PARAMETER_NAME_AT_LIT_DARK_BLOCK).text

    def get_parameter_value_at_lit_dark_block(self):
        return self.find_by_xpath(ExecutionStrategiesConstants.PARAMETER_VALUE_AT_LIT_DARK_BLOCK).text

    def get_parameter_name_at_lit_passive_block(self):
        return self.find_by_xpath(ExecutionStrategiesConstants.PARAMETER_NAME_AT_LIT_PASSIVE_BLOCK).text

    def get_parameter_value_at_lit_passive_block(self):
        return self.find_by_xpath(ExecutionStrategiesConstants.PARAMETER_VALUE_AT_LIT_PASSIVE_BLOCK).text

    def get_parameter_name_at_lit_aggressive_block(self):
        return self.find_by_xpath(ExecutionStrategiesConstants.PARAMETER_NAME_AT_LIT_AGGRESSIVE_BLOCK).text

    def get_parameter_value_at_lit_aggressive_block(self):
        return self.find_by_xpath(ExecutionStrategiesConstants.PARAMETER_VALUE_AT_LIT_AGGRESSIVE_BLOCK).text

    def get_parameter_name_at_general_block(self):
        return self.find_by_xpath(ExecutionStrategiesConstants.PARAMETER_NAME_AT_GENERAL_BLOCK).text

    def get_parameter_value_at_general_block(self):
        return self.find_by_xpath(ExecutionStrategiesConstants.PARAMETER_VALUE_AT_GENERAL_BLOCK).text

    def get_parameter_name_at_lit_sweeping_block(self):
        return self.find_by_xpath(ExecutionStrategiesConstants.PARAMETER_NAME_AT_SWEEPING_BLOCK).text

    def get_parameter_value_at_lit_sweeping_block(self):
        return self.find_by_xpath(ExecutionStrategiesConstants.PARAMETER_VALUE_AT_SWEEPING_BLOCK).text


    def is_lit_general_existed(self):
        return "General" == self.find_by_xpath(
            ExecutionStrategiesConstants.GENERAL_IN_LIT_BLOCK_AT_PARAMETERS_TAB_XPATH).text

    def is_lit_aggressive_existed(self):
        return "Aggressive" == self.find_by_xpath(
            ExecutionStrategiesConstants.AGGRESSIVE_IN_LIT_BLOCK_AT_PARAMETERS_TAB_XPATH).text

    def is_lit_passive_existed(self):
        return "Passive" == self.find_by_xpath(
            ExecutionStrategiesConstants.PASSIVE_IN_LIT_BLOCK_AT_PARAMETERS_TAB_XPATH).text

    def is_lit_dark_existed(self):
        return "Dark" == self.find_by_xpath(
            ExecutionStrategiesConstants.DARK_DISABLED_IN_LIT_BLOCK_AT_PARAMETERS_TAB_XPATH).text

    def get_error_type_after_empty_saved(self):
        return self.find_by_xpath(ExecutionStrategiesConstants.INCORRECT_OR_MISSING_VALUES_ERROR).text

    def click_on_go_back_button(self):
        self.find_by_xpath(ExecutionStrategiesConstants.GO_BACK_BUTTON_AT_SUB_WIZARD).click()
