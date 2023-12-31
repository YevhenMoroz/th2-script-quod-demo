import time

from test_framework.web_admin_core.pages.common_page import CommonPage
from test_framework.web_admin_core.pages.markets.market_data_sources.constants import \
    MarketDataSourcesConstants
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer


class MarketDataSourcesWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def click_on_save_changes(self):
        self.find_by_xpath(MarketDataSourcesConstants.SAVE_CHANGES_XPATH).click()

    def click_on_clear_changes(self):
        self.find_by_xpath(MarketDataSourcesConstants.CLEAR_CHANGES_XPATH).click()

    def click_download_pdf_entity_button_and_check_pdf(self, value):
        self.clear_download_directory()
        self.find_by_xpath(MarketDataSourcesConstants.WIZARD_DOWNLOAD_PDF_XPATH).click()
        time.sleep(2)
        return self.is_pdf_contains_value(value)

    def click_on_close_wizard(self):
        self.find_by_xpath(MarketDataSourcesConstants.WIZARD_CLOSE_BUTTON_XPATH).click()

    def click_on_ok_button(self):
        self.find_by_xpath(MarketDataSourcesConstants.OK_BUTTON_XPATH).click()

    def click_on_no_button(self):
        self.find_by_xpath(MarketDataSourcesConstants.NO_BUTTON_XPATH).click()

    def click_on_cancel_button(self):
        self.find_by_xpath(MarketDataSourcesConstants.CANCEL_BUTTON_XPATH).click()

    def set_symbol(self, value):
        self.set_combobox_value(MarketDataSourcesConstants.WIZARD_SYMBOL_XPATH, value)

    def get_symbol(self):
        return self.get_text_by_xpath(MarketDataSourcesConstants.WIZARD_SYMBOL_XPATH)

    def set_user(self, value):
        self.set_combobox_value(MarketDataSourcesConstants.WIZARD_USER_XPATH, value)

    def get_user(self):
        return self.get_text_by_xpath(MarketDataSourcesConstants.WIZARD_USER_XPATH)

    def set_venue(self, value):
        self.set_combobox_value(MarketDataSourcesConstants.WIZARD_VENUE_XPATH, value)

    def get_venue(self):
        return self.get_text_by_xpath(MarketDataSourcesConstants.WIZARD_VENUE_XPATH)

    def set_md_source(self, value):
        self.set_text_by_xpath(MarketDataSourcesConstants.WIZARD_MDSOURCE_XPATH, value)

    def is_symbol_field_enabled(self):
        return self.is_field_enabled(MarketDataSourcesConstants.WIZARD_SYMBOL_XPATH)

    def is_user_field_enabled(self):
        return self.is_field_enabled(MarketDataSourcesConstants.WIZARD_USER_XPATH)

    def is_venue_field_enabled(self):
        return self.is_field_enabled(MarketDataSourcesConstants.WIZARD_VENUE_XPATH)

    def is_incorrect_or_missing_value_message_displayed(self):
        if self.find_by_xpath(MarketDataSourcesConstants.INCORECT_VALUE_MESSAGE).text == "Incorrect or missing values":
            return True
        else:
            return False

    def get_all_symbol_from_drop_menu(self):
        self.find_by_xpath(MarketDataSourcesConstants.WIZARD_SYMBOL_XPATH).click()
        time.sleep(1)
        return self.get_all_items_from_drop_down(MarketDataSourcesConstants.DROP_DOWN_MENU_XPATH)
