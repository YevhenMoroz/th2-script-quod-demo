from quod_qa.web_admin.web_admin_core.pages.common_page import CommonPage
from quod_qa.web_admin.web_admin_core.pages.general.settings.settings_constants import SettingsConstants

from quod_qa.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer


class SettingsPage(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def set_settings(self, value):
        self.set_text_by_xpath(SettingsConstants.SETTINGS_SETTING_FILTER_XPATH, value)

    def get_settings(self):
        return self.find_by_xpath(SettingsConstants.SETTINGS_SETTING_XPATH)

    def set_value(self, value):
        self.set_text_by_xpath(SettingsConstants.SETTINGS_VALUE_FILTER_XPATH, value)

    def get_value(self):
        return self.find_by_xpath(SettingsConstants.SETTINGS_VALUE_XPATH)
