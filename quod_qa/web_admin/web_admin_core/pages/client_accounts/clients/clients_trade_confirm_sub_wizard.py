from quod_qa.web_admin.web_admin_core.pages.client_accounts.clients.clients_constants import ClientsConstants
from quod_qa.web_admin.web_admin_core.pages.common_page import CommonPage
from quod_qa.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer


class ClientsTradeConfirmSubWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def click_on_plus(self):
        self.find_by_xpath(ClientsConstants.TRADE_CONFIRM_TAB_PLUS_BUTTON_XPATH).click()

    def click_on_checkmark(self):
        self.find_by_xpath(ClientsConstants.TRADE_CONFIRM_TAB_CHECKMARK_BUTTON_XPATH).click()

    def click_on_cancel(self):
        self.find_by_xpath(ClientsConstants.TRADE_CONFIRM_TAB_CANCEL_BUTTON_XPATH).click()

    def click_on_edit(self):
        self.find_by_xpath(ClientsConstants.TRADE_CONFIRM_TAB_EDIT_BUTTON_XPATH).click()

    def click_on_delete(self):
        self.find_by_xpath(ClientsConstants.TRADE_CONFIRM_TAB_DELETE_BUTTON_XPATH).click()

    def set_trade_confirm_generation(self, value):
        self.set_combobox_value(ClientsConstants.TRADE_CONFIRM_TRADE_CONFIRM_GENERATION_XPATH, value)

    def get_trade_confirm_generation(self):
        return self.get_text_by_xpath(ClientsConstants.TRADE_CONFIRM_TRADE_CONFIRM_GENERATION_XPATH)

    def set_trade_confirm_preference(self, value):
        self.set_combobox_value(ClientsConstants.TRADE_CONFIRM_TRADE_CONFIRM_PREFERENCE_XPATH, value)

    def get_trade_confirm_preference(self):
        self.get_text_by_xpath(ClientsConstants.TRADE_CONFIRM_TRADE_CONFIRM_PREFERENCE_XPATH)

    def set_net_gross_ind_type(self, value):
        self.set_combobox_value(ClientsConstants.TRADE_CONFIRM_NET_GROSS_IND_TYPE_XPATH, value)

    def get_net_gross_ind_type(self):
        return self.get_text_by_xpath(ClientsConstants.TRADE_CONFIRM_NET_GROSS_IND_TYPE_XPATH)

    def set_email_address(self, value):
        self.set_text_by_xpath(ClientsConstants.TRADE_CONFIRM_EMAIL_ADDRESS_XPATH, value)

    def get_email_address(self):
        return self.get_text_by_xpath(ClientsConstants.TRADE_CONFIRM_EMAIL_ADDRESS_XPATH)

    def set_email_address_filter(self, value):
        self.set_text_by_xpath(ClientsConstants.TRADE_CONFIRM_EMAIL_ADDRESS_FILTER_XPATH, value)

    def set_recipient_types(self, value):
        self.set_combobox_value(ClientsConstants.TRADE_CONFIRM_RECIPIENT_TYPES_XPATH, value)

    def get_recipient_types(self):
        return self.get_text_by_xpath(ClientsConstants.TRADE_CONFIRM_RECIPIENT_TYPES_XPATH)

    def set_recipient_types_filter(self, value):
        self.set_text_by_xpath(ClientsConstants.TRADE_CONFIRM_RECIPIENT_TYPES_FILTER_XPATH, value)
