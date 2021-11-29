import time

from test_cases.web_admin.web_admin_core.pages.positions.wash_books.wash_books_constants import WashBookConstants
from test_cases.web_admin.web_admin_core.pages.common_page import CommonPage
from test_cases.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer


class WashBookPage(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    # region click on
    def click_on_new_button(self):
        self.find_by_xpath(WashBookConstants.NEW_BUTTON_XPATH).click()

    def click_on_edit(self):
        self.find_by_xpath(WashBookConstants.EDIT_BUTTON_XPATH).click()

    def click_on_enable_disable_button(self):
        self.find_by_xpath(WashBookConstants.ENABLE_DISABLE_BUTTON_XPATH).click()

    def click_on_more_actions(self):
        self.find_by_xpath(WashBookConstants.MORE_ACTIONS_XPATH).click()

    def click_on_edit_at_more_actions(self):
        self.find_by_xpath(WashBookConstants.EDIT_AT_MORE_ACTIONS_XPATH).click()

    def click_on_clone_at_more_actions(self):
        self.find_by_xpath(WashBookConstants.CLONE_AT_MORE_ACTIONS_XPATH).click()

    def click_download_pdf_entity_button_and_check_pdf(self, value):
        self.clear_download_directory()
        self.find_by_xpath(WashBookConstants.DOWNLOAD_PDF_AT_MORE_ACTIONS_XPATH).click()
        time.sleep(2)
        return self.is_pdf_contains_value(value)

    def click_on_pin_row_at_more_actions(self):
        self.find_by_xpath(WashBookConstants.PIN_TO_ROW_AT_MORE_ACTIONS_XPATH).click()

    def click_on_ok(self):
        self.find_by_xpath(WashBookConstants.OK_BUTTON_XPATH).click()

    # endregion

    # region Setters for filter and getters for values

    def set_id_filter(self, value):
        self.set_text_by_xpath(WashBookConstants.ID_FILTER_AT_MAIN_PAGE_XPATH, value)

    def get_id_at_main_page(self):
        return self.find_by_xpath(WashBookConstants.ID_AT_MAIN_PAGE_XPATH).text

    def set_description_filter(self, value):
        self.set_text_by_xpath(WashBookConstants.DESCRIPTION_FILTER_AT_MAIN_PAGE_XPATH, value)

    def get_description_at_main_page(self):
        return self.find_by_xpath(WashBookConstants.DESCRIPTION_AT_MAIN_PAGE_XPATH).text

    def set_client_filter(self, value):
        self.set_text_by_xpath(WashBookConstants.CLIENT_FILTER_AT_MAIN_PAGE_XPATH, value)

    def get_client_at_main_page(self):
        return self.find_by_xpath(WashBookConstants.CLIENT_AT_MAIN_PAGE_XPATH).text

    def set_ext_id_client_filter(self, value):
        self.set_text_by_xpath(WashBookConstants.EXT_ID_CLIENT_FILTER_AT_MAIN_PAGE_XPATH, value)

    def get_ext_id_client_at_main_page(self):
        return self.find_by_xpath(WashBookConstants.EXT_ID_CLIENT_AT_MAIN_PAGE_XPATH).text

    def set_client_id_source_filter(self, value):
        self.set_text_by_xpath(WashBookConstants.CLIENT_ID_SOURCE_FILTER_AT_MAIN_PAGE_XPATH, value)

    def get_client_id_source_at_main_page(self):
        return self.find_by_xpath(WashBookConstants.CLIENT_ID_SOURCE_AT_MAIN_PAGE_XPATH).text

    def set_clearing_account_type_filter(self, value):
        self.set_text_by_xpath(WashBookConstants.CLEARING_ACCOUNT_TYPE_FILTER_AT_MAIN_PAGE_XPATH, value)

    def get_clearing_account_type_at_main_page(self):
        return self.find_by_xpath(WashBookConstants.CLEARING_ACCOUNT_TYPE_AT_MAIN_PAGE_XPATH).text

    def set_counterpart_filter(self, value):
        self.set_text_by_xpath(WashBookConstants.COUNTERPART_FILTER_AT_MAIN_PAGE_XPATH, value)

    def get_counterpart_at_main_page(self):
        return self.find_by_xpath(WashBookConstants.COUNTERPART_AT_MAIN_PAGE_XPATH).text

    def set_enabled_filter(self, value):
        self.find_by_xpath(WashBookConstants.ENABLED_FILTER_AT_MAIN_PAGE_XPATH).click()
        time.sleep(1)
        self.select_value_from_dropdown_list(WashBookConstants.ENABLED_FILTER_LIST_AT_MAIN_PAGE_XPATH.format(value))

    def get_enabled_at_main_page(self):
        return self.is_checkbox_selected(WashBookConstants.ENABLED_AT_MAIN_PAGE_XPATH)

    # endregion
