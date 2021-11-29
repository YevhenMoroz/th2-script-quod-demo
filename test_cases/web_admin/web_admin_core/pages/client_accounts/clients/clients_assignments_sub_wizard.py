from test_cases.web_admin.web_admin_core.pages.client_accounts.clients.clients_constants import ClientsConstants
from test_cases.web_admin.web_admin_core.pages.common_page import CommonPage
from test_cases.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer


class ClientsAssignmentsSubWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def set_user_manager(self, value):
        self.set_text_by_xpath(ClientsConstants.ASSIGNMENTS_TAB_USER_MANAGER_XPATH, value)

    def get_user_manager(self):
        return self.get_text_by_xpath(ClientsConstants.ASSIGNMENTS_TAB_USER_MANAGER_XPATH)

    def set_desk(self, value):
        self.set_combobox_value(ClientsConstants.ASSIGNMENTS_TAB_DESK_XPATH, value)

    def get_desk(self):
        return self.get_text_by_xpath(ClientsConstants.ASSIGNMENTS_TAB_DESK_XPATH)
