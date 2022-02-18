from test_cases.web_admin.web_admin_core.pages.common_page import CommonPage
from test_cases.web_admin.web_admin_core.pages.reference_data.subvenues.subvenues_constants import SubVenuesConstants
from test_cases.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer


class SubVenuesDescriptionSubWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def set_name(self, value):
        self.set_text_by_xpath(SubVenuesConstants.DESCRIPTION_TAB_NAME_XPATH, value)

    def get_name(self):
        return self.get_text_by_xpath(SubVenuesConstants.DESCRIPTION_TAB_NAME_XPATH)

    def set_ext_id_venue(self, value):
        self.set_text_by_xpath(SubVenuesConstants.DESCRIPTION_TAB_EXT_ID_VENUE_XPATH, value)

    def get_ext_id_venue(self):
        return self.get_text_by_xpath(SubVenuesConstants.DESCRIPTION_TAB_EXT_ID_VENUE_XPATH)

    def set_venue(self, value):
        self.set_combobox_value(SubVenuesConstants.DESCRIPTION_TAB_VENUE_XPATH, value)

    def get_venue(self):
        return self.get_text_by_xpath(SubVenuesConstants.DESCRIPTION_TAB_VENUE_XPATH)

    def set_default_symbol(self, value):
        self.set_text_by_xpath(SubVenuesConstants.DESCRIPTION_TAB_DEFAULT_SYMBOL_XPATH, value)

    def get_default_symbol(self):
        return self.get_text_by_xpath(SubVenuesConstants.DESCRIPTION_TAB_DEFAULT_SYMBOL_XPATH)

    def set_market_data_source(self, value):
        self.set_text_by_xpath(SubVenuesConstants.DESCRIPTION_TAB_MARKET_DATA_SOURCE_XPATH, value)

    def get_market_data_source(self):
        return self.get_text_by_xpath(SubVenuesConstants.DESCRIPTION_TAB_MARKET_DATA_SOURCE_XPATH)

    def set_news_symbol(self, value):
        self.set_text_by_xpath(SubVenuesConstants.DESCRIPTION_TAB_NEWS_SYMBOL_XPATH, value)

    def get_news_symbol(self):
        return self.get_text_by_xpath(SubVenuesConstants.DESCRIPTION_TAB_NEWS_SYMBOL_XPATH)

    def click_on_news(self):
        self.find_by_xpath(SubVenuesConstants.DESCRIPTION_TAB_NEWS_CHECKBOX_XPATH).click()

    def get_feed_source(self):
        return self.find_by_xpath(SubVenuesConstants.DESCRIPTION_TAB_FEED_SOURCE_XPATH).get_attribute("value")

    def is_feed_source_editable(self):
        return self.is_field_enabled(SubVenuesConstants.DESCRIPTION_TAB_FEED_SOURCE_XPATH)
