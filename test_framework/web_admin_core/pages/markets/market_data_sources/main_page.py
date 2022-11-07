import time

from test_framework.web_admin_core.pages.common_page import CommonPage
from test_framework.web_admin_core.pages.markets.market_data_sources.constants import \
    MarketDataSourcesConstants
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer


class MarketDataSourcesPage(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def click_on_more_actions(self):
        self.find_by_xpath(MarketDataSourcesConstants.MORE_ACTIONS_BUTTON_XPATH).click()

    def click_on_edit_at_more_actions(self):
        self.find_by_xpath(MarketDataSourcesConstants.EDIT_AT_MORE_ACTIONS_XPATH).click()

    def click_on_clone_at_more_actions(self):
        self.find_by_xpath(MarketDataSourcesConstants.CLONE_AT_MORE_ACTIONS_XPATH).click()

    def click_download_pdf_entity_button_and_check_pdf(self, value: str):
        self.clear_download_directory()
        self.find_by_xpath(MarketDataSourcesConstants.DOWNLOAD_PDF_AT_MORE_ACTIONS_XPATH).click()
        time.sleep(2)
        return self.is_pdf_contains_value(value)

    def click_on_pin_row_at_more_actions(self):
        self.find_by_xpath(MarketDataSourcesConstants.PIN_TO_ROW_AT_MORE_ACTIONS_XPATH).click()

    def click_on_delete_and_confirmation(self, confirmation):
        self.find_by_xpath(MarketDataSourcesConstants.DELETE_AT_MORE_ACTIONS_XPATH).click()
        if confirmation:
            time.sleep(2)
            self.find_by_xpath(MarketDataSourcesConstants.OK_BUTTON_XPATH).click()
        else:
            self.find_by_xpath(MarketDataSourcesConstants.CANCEL_BUTTON_XPATH).click()

    def click_on_ok_button(self):
        self.find_by_xpath(MarketDataSourcesConstants.OK_BUTTON_XPATH).click()

    def click_on_no_button(self):
        self.find_by_xpath(MarketDataSourcesConstants.NO_BUTTON_XPATH).click()

    def click_on_cancel_button(self):
        self.find_by_xpath(MarketDataSourcesConstants.CANCEL_BUTTON_XPATH).click()


    def click_on_download_csv_button(self):
        self.find_by_xpath(MarketDataSourcesConstants.DOWNLOAD_CSV_BUTTON_XPATH).click()

    def click_on_refresh_button(self):
        self.find_by_xpath(MarketDataSourcesConstants.REFRESH_PAGE_BUTTON_XPATH).click()

    def click_on_new_button(self):
        self.find_by_xpath(MarketDataSourcesConstants.NEW_BUTTON_XPATH).click()

    # --setters--
    def set_symbol_at_filter(self, value):
        self.set_text_by_xpath(MarketDataSourcesConstants.MAIN_PAGE_SYMBOL_FILTER_XPATH, value)

    def set_user_at_filter(self, value):
        self.set_text_by_xpath(MarketDataSourcesConstants.MAIN_PAGE_USER_FILTER_XPATH, value)

    def set_venue_at_filter(self, value):
        self.set_text_by_xpath(MarketDataSourcesConstants.MAIN_PAGE_VENUE_FILTER_XPATH, value)

    def set_md_source_at_filter(self, value):
        self.set_text_by_xpath(MarketDataSourcesConstants.MAIN_PAGE_MDSOURCE_FILTER_XPATH, value)

    # --getters--
    def get_symbol(self):
        return self.find_by_xpath(MarketDataSourcesConstants.MAIN_PAGE_SYMBOL_XPATH).text

    def get_user(self):
        return self.find_by_xpath(MarketDataSourcesConstants.MAIN_PAGE_USER_XPATH).text

    def get_venue(self):
        return self.find_by_xpath(MarketDataSourcesConstants.MAIN_PAGE_VENUE_XPATH).text

    def get_md_source(self):
        return self.find_by_xpath(MarketDataSourcesConstants.MAIN_PAGE_MDSOURCE_XPATH).text
