from quod_qa.web_admin.web_admin_core.pages.common_page import CommonPage
from quod_qa.web_admin.web_admin_core.pages.general.admin_command.admin_command_constants import AdminCommandConstants

from quod_qa.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer


class AdminCommandPage(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def set_admin_command(self, value):
        self.set_combobox_value(AdminCommandConstants.ADMIN_COMMAND_XPATH, value)

    def get_admin_command(self):
        return self.get_text_by_xpath(AdminCommandConstants.ADMIN_COMMAND_XPATH)

    def set_component_id(self, value):
        self.set_text_by_xpath(AdminCommandConstants.COMPONENT_ID_XPATH, value)

    def get_component_id(self):
        return self.get_text_by_xpath(AdminCommandConstants.COMPONENT_ID_XPATH)

    def click_on_plus(self):
        self.find_by_xpath(AdminCommandConstants.PLUS_BUTTON_XPATH).click()

    def click_on_checkmark(self):
        self.find_by_xpath(AdminCommandConstants.CHECKMARK_BUTTON_XPATH).click()

    def click_on_close(self):
        self.find_by_xpath(AdminCommandConstants.CLOSE_BUTTON_XPATH).click()

    def click_on_edit(self):
        self.find_by_xpath(AdminCommandConstants.EDIT_BUTTON_XPATH).click()

    def click_on_delete(self):
        self.find_by_xpath(AdminCommandConstants.DELETE_BUTTON_XPATH).click()

    def set_name(self, value):
        self.set_text_by_xpath(AdminCommandConstants.NAME_XPATH, value)

    def set_value(self, value):
        self.set_text_by_xpath(AdminCommandConstants.VALUE_XPATH, value)

    def click_on_send(self):
        self.find_by_xpath(AdminCommandConstants.SEND_BUTTON_XPATH).click()

    def is_error_displayed(self):
        error_name = "Request failed, verify the input data. If the problem persists, please contact the administrator for full details"
        return error_name == self.find_by_xpath(AdminCommandConstants.ERROR_XPATH).text
