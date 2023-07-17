from test_framework.web_admin_core.pages.common_page import CommonPage
from test_framework.web_admin_core.pages.users.user_lists.constants import Constants
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer


class MainPage(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def set_global_filter(self, value):
        self.set_text_by_xpath(Constants.MainPage.GLOBAL_FILTER, value)

    def click_on_help_icon(self):
        self.find_by_xpath(Constants.MainPage.HELP_ICON_BUTTON).click()

    def click_on_download_csv_button(self):
        self.find_by_xpath(Constants.MainPage.FULL_SCREEN_BUTTON).click()

    def click_on_refresh_page_button(self):
        self.find_by_xpath(Constants.MainPage.REFRESH_PAGE_BUTTON).click()

    def click_on_new_button(self):
        self.find_by_xpath(Constants.MainPage.NEW_BUTTON).click()

    def set_name_filter(self, value):
        self.set_text_by_xpath(Constants.MainPage.NAME_FILTER, value)

    def set_description_filter(self, value):
        self.set_text_by_xpath(Constants.MainPage.DESCRIPTION_FILTER, value)

    def click_on_more_actions_button(self):
        self.find_by_xpath(Constants.MainPage.MORE_ACTION_BUTTON).click()

    def click_on_edit_button(self):
        self.find_by_xpath(Constants.MainPage.EDIT_BUTTON).click()

    def click_on_clone_button(self):
        self.find_by_xpath(Constants.MainPage.CLONE_BUTTON).click()

    def click_on_delete_button(self):
        self.find_by_xpath(Constants.MainPage.DELETE_BUTTON).click()

    def click_on_download_pdf_button(self):
        self.find_by_xpath(Constants.MainPage.DOWNLOAD_PDF_BUTTON).click()

    def is_user_lists_found(self, value):
        return self.is_element_present(Constants.MainPage.SEARCHED_USER_LIST.format(value))
