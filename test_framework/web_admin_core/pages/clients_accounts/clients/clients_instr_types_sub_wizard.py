from test_framework.web_admin_core.pages.clients_accounts.clients.clients_constants import ClientsConstants
from test_framework.web_admin_core.pages.common_page import CommonPage
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer


class ClientsInstrTypesSubWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def click_on_plus(self):
        self.find_by_xpath(ClientsConstants.INSTR_TYPES_TAB_PLUS_BUTTON_XPATH).click()

    def click_on_checkmark(self):
        self.find_by_xpath(ClientsConstants.INSTR_TYPES_TAB_CHECKMARK_BUTTON_XPATH).click()

    def click_on_cancel(self):
        self.find_by_xpath(ClientsConstants.INSTR_TYPES_TAB_CANCEL_BUTTON_XPATH).click()

    def click_on_edit(self):
        self.find_by_xpath(ClientsConstants.INSTR_TYPES_TAB_EDIT_BUTTON_XPATH).click()

    def click_on_delete(self):
        self.find_by_xpath(ClientsConstants.INSTR_TYPES_TAB_DELETE_BUTTON_XPATH).click()

    def set_instr_type(self, value):
        self.set_combobox_value(ClientsConstants.INSTR_TYPES_TAB_INSTR_TYPE_XPATH, value)

    def get_instr_type(self):
        return self.get_text_by_xpath(ClientsConstants.INSTR_TYPES_TAB_INSTR_TYPE_XPATH)

    def set_instr_type_filter(self, value):
        self.set_text_by_xpath(ClientsConstants.INSTR_TYPES_TAB_INSTR_TYPE_FILTER_XPATH, value)

    def set_pos_keeping_mode(self, value):
        self.set_combobox_value(ClientsConstants.INSTR_TYPES_TAB_POS_KEEPING_MODE_XPATH, value)

    def get_pos_keeping_mode(self):
        return self.get_text_by_xpath(ClientsConstants.INSTR_TYPES_TAB_POS_KEEPING_MODE_XPATH)

    def set_pos_keeping_mode_filter(self, value):
        self.set_text_by_xpath(ClientsConstants.INSTR_TYPES_TAB_POS_KEEPING_MODE_FILTER_XPATH, value)
