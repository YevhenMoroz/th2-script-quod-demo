import time

from test_cases.web_admin.web_admin_core.pages.client_accounts.accounts.accounts_constants import AccountsConstants
from test_cases.web_admin.web_admin_core.pages.common_page import CommonPage
from test_cases.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer


class AccountsPage(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def click_new_button(self):
        new_button = self.find_by_xpath(AccountsConstants.NEW_BUTTON_XPATH)
        new_button.click()

        time.sleep(2)

    def click_on_load_button(self):
        load_button = self.find_by_xpath(AccountsConstants.LOAD_BUTTON)
        load_button.click()

    def filter_grid(self, id_value: str):
        self.set_text_by_xpath(AccountsConstants.ID_INPUT_GRID_FILTER_XPATH, id_value)
        time.sleep(2)

    def get_id_grid_value(self):
        return self.find_by_xpath(AccountsConstants.ID_VALUE_GRID_XPATH).text

    def click_more_actions_button(self):
        self.find_by_xpath(AccountsConstants.MORE_ACTIONS_BUTTON_GRID_XPATH).click()

    def click_edit_entity_button(self):
        self.find_by_xpath(AccountsConstants.EDIT_ENTITY_BUTTON_GRID_XPATH).click()
        time.sleep(2)

    def click_clone_entity_button(self):
        self.find_by_xpath(AccountsConstants.CLONE_ENTITY_BUTTON_GRID_XPATH).click()
        time.sleep(2)

    def click_download_pdf_entity_button_and_check_pdf(self, value: str):
        self.clear_download_directory()
        self.find_by_xpath(AccountsConstants.DOWNLOAD_PDF_ENTITY_BUTTON_GRID_XPATH).click()
        time.sleep(2)
        return self.is_pdf_contains_value(value)

    def toggle_entity_toggle_button(self):
        self.find_by_xpath(AccountsConstants.ENABLE_DISABLE_TOGGLE_BUTTON_GRID_XPATH).click()
        self.find_by_xpath(AccountsConstants.CONFIRM_ACTION_BUTTON_XPATH).click()
        time.sleep(2)

    def is_entity_toggle_button_enabled(self):
        return self.is_toggle_button_enabled(AccountsConstants.ENABLE_DISABLE_TOGGLE_BUTTON_GRID_XPATH)

    def get_popup_text(self):
        popup = self.find_by_xpath(AccountsConstants.POPUP_TEXT_XPATH)
        text = popup.text

        popup.click()
        return text

    def get_clearing_account_type(self):
        return self.find_by_xpath(AccountsConstants.MAIN_PAGE_CLEARING_ACCOUNT_TYPE).text

    def get_client(self):
        return self.find_by_xpath(AccountsConstants.MAIN_PAGE_CLIENT).text

    def get_ext_id_client(self):
        return self.find_by_xpath(AccountsConstants.EXT_ID_CLIENT_XPATH).text

    def set_id(self, value):
        self.set_text_by_xpath(AccountsConstants.ID_INPUT_GRID_FILTER_XPATH, value)

    def set_account_for_load(self, value):
        self.set_text_by_xpath(AccountsConstants.ACCOUNT_VALUE_FOR_LOAD, value)

    def load_account_from_global_filter(self, user_id):
        self.set_account_for_load(user_id)
        time.sleep(2)
        self.click_on_load_button()
        time.sleep(2)
