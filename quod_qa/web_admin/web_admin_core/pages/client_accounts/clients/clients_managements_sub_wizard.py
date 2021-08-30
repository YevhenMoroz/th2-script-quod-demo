from quod_qa.web_admin.web_admin_core.pages.client_accounts.clients.clients_constants import ClientsConstants
from quod_qa.web_admin.web_admin_core.pages.common_page import CommonPage
from quod_qa.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer


class ClientsManagementsSubWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def set_user_manager(self, value):
        self.set_combobox_value(ClientsConstants.MANAGEMENTS_TAB_USER_MANAGER_XPATH, value)

    def get_user_manager(self):
        return self.get_text_by_xpath(ClientsConstants.MANAGEMENTS_TAB_USER_MANAGER_XPATH)

    def set_desk_manager(self, value):
        self.set_combobox_value(ClientsConstants.MANAGEMENTS_TAB_DESK_MANAGER_XPATH, value)

    def get_desk_manager(self):
        return self.get_text_by_xpath(ClientsConstants.MANAGEMENTS_TAB_DESK_MANAGER_XPATH)

    def set_fix_order_recipient_user(self, value):
        self.set_combobox_value(ClientsConstants.MANAGEMENTS_TAB_FIX_ORDER_RECIPIENT_USER_XPATH, value)

    def get_fix_order_recipient_user(self):
        return self.get_text_by_xpath(ClientsConstants.MANAGEMENTS_TAB_FIX_ORDER_RECIPIENT_USER_XPATH)

    def set_fix_order_recipient_desk(self, value):
        self.set_combobox_value(ClientsConstants.MANAGEMENTS_TAB_FIX_ORDER_RECIPIENT_DESK_XPATH, value)

    def get_fix_order_recipient_desk(self):
        return self.get_text_by_xpath(ClientsConstants.MANAGEMENTS_TAB_FIX_ORDER_RECIPIENT_DESK_XPATH)

    def set_beneficiary_desk(self, value):
        self.set_combobox_value(ClientsConstants.MANAGEMENTS_TAB_BENEFICIARY_DESK_XPATH, value)

    def get_beneficiary_desk(self):
        return self.get_text_by_xpath(ClientsConstants.MANAGEMENTS_TAB_BENEFICIARY_DESK_XPATH)

    def set_middle_office_user(self, value):
        self.set_combobox_value(ClientsConstants.MANAGEMENTS_TAB_MIDDLE_OFFICE_USER_XPATH, value)

    def get_middle_office_user(self):
        return self.get_text_by_xpath(ClientsConstants.MANAGEMENTS_TAB_MIDDLE_OFFICE_USER_XPATH)

    def set_middle_office_desk(self, value):
        self.set_combobox_value(ClientsConstants.MANAGEMENTS_TAB_MIDDLE_OFFICE_DESK_XPATH, value)

    def get_middle_office_desk(self):
        return self.get_text_by_xpath(ClientsConstants.MANAGEMENTS_TAB_MIDDLE_OFFICE_DESK_XPATH)
