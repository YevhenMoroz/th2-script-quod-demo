import time

from selenium.webdriver.support.wait import WebDriverWait

from quod_qa.web_admin.web_admin_core.pages.client_accounts.accounts.accounts_constants import AccountsConstants
from quod_qa.web_admin.web_admin_core.pages.common_page import CommonPage


class AccountsPage(CommonPage):
    def __init__(self, web_driver_wait: WebDriverWait):
        super().__init__(web_driver_wait)

    def click_new_button(self):
        new_button = self.find_by_xpath(AccountsConstants.NEW_BUTTON_XPATH)
        new_button.click()

        time.sleep(2)

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

    def click_download_pdf_entity_button(self):
        self.find_by_xpath(AccountsConstants.DOWNLOAD_PDF_ENTITY_BUTTON_GRID_XPATH).click()
        time.sleep(2)

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
