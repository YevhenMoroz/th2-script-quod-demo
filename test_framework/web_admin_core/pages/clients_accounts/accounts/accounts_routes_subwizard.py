from test_framework.web_admin_core.pages.clients_accounts.accounts.accounts_constants import AccountsConstants
from test_framework.web_admin_core.pages.common_page import CommonPage
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer


class AccountsRoutesSubWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def click_on_plus_button(self):
        self.find_by_xpath(AccountsConstants.ADD_ROUTES_ENTITY_BUTTON_XPATH).click()

    def filter_routes(self, route_account_name: str = "", route: str = ""):
        self.set_text_by_xpath(AccountsConstants.ROUTES_ROUTE_ACCOUNT_NAME_FILTER_XPATH, route_account_name)
        self.set_text_by_xpath(AccountsConstants.ROUTES_ROUTE_FILTER_XPATH, route)

    def click_edit_button(self):
        self.find_by_xpath(AccountsConstants.ROUTES_EDIT_BUTTON_XPATH).click()

    def click_delete_button(self):
        self.find_by_xpath(AccountsConstants.ROUTES_DELETE_BUTTON_XPATH).click()

    def click_on_checkmark_button(self):
        self.find_by_xpath(AccountsConstants.ROUTES_CREATE_ENTITY_BUTTON_XPATH).click()

    def click_discard_entity_button(self):
        self.find_by_xpath(AccountsConstants.ROUTES_DISCARD_ENTITY_BUTTON_XPATH).click()

    def set_route_account_name(self, value: str):
        self.set_text_by_xpath(AccountsConstants.ROUTES_ROUTE_ACCOUNT_NAME_INPUT_XPATH, value)

    def get_route_account_name(self):
        return self.get_text_by_xpath(AccountsConstants.ROUTES_ROUTE_ACCOUNT_NAME_INPUT_XPATH)

    def set_route(self, value: str):
        self.set_combobox_value(AccountsConstants.ROUTES_ROUTE_COMBOBOX_XPATH, value)

    def get_route(self):
        return self.get_text_by_xpath(AccountsConstants.ROUTES_ROUTE_COMBOBOX_XPATH)

    def set_default_route(self, value):
        self.set_combobox_value(AccountsConstants.ROUTES_DEFAULT_ROUTE_XPATH, value)

    def get_default_route(self):
        return self.get_text_by_xpath(AccountsConstants.ROUTES_DEFAULT_ROUTE_XPATH)

    def select_agent_fee_exemption_checkbox(self):
        self.find_by_xpath(AccountsConstants.ROUTES_AGENT_FEE_EXEMPTION_XPATH).click()
        
    def is_agent_fee_exemption_selected(self):
        return self.is_checkbox_selected(AccountsConstants.ROUTES_AGENT_FEE_EXEMPTION_XPATH)
