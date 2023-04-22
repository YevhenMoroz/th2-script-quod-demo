from test_framework.web_admin_core.pages.common_page import CommonPage
from test_framework.web_admin_core.pages.general.system_commands.system_commands_constants import SystemCommandsConstants

from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer


class SystemCommandsPage(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def set_system_commands(self, value):
        self.select_value_from_dropdown_list(SystemCommandsConstants.SYSTEM_COMMANDS_XPATH, value)

    def get_system_commands(self):
        return self.get_text_by_xpath(SystemCommandsConstants.SYSTEM_COMMANDS_XPATH)

    def set_component_id(self, value):
        self.set_text_by_xpath(SystemCommandsConstants.COMPONENT_ID_XPATH, value)

    def get_component_id(self):
        return self.get_text_by_xpath(SystemCommandsConstants.COMPONENT_ID_XPATH)

    def click_on_plus(self):
        self.find_by_xpath(SystemCommandsConstants.PLUS_BUTTON_XPATH).click()

    def click_on_checkmark(self):
        self.find_by_xpath(SystemCommandsConstants.CHECKMARK_BUTTON_XPATH).click()

    def click_on_close(self):
        self.find_by_xpath(SystemCommandsConstants.CLOSE_BUTTON_XPATH).click()

    def click_on_edit(self):
        self.find_by_xpath(SystemCommandsConstants.EDIT_BUTTON_XPATH).click()

    def click_on_delete(self):
        self.find_by_xpath(SystemCommandsConstants.DELETE_BUTTON_XPATH).click()

    def set_name(self, value):
        self.set_text_by_xpath(SystemCommandsConstants.NAME_XPATH, value)

    def set_value(self, value):
        self.set_text_by_xpath(SystemCommandsConstants.VALUE_XPATH, value)

    def click_on_send(self):
        self.find_by_xpath(SystemCommandsConstants.SEND_BUTTON_XPATH).click()

    def is_error_displayed(self):
        return self.is_element_present(SystemCommandsConstants.ERROR_XPATH)

    def is_command_field_displayed(self):
        return self.is_element_present(SystemCommandsConstants.SYSTEM_COMMANDS_XPATH)
