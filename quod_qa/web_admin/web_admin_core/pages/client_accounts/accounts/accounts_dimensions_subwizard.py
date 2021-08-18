from quod_qa.web_admin.web_admin_core.pages.client_accounts.accounts.accounts_constants import AccountsConstants
from quod_qa.web_admin.web_admin_core.pages.common_page import CommonPage
from quod_qa.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer


class AccountsDimensionsSubWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def open_dimensions_subwizard(self):
        self.find_by_xpath(AccountsConstants.ADD_DIMENSIONS_ENTITY_BUTTON_XPATH).click()

    def filter_dimensions(self, venue_account: str = "", venue: str = "", account_id_source: str = "", default_route: str = "", stamp_exempt: str = "", levy_exempt: str = "", per_transac_exempt: str = "", venue_client_account_name: str = ""):
        self.set_text_by_xpath(AccountsConstants.DIMENSIONS_VENUE_ACCOUNT_FILTER_XPATH, venue_account)
        self.set_text_by_xpath(AccountsConstants.DIMENSIONS_VENUE_FILTER_XPATH, venue)
        self.set_text_by_xpath(AccountsConstants.DIMENSIONS_ACCOUNT_ID_SOURCE_FILTER_XPATH, account_id_source)
        self.set_text_by_xpath(AccountsConstants.DIMENSIONS_DEFAULT_ROUTE_FILTER_XPATH, default_route)
        self.set_text_by_xpath(AccountsConstants.DIMENSIONS_STAMP_EXEMPT_FILTER_XPATH, stamp_exempt)
        self.set_text_by_xpath(AccountsConstants.DIMENSIONS_LEVY_EXEMPT_FILTER_XPATH, levy_exempt)
        self.set_text_by_xpath(AccountsConstants.DIMENSIONS_PER_TRANSAC_EXEMPT_FILTER_XPATH, per_transac_exempt)
        self.set_text_by_xpath(AccountsConstants.DIMENSIONS_VENUE_CLIENT_ACCOUNT_NAME_FILTER_XPATH, venue_client_account_name)

    def click_edit_button(self):
        self.find_by_xpath(AccountsConstants.DIMENSIONS_EDIT_BUTTON_XPATH).click()

    def click_delete_button(self):
        self.find_by_xpath(AccountsConstants.DIMENSIONS_DELETE_BUTTON_XPATH).click()

    def set_venue_account(self, value: str):
        self.set_text_by_xpath(AccountsConstants.DIMENSIONS_VENUE_ACCOUNT_INPUT_XPATH, value)

    def get_venue_account(self):
        return self.get_text_by_xpath(AccountsConstants.DIMENSIONS_VENUE_ACCOUNT_INPUT_XPATH)

    def set_venue(self, value: str):
        self.set_combobox_value(AccountsConstants.DIMENSIONS_VENUE_COMBOBOX_XPATH, value)

    def get_venue(self):
        return self.get_text_by_xpath(AccountsConstants.DIMENSIONS_VENUE_COMBOBOX_XPATH)

    def set_account_id_source(self, value: str):
        self.set_combobox_value(AccountsConstants.DIMENSIONS_ACCOUNT_ID_SOURCE_COMBOBOX_XPATH, value)

    def get_account_id_source(self):
        return self.get_text_by_xpath(AccountsConstants.DIMENSIONS_ACCOUNT_ID_SOURCE_COMBOBOX_XPATH)

    def set_default_route(self, value: str):
        self.set_combobox_value(AccountsConstants.DIMENSIONS_DEFAULT_ROUTE_COMBOBOX_XPATH, value)

    def get_default_route(self):
        return self.get_text_by_xpath(AccountsConstants.DIMENSIONS_DEFAULT_ROUTE_COMBOBOX_XPATH)

    def set_stamp_exempt(self):
        self.toggle_checkbox(AccountsConstants.DIMENSIONS_STAMP_EXEMPT_CHECKBOX_XPATH)

    def get_stamp_exempt(self):
        return self.is_checkbox_selected(AccountsConstants.DIMENSIONS_STAMP_EXEMPT_CHECKBOX_XPATH)

    def set_levy_exempt(self):
        self.toggle_checkbox(AccountsConstants.DIMENSIONS_LEVY_EXEMPT_CHECKBOX_XPATH)

    def get_levy_exempt(self):
        return self.is_checkbox_selected(AccountsConstants.DIMENSIONS_LEVY_EXEMPT_CHECKBOX_XPATH)

    def set_per_transac_exempt(self):
        self.toggle_checkbox(AccountsConstants.DIMENSIONS_PER_TRANSAC_EXEMPT_CHECKBOX_XPATH)

    def get_per_transac_exempt(self):
        return self.is_checkbox_selected(AccountsConstants.DIMENSIONS_PER_TRANSAC_EXEMPT_CHECKBOX_XPATH)

    def set_venue_client_account_name(self, value: str):
        self.set_text_by_xpath(AccountsConstants.DIMENSIONS_VENUE_CLIENT_ACCOUNT_NAME_INPUT_XPATH, value)

    def get_venue_client_account_name(self):
        return self.is_checkbox_selected(AccountsConstants.DIMENSIONS_VENUE_CLIENT_ACCOUNT_NAME_INPUT_XPATH)

    def click_create_entity_button(self):
        self.find_by_xpath(AccountsConstants.DIMENSIONS_CREATE_ENTITY_BUTTON_XPATH).click()

    def click_discard_entity_button(self):
        self.find_by_xpath(AccountsConstants.DIMENSIONS_DISCARD_ENTITY_BUTTON_XPATH).click()

    def click_on_plus(self):
        self.find_by_xpath(AccountsConstants.DIMENSIONS_PLUS_BUTTON_XPATH).click()