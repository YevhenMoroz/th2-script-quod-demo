import time

from test_framework.web_admin_core.pages.common_page import CommonPage
from test_framework.web_admin_core.pages.markets.listings.listings_constants import ListingsConstants
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer


class ListingsAttachmentSubWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def set_venue(self, value):
        self.set_combobox_value(ListingsConstants.ATTACHMENT_TAB_VENUE_XPATH, value)

    def get_venue(self):
        return self.get_text_by_xpath(ListingsConstants.ATTACHMENT_TAB_VENUE_XPATH)

    def is_venue_field_enabled(self):
        return self.is_field_enabled(ListingsConstants.ATTACHMENT_TAB_VENUE_XPATH)

    def set_preferred_venue(self, value):
        self.set_combobox_value(ListingsConstants.ATTACHMENT_TAB_PREFERRED_VENUE_XPATH, value)

    def get_preferred_venue(self):
        return self.get_text_by_xpath(ListingsConstants.ATTACHMENT_TAB_PREFERRED_VENUE_XPATH)

    def set_sub_venue(self, value):
        self.set_combobox_value(ListingsConstants.ATTACHMENT_TAB_SUB_VENUE_XPATH, value)

    def get_sub_venue(self):
        return self.get_text_by_xpath(ListingsConstants.ATTACHMENT_TAB_SUB_VENUE_XPATH)

    def get_all_sub_venue_from_drop_menu(self):
        self.find_by_xpath(ListingsConstants.ATTACHMENT_TAB_SUB_VENUE_XPATH).click()
        time.sleep(1)
        return self.get_all_items_from_drop_down(ListingsConstants.DROP_DOWN)

    def set_listing_group(self, value):
        self.set_combobox_value(ListingsConstants.ATTACHMENT_TAB_LISTING_GROUP_XPATH, value)

    def get_listing_group(self):
        return self.get_text_by_xpath(ListingsConstants.ATTACHMENT_TAB_SUB_VENUE_XPATH)
