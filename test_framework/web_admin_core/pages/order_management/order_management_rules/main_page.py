import time

from test_framework.web_admin_core.pages.common_page import CommonPage
from test_framework.web_admin_core.pages.order_management.order_management_rules.constants import Constants


class MainPage(CommonPage):

    def click_on_more_actions(self):
        self.find_by_xpath(Constants.MoreActions.MORE_ACTIONS_BUTTON).click()

    def click_on_edit(self):
        self.find_by_xpath(Constants.MoreActions.EDIT).click()

    def click_on_clone(self):
        self.find_by_xpath(Constants.MoreActions.CLONE).click()

    def click_download_pdf_entity_button_and_check_pdf(self, value):
        self.clear_download_directory()
        self.find_by_xpath(Constants.MoreActions.DOWNLOAD_PDF).click()
        time.sleep(2)
        return self.is_pdf_contains_value(value)

    def click_download_csv_entity_button_and_check_csv(self):
        self.clear_download_directory()
        self.find_by_xpath(Constants.MainPage.DOWNLOAD_CSV_BUTTON).click()
        time.sleep(2)
        return self.get_csv_context()

    def click_on_pin_row(self):
        self.find_by_xpath(Constants.MoreActions.PIN_ROW).click()

    def click_on_new_button(self):
        self.find_by_xpath(Constants.MainPage.NEW_BUTTON).click()

    def click_on_toggle_button(self, confirm: bool):
        self.find_by_xpath(Constants.MainPage.TOGGLE_BUTTON).click()
        if confirm:
            self.find_by_xpath(Constants.MainPage.OK_BUTTON).click()

    def is_searched_entity_found(self, value):
        return self.is_element_present(Constants.MainPage.SEARCHED_ENTITY.format(value))

    def set_name_filter(self, value):
        self.set_text_by_xpath(Constants.MainPage.NAME_FILTER, value)

    def set_enabled_filter(self, value):
        self.select_value_from_dropdown_list(Constants.MainPage.ENABLED_FILTER, value)

    def get_all_names(self):
        return self.get_all_items_from_table_column(Constants.MainPage.ENTITY_NAME)

    def get_all_statuses(self):
        return self.get_all_checkboxes_statuses_from_table_column(Constants.MainPage.ENTITY_STATUS)
