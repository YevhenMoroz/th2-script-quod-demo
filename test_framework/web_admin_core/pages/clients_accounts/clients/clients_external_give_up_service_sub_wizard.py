from test_framework.web_admin_core.pages.clients_accounts.clients.clients_constants import ClientsConstants
from test_framework.web_admin_core.pages.common_page import CommonPage
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer


class ClientsExternalGiveUpService(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def click_on_plus_button(self):
        self.find_by_xpath(ClientsConstants.ExternalGiveUpService.PLUS_BUTTON).click()

    def click_on_edit_button(self):
        self.find_by_xpath(ClientsConstants.ExternalGiveUpService.EDIT_BUTTON).click()

    def click_on_delete_button(self, confirmation: bool):
        self.find_by_xpath(ClientsConstants.ExternalGiveUpService.DELETE_BUTTON).click()
        if confirmation:
            self.find_by_xpath(ClientsConstants.OK_BUTTON_XPATH).click()

    def click_on_save_checkmark(self):
        self.find_by_xpath(ClientsConstants.ExternalGiveUpService.SAVE_CHECKMARK).click()

    def click_on_cancel_checkmark(self):
        self.find_by_xpath(ClientsConstants.ExternalGiveUpService.CANCEL_CHECKMARK).click()

    def set_name(self, value):
        self.set_text_by_xpath(ClientsConstants.ExternalGiveUpService.NAME, value)

    def get_name(self):
        return self.get_text_by_xpath(ClientsConstants.ExternalGiveUpService.NAME)

    def set_name_filter(self, value):
        self.set_text_by_xpath(ClientsConstants.ExternalGiveUpService.NAME_FILTER, value)

    def set_gateway_instance(self, value):
        self.set_text_by_xpath(ClientsConstants.ExternalGiveUpService.GATEWAY_INSTANCE, value)

    def set_gateway_instance_filter(self, value):
        self.set_text_by_xpath(ClientsConstants.ExternalGiveUpService.GATEWAY_INSTANCE_FILTER, value)

    def get_gateway_instance(self):
        return self.get_text_by_xpath(ClientsConstants.ExternalGiveUpService.GATEWAY_INSTANCE)

    def click_on_unsolicited_checkmark(self):
        self.find_by_xpath(ClientsConstants.ExternalGiveUpService.UNSOLICITED_CHECKBOX).click()

    def set_gateway_prefix(self, value):
        self.set_text_by_xpath(ClientsConstants.ExternalGiveUpService.GATEWAY_PREFIX, value)

    def get_gateway_prefix(self):
        return self.get_text_by_xpath(ClientsConstants.ExternalGiveUpService.GATEWAY_PREFIX)


