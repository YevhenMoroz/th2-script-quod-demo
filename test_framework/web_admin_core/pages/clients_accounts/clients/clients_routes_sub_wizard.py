from test_framework.web_admin_core.pages.clients_accounts.clients.clients_constants import ClientsConstants
from test_framework.web_admin_core.pages.common_page import CommonPage
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer


class ClientsRoutesSubWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def click_on_plus(self):
        self.find_by_xpath(ClientsConstants.ROUTES_TAB_PLUS_BUTTON_XPATH).click()

    def click_on_checkmark(self):
        self.find_by_xpath(ClientsConstants.ROUTES_TAB_CHECKMARK_BUTTON_XPATH).click()

    def click_on_cancel(self):
        self.find_by_xpath(ClientsConstants.ROUTES_TAB_CANCEL_BUTTON_XPATH).click()

    def click_on_edit(self):
        self.find_by_xpath(ClientsConstants.ROUTES_TAB_EDIT_BUTTON_XPATH).click()

    def click_on_delete(self):
        self.find_by_xpath(ClientsConstants.ROUTES_TAB_DELETE_BUTTON_XPATH).click()

    def set_route(self, value):
        self.set_combobox_value(ClientsConstants.ROUTES_TAB_ROUTE_XPATH, value)

    # for future: get_route_in_edit_mode
    def get_route(self):
        return self.get_text_by_xpath(ClientsConstants.ROUTES_TAB_ROUTE_XPATH)

    def get_route_in_table(self):
        return self.find_by_xpath(ClientsConstants.ROUTES_TAB_ROUTE_TABLE).text

    def set_route_filter(self, value):
        self.set_text_by_xpath(ClientsConstants.ROUTES_TAB_ROUTE_FILTER_XPATH, value)

    def set_route_client_name(self, value):
        self.set_text_by_xpath(ClientsConstants.ROUTES_TAB_ROUTE_CLIENT_NAME_XPATH, value)

    def get_route_client_name(self):
        return self.get_text_by_xpath(ClientsConstants.ROUTES_TAB_ROUTE_CLIENT_NAME_XPATH)

    def set_route_client_name_filter(self, value):
        self.set_text_by_xpath(ClientsConstants.ROUTES_TAB_ROUTE_CLIENT_NAME_FILTER_XPATH, value)

    def click_on_agent_fee_exemption_checkbox(self):
        self.find_by_xpath(ClientsConstants.ROUTES_TAB_ROUTE_AGENT_FEE_EXEMPTION).click()

    def is_agent_fee_exemption_selected(self):
        return self.is_checkbox_selected(ClientsConstants.ROUTES_TAB_ROUTE_AGENT_FEE_EXEMPTION)

    def is_route_present(self):
        return self.is_element_present(ClientsConstants.DELETE_XPATH)
