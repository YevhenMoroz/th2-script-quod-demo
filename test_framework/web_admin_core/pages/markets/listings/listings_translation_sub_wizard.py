from test_framework.web_admin_core.pages.common_page import CommonPage
from test_framework.web_admin_core.pages.markets.listings.listings_constants import \
    ListingsConstants
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer


class TranslationTab:
    class ListingTable(CommonPage):
        def __init__(self, web_driver_container: WebDriverContainer):
            super().__init__(web_driver_container)

        def click_on_plus(self):
            self.find_by_xpath(ListingsConstants.TRANSLATION_TAB_LISTING_PLUS_BUTTON_XPATH).click()

        def click_on_checkmark(self):
            self.find_by_xpath(ListingsConstants.TRANSLATION_TAB_LISTING_CHECKMARK_BUTTON_XPATH).click()

        def click_on_close(self):
            self.find_by_xpath(ListingsConstants.TRANSLATION_TAB_LISTING_CLOSE_BUTTON_XPATH).click()

        def click_on_edit(self):
            self.find_by_xpath(ListingsConstants.TRANSLATION_TAB_LISTING_EDIT_BUTTON_XPATH).click()

        def click_on_delete(self):
            self.find_by_xpath(ListingsConstants.TRANSLATION_TAB_LISTING_DELETE_BUTTON_XPATH).click()

        def set_language_filter(self, value):
            self.set_text_by_xpath(ListingsConstants.TRANSLATION_TAB_LISTING_LANGUAGE_FILTER_XPATH, value)

        def set_language(self, value):
            self.set_combobox_value(ListingsConstants.TRANSLATION_TAB_LISTING_LANGUAGE_XPATH, value)

        def get_language(self):
            return self.get_text_by_xpath(ListingsConstants.TRANSLATION_TAB_LISTING_LANGUAGE_XPATH)

        def set_description_filter(self, value):
            self.set_text_by_xpath(ListingsConstants.TRANSLATION_TAB_LISTING_DESCRIPTION_FILTER_XPATH, value)

        def set_description(self, value):
            self.set_text_by_xpath(ListingsConstants.TRANSLATION_TAB_LISTING_DESCRIPTION_XPATH, value)

        def get_description(self):
            return self.get_text_by_xpath(ListingsConstants.TRANSLATION_TAB_LISTING_DESCRIPTION_XPATH)

        def is_searched_listing_entity_displayed(self, value):
            return self.is_element_present(ListingsConstants.TRANSLATION_TAB_LISTING_SEARCHED_ENTITY_XPATH.format(value))

    class InstrumentTable(CommonPage):
        def __init__(self, web_driver_container: WebDriverContainer):
            super().__init__(web_driver_container)

        def click_on_plus(self):
            self.find_by_xpath(ListingsConstants.TRANSLATION_TAB_INSTRUMENT_PLUS_BUTTON_XPATH).click()

        def click_on_checkmark(self):
            self.find_by_xpath(ListingsConstants.TRANSLATION_TAB_INSTRUMENT_CHECKMARK_BUTTON_XPATH).click()

        def click_on_close(self):
            self.find_by_xpath(ListingsConstants.TRANSLATION_TAB_INSTRUMENT_CLOSE_BUTTON_XPATH).click()

        def click_on_edit(self):
            self.find_by_xpath(ListingsConstants.TRANSLATION_TAB_INSTRUMENT_EDIT_BUTTON_XPATH).click()

        def click_on_delete(self):
            self.find_by_xpath(ListingsConstants.TRANSLATION_TAB_INSTRUMENT_DELETE_BUTTON_XPATH).click()

        def set_language_filter(self, value):
            self.set_text_by_xpath(ListingsConstants.TRANSLATION_TAB_INSTRUMENT_LANGUAGE_FILTER_XPATH, value)

        def set_language(self, value):
            self.set_combobox_value(ListingsConstants.TRANSLATION_TAB_INSTRUMENT_LANGUAGE_XPATH, value)

        def get_language(self):
            return self.get_text_by_xpath(ListingsConstants.TRANSLATION_TAB_INSTRUMENT_LANGUAGE_XPATH)

        def set_description_filter(self, value):
            self.set_text_by_xpath(ListingsConstants.TRANSLATION_TAB_INSTRUMENT_DESCRIPTION_FILTER_XPATH, value)

        def set_description(self, value):
            self.set_text_by_xpath(ListingsConstants.TRANSLATION_TAB_INSTRUMENT_DESCRIPTION_XPATH, value)

        def get_description(self):
            return self.get_text_by_xpath(ListingsConstants.TRANSLATION_TAB_INSTRUMENT_DESCRIPTION_XPATH)

        def is_searched_instrument_entity_displayed(self, value):
            return self.is_element_present(ListingsConstants.TRANSLATION_TAB_INSTRUMENT_SEARCHED_ENTITY_XPATH.format(value))
