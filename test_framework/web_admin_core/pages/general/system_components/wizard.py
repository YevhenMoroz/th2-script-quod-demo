import time

from test_framework.web_admin_core.pages.common_page import CommonPage
from test_framework.web_admin_core.pages.general.system_components.constants import Constants
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer


class Wizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def get_short_name(self):
        return self.get_text_by_xpath(Constants.ValuesTab.SHORT_NAME)

    def get_long_name(self):
        return self.get_text_by_xpath(Constants.ValuesTab.LONG_NAME)

    def get_version(self):
        return self.get_text_by_xpath(Constants.ValuesTab.VERSION)

    def click_on_save_changes_button(self):
        self.find_by_xpath(Constants.Wizard.SAVE_CHANGES_BUTTON).click()

    def click_on_revert_changes_button(self):
        self.find_by_xpath(Constants.Wizard.REVERT_CHANGES_BUTTON).click()

    def click_on_page_header_link(self):
        self.find_by_xpath(Constants.Wizard.PAGE_HEADER_LINK).click()

    def click_on_help_icon_button(self):
        self.find_by_xpath(Constants.Wizard.HELP_ICON).click()

    def click_on_download_local_file_button(self):
        self.find_by_xpath(Constants.Wizard.DOWNLOAD_LOCAL_FILE_BUTTON).click()

    def click_on_close_wizard_button(self):
        self.find_by_xpath(Constants.Wizard.CLOSE_WIZARD_BUTTON).click()

    def is_wizard_open(self):
        return self.is_element_present(Constants.Wizard.PAGE_HEADER_LINK)
