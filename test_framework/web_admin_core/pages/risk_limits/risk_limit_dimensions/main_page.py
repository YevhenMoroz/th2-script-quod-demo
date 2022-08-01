import time

from test_framework.web_admin_core.pages.common_page import CommonPage
from test_framework.web_admin_core.pages.risk_limits.risk_limit_dimensions.constants import Constants
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer


class MainPage(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def click_on_more_actions(self):
        self.find_by_xpath(Constants.MainPage.MoreAction.MORE_ACTIONS_BUTTON).click()

    def click_on_edit(self):
        self.find_by_xpath(Constants.MainPage.MoreAction.EDIT).click()

    def click_on_clone(self):
        self.find_by_xpath(Constants.MainPage.MoreAction.CLONE).click()

    def click_on_delete(self, confirmation):
        self.find_by_xpath(Constants.MainPage.MoreAction.DELETE).click()
        if confirmation:
            time.sleep(2)
            self.find_by_xpath(Constants.MainPage.OK_BUTTON).click()
        else:
            self.find_by_xpath(Constants.MainPage.CANCEL_BUTTON).click()

    def click_download_pdf_entity_button_and_check_pdf(self, value):
        self.clear_download_directory()
        self.find_by_xpath(Constants.MainPage.MoreAction.DOWNLOAD_PDF).click()
        time.sleep(2)
        return self.is_pdf_contains_value(value)

    def click_download_csv_entity_button_and_check_csv(self):
        self.clear_download_directory()
        self.find_by_xpath(Constants.MainPage.DOWNLOAD_CSV_BUTTON).click()
        time.sleep(2)
        return self.get_csv_context()

    def click_on_pin_row(self):
        self.find_by_xpath(Constants.MainPage.MoreAction.PIN_ROW).click()

    def click_on_new_button(self):
        self.find_by_xpath(Constants.MainPage.NEW_BUTTON).click()

    def click_on_user_icon(self):
        self.find_by_xpath(Constants.MainPage.USER_ICON_AT_RIGHT_CORNER).click()

    def click_on_logout(self):
        self.find_by_xpath(Constants.MainPage.LOGOUT_BUTTON).click()

    def is_searched_entity_found(self, value):
        return self.is_element_present(Constants.MainPage.SEARCHED_ENTITY.format(value))

    def set_name_filter(self, value):
        self.set_text_by_xpath(Constants.MainPage.NAME_FILTER, value)
