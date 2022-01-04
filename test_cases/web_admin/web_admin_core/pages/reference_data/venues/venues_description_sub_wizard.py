from test_cases.web_admin.web_admin_core.pages.common_page import CommonPage
from test_cases.web_admin.web_admin_core.pages.reference_data.venues.venues_constants import VenuesConstants
from test_cases.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer


class VenuesDescriptionSubWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def set_name(self, value):
        self.set_text_by_xpath(VenuesConstants.DESCRIPTION_TAB_NAME_XPATH, value)

    def get_name(self):
        return self.get_text_by_xpath(VenuesConstants.DESCRIPTION_TAB_NAME_XPATH)

    def set_country(self, value):
        self.set_combobox_value(VenuesConstants.DESCRIPTION_TAB_COUNTRY_XPATH, value)

    def get_country(self):
        return self.get_text_by_xpath(VenuesConstants.DESCRIPTION_TAB_COUNTRY_XPATH)

    def set_very_short_name(self, value):
        self.set_text_by_xpath(VenuesConstants.DESCRIPTION_TAB_VERY_SHORT_NAME_XPATH, value)

    def get_very_short_name(self):
        return self.get_text_by_xpath(VenuesConstants.DESCRIPTION_TAB_VERY_SHORT_NAME_XPATH)

    def set_type(self, value):
        self.set_combobox_value(VenuesConstants.DESCRIPTION_TAB_TYPE_XPATH, value)

    def get_type(self):
        return self.get_text_by_xpath(VenuesConstants.DESCRIPTION_TAB_TYPE_XPATH)

    def set_bic(self, value):
        self.set_text_by_xpath(VenuesConstants.DESCRIPTION_TAB_BIC_XPATH, value)

    def get_bic(self):
        return self.get_text_by_xpath(VenuesConstants.DESCRIPTION_TAB_BIC_XPATH)

    def set_id(self, value):
        self.set_text_by_xpath(VenuesConstants.DESCRIPTION_TAB_ID_XPATH, value)

    def get_id(self):
        return self.get_text_by_xpath(VenuesConstants.DESCRIPTION_TAB_ID_XPATH)

    def set_category(self, value):
        self.set_text_by_xpath(VenuesConstants.DESCRIPTION_TAB_CATEGORY_XPATH, value)

    def get_category(self):
        self.get_text_by_xpath(VenuesConstants.DESCRIPTION_TAB_CATEGORY_XPATH)

    def set_client_venue_id(self, value):
        self.set_text_by_xpath(VenuesConstants.DESCRIPTION_TAB_CLIENT_VENUE_ID_XPATH, value)

    def get_client_venue_id(self):
        return self.get_text_by_xpath(VenuesConstants.DESCRIPTION_TAB_CLIENT_VENUE_ID_XPATH)

    def set_counterpart(self, value):
        self.set_combobox_value(VenuesConstants.DESCRIPTION_TAB_COUNTERPART_XPATH, value)

    def get_counterpart(self):
        return self.get_text_by_xpath(VenuesConstants.DESCRIPTION_TAB_COUNTERPART_XPATH)

    def set_mic(self, value):
        self.set_combobox_value(VenuesConstants.DESCRIPTION_TAB_MIC_XPATH, value)

    def get_mic(self):
        return self.get_text_by_xpath(VenuesConstants.DESCRIPTION_TAB_MIC_XPATH)

    def set_short_name(self, value):
        self.set_text_by_xpath(VenuesConstants.DESCRIPTION_TAB_SHORT_NAME_XPATH, value)

    def get_short_name(self):
        return self.get_text_by_xpath(VenuesConstants.DESCRIPTION_TAB_SHORT_NAME_XPATH)

    def set_route_venue_id(self, value):
        self.set_text_by_xpath(VenuesConstants.DESCRIPTION_TAB_ROUTE_VENUE_ID_XPATH, value)

    def get_route_venue_id(self):
        return self.get_text_by_xpath(VenuesConstants.DESCRIPTION_TAB_ROUTE_VENUE_ID_XPATH)

    def click_on_counterpart_manage_button(self):
        self.find_by_xpath(VenuesConstants.DESCRIPTION_TAB_COUNTERPART_MANAGE_XPATH).click()

    def click_on_mic_manage_button(self):
        self.find_by_xpath(VenuesConstants.VALUES_TAB_MANAGE_MIC_BUTTON_XPATH).click()