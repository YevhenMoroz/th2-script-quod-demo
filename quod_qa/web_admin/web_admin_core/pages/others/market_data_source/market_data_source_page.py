import time

from quod_qa.web_admin.web_admin_core.pages.common_page import CommonPage
from quod_qa.web_admin.web_admin_core.pages.others.market_data_source.market_data_source_constants import \
    MarketDataSourceConstants
from quod_qa.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer


class MarketDataSourcePage(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def click_on_more_actions(self):
        self.find_by_xpath(MarketDataSourceConstants.MORE_ACTIONS_BUTTON_XPATH).click()

    def click_on_edit_at_more_actions(self):
        self.find_by_xpath(MarketDataSourceConstants.EDIT_AT_MORE_ACTIONS_XPATH).click()

    def click_on_clone_at_more_actions(self):
        self.find_by_xpath(MarketDataSourceConstants.CLONE_AT_MORE_ACTIONS_XPATH).click()

    def click_download_pdf_entity_button_and_check_pdf(self, value: str):
        self.clear_download_directory()
        self.find_by_xpath(MarketDataSourceConstants.DOWNLOAD_PDF_AT_MORE_ACTIONS_XPATH).click()
        time.sleep(2)
        return self.is_pdf_contains_value(value)

    def click_on_pin_row_at_more_actions(self):
        self.find_by_xpath(MarketDataSourceConstants.PIN_TO_ROW_AT_MORE_ACTIONS_XPATH).click()

    def click_on_delete_and_confirmation(self, confirmation):
        self.find_by_xpath(MarketDataSourceConstants.DELETE_AT_MORE_ACTIONS_XPATH).click()
        if confirmation:
            time.sleep(2)
            self.find_by_xpath(MarketDataSourceConstants.OK_BUTTON_XPATH).click()
        else:
            self.find_by_xpath(MarketDataSourceConstants.CANCEL_BUTTON_XPATH).click()

    def click_on_ok_button(self):
        self.find_by_xpath(MarketDataSourceConstants.OK_BUTTON_XPATH).click()

    def click_on_no_button(self):
        self.find_by_xpath(MarketDataSourceConstants.NO_BUTTON_XPATH).click()

    def click_on_cancel_button(self):
        self.find_by_xpath(MarketDataSourceConstants.CANCEL_BUTTON_XPATH).click()


    def click_on_download_csv_button(self):
        self.find_by_xpath(MarketDataSourceConstants.DOWNLOAD_CSV_BUTTON_XPATH).click()

    def click_on_refresh_button(self):
        self.find_by_xpath(MarketDataSourceConstants.REFRESH_PAGE_BUTTON_XPATH).click()

    def click_on_new_button(self):
        self.find_by_xpath(MarketDataSourceConstants.NEW_BUTTON_XPATH).click()

    # --setters--
    def set_symbol_at_filter(self, value):
        self.set_text_by_xpath(MarketDataSourceConstants.MAIN_PAGE_SYMBOL_FILTER_XPATH, value)

    def set_user_at_filter(self, value):
        self.set_text_by_xpath(MarketDataSourceConstants.MAIN_PAGE_USER_FILTER_XPATH, value)

    def set_venue_at_filter(self, value):
        self.set_text_by_xpath(MarketDataSourceConstants.MAIN_PAGE_VENUE_FILTER_XPATH, value)

    def set_md_source_at_filter(self, value):
        self.set_text_by_xpath(MarketDataSourceConstants.MAIN_PAGE_MDSOURCE_FILTER_XPATH, value)

    # --getters--
    def get_symbol(self):
        return self.find_by_xpath(MarketDataSourceConstants.MAIN_PAGE_SYMBOL_XPATH).text

    def get_user(self):
        return self.find_by_xpath(MarketDataSourceConstants.MAIN_PAGE_USER_XPATH).text

    def get_venue(self):
        return self.find_by_xpath(MarketDataSourceConstants.MAIN_PAGE_VENUE_XPATH).text

    def get_md_source(self):
        return self.find_by_xpath(MarketDataSourceConstants.MAIN_PAGE_MDSOURCE_XPATH).text
