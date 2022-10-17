import time

from test_framework.web_admin_core.pages.common_page import CommonPage
from test_framework.web_admin_core.pages.reference_data.venues.venues_constants import VenuesConstants
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer


class VenuesValuesSubWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def set_name(self, value):
        self.set_text_by_xpath(VenuesConstants.VALUES_TAB_NAME_XPATH, value)

    def get_name(self):
        return self.get_text_by_xpath(VenuesConstants.VALUES_TAB_NAME_XPATH)

    def set_country(self, value):
        self.set_combobox_value(VenuesConstants.VALUES_TAB_COUNTRY_XPATH, value)

    def set_country_custom_value(self, value):
        self.set_text_by_xpath(VenuesConstants.VALUES_TAB_COUNTRY_XPATH, value)

    def get_country(self):
        return self.get_text_by_xpath(VenuesConstants.VALUES_TAB_COUNTRY_XPATH)

    def set_very_short_name(self, value):
        self.set_text_by_xpath(VenuesConstants.VALUES_TAB_VERY_SHORT_NAME_XPATH, value)

    def get_very_short_name(self):
        return self.get_text_by_xpath(VenuesConstants.VALUES_TAB_VERY_SHORT_NAME_XPATH)

    def set_type(self, value):
        self.set_combobox_value(VenuesConstants.VALUES_TAB_TYPE_XPATH, value)

    def set_type_custom_value(self, value):
        self.set_text_by_xpath(VenuesConstants.VALUES_TAB_TYPE_XPATH, value)

    def get_type(self):
        return self.get_text_by_xpath(VenuesConstants.VALUES_TAB_TYPE_XPATH)

    def set_bic(self, value):
        self.set_text_by_xpath(VenuesConstants.VALUES_TAB_BIC_XPATH, value)

    def get_bic(self):
        return self.get_text_by_xpath(VenuesConstants.VALUES_TAB_BIC_XPATH)

    def set_id(self, value):
        self.set_text_by_xpath(VenuesConstants.VALUES_TAB_ID_XPATH, value)

    def get_id(self):
        return self.get_text_by_xpath(VenuesConstants.VALUES_TAB_ID_XPATH)

    def set_category(self, value):
        self.set_text_by_xpath(VenuesConstants.VALUES_TAB_CATEGORY_XPATH, value)

    def get_category(self):
        self.get_text_by_xpath(VenuesConstants.VALUES_TAB_CATEGORY_XPATH)

    def set_client_venue_id(self, value):
        self.set_text_by_xpath(VenuesConstants.VALUES_TAB_CLIENT_VENUE_ID_XPATH, value)

    def get_client_venue_id(self):
        return self.get_text_by_xpath(VenuesConstants.VALUES_TAB_CLIENT_VENUE_ID_XPATH)

    def set_counterpart(self, value):
        self.set_combobox_value(VenuesConstants.VALUES_TAB_COUNTERPART_XPATH, value)

    def set_counterpart_custom_value(self, value):
        self.set_text_by_xpath(VenuesConstants.VALUES_TAB_COUNTERPART_XPATH, value)

    def get_counterpart(self):
        return self.get_text_by_xpath(VenuesConstants.VALUES_TAB_COUNTERPART_XPATH)

    def set_mic(self, value):
        self.set_combobox_value(VenuesConstants.VALUES_TAB_MIC_XPATH, value)

    def get_mic(self):
        return self.get_text_by_xpath(VenuesConstants.VALUES_TAB_MIC_XPATH)

    def set_short_name(self, value):
        self.set_text_by_xpath(VenuesConstants.VALUES_TAB_SHORT_NAME_XPATH, value)

    def get_short_name(self):
        return self.get_text_by_xpath(VenuesConstants.VALUES_TAB_SHORT_NAME_XPATH)

    def set_route_venue_id(self, value):
        self.set_text_by_xpath(VenuesConstants.VALUES_TAB_ROUTE_VENUE_ID_XPATH, value)

    def get_route_venue_id(self):
        return self.get_text_by_xpath(VenuesConstants.VALUES_TAB_ROUTE_VENUE_ID_XPATH)

    def click_on_counterpart_manage_button(self):
        self.find_by_xpath(VenuesConstants.VALUES_TAB_COUNTERPART_MANAGE_XPATH).click()

    def click_on_mic_manage_button(self):
        self.find_by_xpath(VenuesConstants.VALUES_TAB_MANAGE_MIC_BUTTON_XPATH).click()

    def is_not_found_present_in_drop_menu(self):
        return self.find_by_xpath(VenuesConstants.NOT_FOUND_OPTION_IN_DROP_DOWN_XPATH).text

    def set_position_flattening_period(self, value):
        self.set_checkbox_list(VenuesConstants.VALUES_TAB_POSITION_FLATTENING_PERIOD_XPATH, value)

    def get_position_flattening_period(self):
        return self.get_text_by_xpath(VenuesConstants.VALUES_TAB_POSITION_FLATTENING_PERIOD_XPATH)

    def get_all_position_flattening_period_drop_menu(self):
        self.find_by_xpath(VenuesConstants.VALUES_TAB_POSITION_FLATTENING_PERIOD_XPATH).click()
        time.sleep(1)
        return self.get_all_items_from_drop_down(VenuesConstants.VALUES_TAB_POSITION_FLATTENING_PERIOD_DROP_DOWN_MENU_XPATH)

    def is_all_position_flattening_period_entity_selected(self):
        self.find_by_xpath(VenuesConstants.VALUES_TAB_POSITION_FLATTENING_PERIOD_XPATH).click()
        time.sleep(1)
        all_checkboxes = self.find_elements_by_xpath(VenuesConstants.VALUES_TAB_POSITION_FLATTENING_PERIOD_CHECKBOXES_AT_DROP_DOWN_XPATH)
        selected_checkboxes = [True if 'checked' in i.get_attribute('class') else False for i in all_checkboxes]
        return True if False not in selected_checkboxes else False
