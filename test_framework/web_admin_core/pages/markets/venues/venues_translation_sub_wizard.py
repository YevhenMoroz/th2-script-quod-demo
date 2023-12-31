from test_framework.web_admin_core.pages.common_page import CommonPage
from test_framework.web_admin_core.pages.markets.venues.venues_constants import VenuesConstants
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer


class VenuesTranslationSubWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def click_on_plus_button(self):
        self.find_by_xpath(VenuesConstants.TRANSLATION_TAB_PLUS_BUTTON_XPATH).click()

    def click_on_checkmark(self):
        self.find_by_xpath(VenuesConstants.TRANSLATION_TAB_CHECKMARK_BUTTON_XPATH).click()

    def click_on_close(self):
        self.find_by_xpath(VenuesConstants.TRANSLATION_TAB_CLOSE_BUTTON_XPATH).click()

    def click_on_edit(self):
        self.find_by_xpath(VenuesConstants.TRANSLATION_TAB_EDIT_BUTTON_XPATH).click()

    def click_on_delete(self):
        self.find_by_xpath(VenuesConstants.TRANSLATION_TAB_DELETE_BUTTON_XPATH).click()

    def set_language(self, value):
        self.set_combobox_value(VenuesConstants.TRANSLATION_TAB_LANGUAGE_XPATH, value)

    def set_language_filter(self, value):
        self.set_text_by_xpath(VenuesConstants.TRANSLATION_TAB_LANGUAGE_FILTER_XPATH, value)

    def get_language(self):
        return self.get_text_by_xpath(VenuesConstants.TRANSLATION_TAB_LANGUAGE_XPATH)

    def set_name(self, value):
        self.set_text_by_xpath(VenuesConstants.TRANSLATION_TAB_NAME_XPATH, value)

    def set_name_filter(self, value):
        self.set_text_by_xpath(VenuesConstants.TRANSLATION_TAB_NAME_FILTER_XPATH, value)

    def get_name(self):
        return self.get_text_by_xpath(VenuesConstants.TRANSLATION_TAB_NAME_XPATH)

    def set_description(self, value):
        self.set_text_by_xpath(VenuesConstants.TRANSLATION_TAB_DESCRIPTION_XPATH, value)

    def set_description_filter(self, value):
        self.set_text_by_xpath(VenuesConstants.TRANSLATION_TAB_DESCRIPTION_FILTER_XPATH, value)

    def get_description(self):
        return self.get_text_by_xpath(VenuesConstants.TRANSLATION_TAB_DESCRIPTION_XPATH)

    def set_venue_short_name(self, value):
        self.set_text_by_xpath(VenuesConstants.TRANSLATION_TAB_VENUE_SHORT_NAME_XPATH, value)

    def set_venue_short_name_filter(self, value):
        self.set_text_by_xpath(VenuesConstants.TRANSLATION_TAB_VENUE_SHORT_NAME_FILTER_XPATH, value)

    def get_venue_short_name(self):
        return self.get_text_by_xpath(VenuesConstants.TRANSLATION_TAB_VENUE_SHORT_NAME_XPATH)

    def set_venue_very_short_name(self, value):
        self.set_text_by_xpath(VenuesConstants.TRANSLATION_TAB_VENUE_VERY_SHORT_NAME_XPATH, value)

    def get_venue_very_short_name(self):
        self.get_text_by_xpath(VenuesConstants.TRANSLATION_TAB_VENUE_VERY_SHORT_NAME_XPATH)

    def set_venue_very_short_name_filter(self, value):
        self.set_text_by_xpath(VenuesConstants.TRANSLATION_TAB_VENUE_VERY_SHORT_NAME_FILTER_XPATH, value)
