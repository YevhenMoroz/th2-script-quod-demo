import time

from quod_qa.web_admin.web_admin_core.pages.common_page import CommonPage
from quod_qa.web_admin.web_admin_core.pages.order_management.execution_strategies.execution_strategies_constants import \
    ExecutionStrategiesConstants
from quod_qa.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer


class ExecutionStrategiesPage(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    # change criteria
    def click_on_change_criteria(self):
        self.find_by_xpath(ExecutionStrategiesConstants.CHANGE_CRITERIA_AT_MAIN_MENU_XPATH).click()

    def click_on_change_criteria_for_saving(self):
        self.find_by_xpath(ExecutionStrategiesConstants.SAVE_CHANGE_CRITERIA_AT_MAIN_MENU_XPATH).click()

    def set_first_criteria(self, value):
        self.set_combobox_value(ExecutionStrategiesConstants.FIRST_CRITERIA_FIELD_AT_CHANGE_CRITERIA_TAB_XPATH, value)

    def set_second_criteria(self, value):
        self.set_combobox_value(ExecutionStrategiesConstants.SECOND_CRITERIA_FIELD_AT_CHANGE_CRITERIA_TAB_XPATH, value)

    # left menu
    def click_on_enable_disable_button(self):
        self.find_by_xpath(ExecutionStrategiesConstants.ENABLE_DISABLE_BUTTON_XPATH).click()

    def click_on_more_actions(self):
        self.find_by_xpath(ExecutionStrategiesConstants.MORE_ACTIONS_BUTTON_XPATH).click()

    def click_on_edit_at_more_actions(self):
        self.find_by_xpath(ExecutionStrategiesConstants.EDIT_AT_MORE_ACTIONS_XPATH).click()

    def click_on_clone_at_more_actions(self):
        self.find_by_xpath(ExecutionStrategiesConstants.CLONE_AT_MORE_ACTIONS_XPATH).click()

    def click_download_pdf_entity_button_and_check_pdf(self, value: str):
        self.clear_download_directory()
        self.find_by_xpath(ExecutionStrategiesConstants.DOWNLOAD_PDF_AT_MORE_ACTIONS_XPATH).click()
        time.sleep(2)
        return self.is_pdf_contains_value(value)

    def click_on_pin_row_at_more_actions(self):
        self.find_by_xpath(ExecutionStrategiesConstants.PIN_TO_ROW_AT_MORE_ACTIONS_XPATH).click()

    def click_on_ok_button(self):
        self.find_by_xpath(ExecutionStrategiesConstants.OK_BUTTON_XPATH).click()

    # -------------
    def click_on_new_button(self):
        self.find_by_xpath(ExecutionStrategiesConstants.NEW_BUTTON_AT_MAIN_MENU_XPATH).click()

    def set_name_at_filter_field(self, value):
        self.set_text_by_xpath(ExecutionStrategiesConstants.NAME_FILTER_AT_MAIN_MENU_XPATH, value)

    def get_name_value(self):
        return self.find_by_xpath(ExecutionStrategiesConstants.NAME_VALUE_AT_MAIN_MENU_XPATH).text

    def set_description_at_filter_field(self, value):
        self.set_text_by_xpath(ExecutionStrategiesConstants.DESCRIPTION_FILTER_AT_MAIN_MENU_XPATH, value)

    def get_description_value(self):
        return self.find_by_xpath(ExecutionStrategiesConstants.DESCRIPTION_VALUE_AT_MAIN_MENU_XPATH).text

    def set_strategy_type_at_filter_field(self, value):
        self.set_text_by_xpath(ExecutionStrategiesConstants.STRATEGY_TYPE_FILTER_AT_MAIN_MENU_XPATH, value)

    def get_strategy_type_value(self):
        return self.find_by_xpath(ExecutionStrategiesConstants.STRATEGY_TYPE_VALUE_AT_MAIN_MENU_XPATH).text

    def set_ext_id_client_at_filter_field(self, value):
        self.set_text_by_xpath(ExecutionStrategiesConstants.EXT_ID_CLIENT_FILTER_AT_MAIN_MENU_XPATH, value)

    # def get_ext_id_client_value(self):
    #     pass

    def set_ext_id_venue_at_filter_field(self, value):
        self.set_text_by_xpath(ExecutionStrategiesConstants.EXT_ID_VENUE_FILTER_AT_MAIN_MENU_XPATH, value)

    # def get_ext_id_venue_at_filter_field(self):
    #     pass

    def set_user_at_filter_field(self, value):
        self.set_text_by_xpath(ExecutionStrategiesConstants.USER_FILTER_AT_MAIN_MENU_XPATH, value)

    # def get_user_value(self):
    #     pass

    def set_client_at_filter_field(self, value):
        self.set_text_by_xpath(ExecutionStrategiesConstants.CLIENT_FILTER_AT_MAIN_MENU_XPATH, value)

    # def get_client_value(self):
    #     pass
    def set_enabled_at_filter_field(self, value):
        self.select_value_from_dropdown_list(ExecutionStrategiesConstants.ENABLED_FILTER_AT_MAIN_MENU_XPATH, value)

        # self.find_by_xpath(ExecutionStrategiesConstants.ENABLED_FILTER_AT_MAIN_MENU_XPATH).select_by_value(value)
