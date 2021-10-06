import time

from quod_qa.web_admin.web_admin_core.pages.common_page import CommonPage
from quod_qa.web_admin.web_admin_core.pages.reference_data.listing_groups.listing_groups_constants import \
    ListingGroupsConstants
from quod_qa.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer


class ListingGroupsDescriptionSubWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def set_name(self, value):
        self.set_text_by_xpath(ListingGroupsConstants.DESCRIPTION_TAB_NAME_XPATH, value)

    def get_name(self):
        return self.get_text_by_xpath(ListingGroupsConstants.DESCRIPTION_TAB_NAME_XPATH)

    def set_ext_id_venue(self, value):
        self.set_text_by_xpath(ListingGroupsConstants.DESCRIPTION_TAB_EXT_ID_VENUE_XPATH, value)

    def get_ext_id_venue(self):
        return self.get_text_by_xpath(ListingGroupsConstants.DESCRIPTION_TAB_EXT_ID_VENUE_XPATH)

    def set_sub_venue(self, value):
        self.set_combobox_value(ListingGroupsConstants.DESCRIPTION_TAB_SUB_VENUE_XPATH, value)

    def get_sub_venue(self):
        return self.get_text_by_xpath(ListingGroupsConstants.DESCRIPTION_TAB_SUB_VENUE_XPATH)

    def set_default_symbol(self, value):
        self.set_text_by_xpath(ListingGroupsConstants.DESCRIPTION_TAB_DEFAULT_SYMBOL_XPATH, value)

    def get_default_symbol(self):
        return self.get_text_by_xpath(ListingGroupsConstants.DESCRIPTION_TAB_DEFAULT_SYMBOL_XPATH)

    def get_feed_source(self):
        return self.find_by_xpath(ListingGroupsConstants.DESCRIPTION_TAB_FEED_SOURCE_XPATH).get_attribute("value")

    def set_market_data_source(self, value):
        self.set_text_by_xpath(ListingGroupsConstants.DESCRIPTION_TAB_MARKET_DATA_SOURCE_XPATH, value)

    def get_market_data_source(self):
        return self.get_text_by_xpath(ListingGroupsConstants.DESCRIPTION_TAB_MARKET_DATA_SOURCE_XPATH)

    def click_on_news_checkbox(self):
        self.find_by_xpath(ListingGroupsConstants.DESCRIPTION_TAB_NEWS_CHECKBOX_XPATH).click()

    def set_news_symbol(self, value):
        self.set_text_by_xpath(ListingGroupsConstants.DESCRIPTION_TAB_NEWS_SYMBOL_XPATH, value)

    def get_news_symbol(self):
        return self.get_text_by_xpath(ListingGroupsConstants.DESCRIPTION_TAB_NEWS_SYMBOL_XPATH)
