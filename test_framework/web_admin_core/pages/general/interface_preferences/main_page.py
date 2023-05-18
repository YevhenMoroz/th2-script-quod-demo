from test_framework.web_admin_core.pages.common_page import CommonPage
from test_framework.web_admin_core.pages.general.interface_preferences.constants import Constants
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer


class MainPage(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def click_on_plus_button(self):
        self.find_by_xpath(Constants.MainPage.PLUS_BUTTON).click()

    def click_on_save_checkmark(self):
        self.find_by_xpath(Constants.MainPage.SAVE_CHECKMARK_BUTTON).click()

    def click_on_cancel_button(self):
        self.find_by_xpath(Constants.MainPage.CANCEL_BUTTON).click()

    def click_on_edit_button(self):
        self.find_by_xpath(Constants.MainPage.EDIT_BUTTON).click()

    def click_on_delete_button(self):
        self.find_by_xpath(Constants.MainPage.DELETE_BUTTON).click()

    def set_interface_id_filter(self, value):
        self.set_text_by_xpath(Constants.MainPage.INTERFACE_ID_FILTER, value)

    def set_name_filter(self, value):
        self.set_text_by_xpath(Constants.MainPage.NAME_FILTER, value)

    def set_interface_id(self, value):
        self.set_text_by_xpath(Constants.MainPage.INTERFACE_ID, value)

    def set_name(self, value):
        self.set_text_by_xpath(Constants.MainPage.NAME, value)

    def send_upload_file(self, path_to_file):
        self.find_by_xpath(Constants.MainPage.UPDATE_PREFERENCE_LINK).send_keys(path_to_file)

    def click_on_default_checkbox(self):
        self.find_by_xpath(Constants.MainPage.DELETE_BUTTON).click()

    def click_on_clear_changes_button(self):
        self.find_by_xpath(Constants.MainPage.CLEAR_CHANGES_BUTTON).click()

    def click_on_save_changes_button(self):
        self.find_by_xpath(Constants.MainPage.SAVE_CHANGES_BUTTON)

    def is_searched_entity_found_by_name(self, name):
        return self.is_element_present(Constants.MainPage.SEARCHED_ENTITY.format(name))
