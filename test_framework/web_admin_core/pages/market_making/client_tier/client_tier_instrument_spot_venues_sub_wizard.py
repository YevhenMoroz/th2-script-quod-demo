from test_framework.web_admin_core.pages.common_page import CommonPage
from test_framework.web_admin_core.pages.market_making.client_tier.client_tier_constants import \
    ClientTierConstants
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer


class ClientTiersInstrumentSpotVenuesSubWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def click_on_plus(self):
        self.find_by_xpath(ClientTierConstants.CLIENT_TIER_INSTRUMENTS_SPOT_VENUES_TAB_PLUS_BUTTON_XPATH).click()

    def click_on_checkmark(self):
        self.find_by_xpath(ClientTierConstants.CLIENT_TIER_INSTRUMENTS_SPOT_VENUES_TAB_CHECKMARK_BUTTON_XPATH).click()

    def click_on_close(self):
        self.find_by_xpath(ClientTierConstants.CLIENT_TIER_INSTRUMENTS_SPOT_VENUES_TAB_CLOSE_BUTTON_XPATH).click()

    def click_on_edit(self):
        self.find_by_xpath(ClientTierConstants.CLIENT_TIER_INSTRUMENTS_SPOT_VENUES_TAB_EDIT_BUTTON_XPATH).click()

    def click_on_delete(self):
        self.find_by_xpath(ClientTierConstants.CLIENT_TIER_INSTRUMENTS_SPOT_VENUES_TAB_DELETE_BUTTON_XPATH).click()

    def set_venue(self, value):
        self.set_combobox_value(ClientTierConstants.CLIENT_TIER_INSTRUMENTS_SPOT_VENUES_TAB_VENUE_XPATH, value)

    def get_venue(self):
        return self.find_by_xpath(ClientTierConstants.CLIENT_TIER_INSTRUMENTS_SPOT_VENUES_TAB_VENUE_XPATH)

    def click_on_critical_venue_checkbox(self):
        self.find_by_xpath(
            ClientTierConstants.CLIENT_TIER_INSTRUMENTS_SPOT_VENUES_TAB_CRITICAL_VENUE_CHECKBOX_XPATH).click()

    def get_critical_venue_checkbox(self):
        return self.is_checkbox_selected(
            ClientTierConstants.CLIENT_TIER_INSTRUMENTS_SPOT_VENUES_TAB_CRITICAL_VENUE_CHECKBOX_XPATH)

    def set_critical_venue_filter(self, value):
        self.set_text_by_xpath(ClientTierConstants.CLIENT_TIER_INSTRUMENTS_SPOT_VENUES_TAB_CRITICAL_VENUE_FILTER_XPATH,
                               value)

    def click_on_exclude_when_unhealthy(self):
        self.find_by_xpath(
            ClientTierConstants.CLIENT_TIER_INSTRUMENTS_SPOT_VENUES_TAB_EXCLUDE_WHEN_UNHEALTHY_CHECKBOX_XPATH).click()

    def get_exclude_when_unhealthy(self):
        return self.is_checkbox_selected(
            ClientTierConstants.CLIENT_TIER_INSTRUMENTS_SPOT_VENUES_TAB_EXCLUDE_WHEN_UNHEALTHY_CHECKBOX_XPATH)

    def set_exclude_when_unhealthy_filter(self, value):
        self.set_text_by_xpath(
            ClientTierConstants.CLIENT_TIER_INSTRUMENTS_SPOT_VENUES_TAB_EXCLUDE_WHEN_UNHEALTHY_FILTER_XPATH, value)

    def set_default_weight(self, value):
        self.set_text_by_xpath(ClientTierConstants.CLIENT_TIER_INSTRUMENTS_SPOT_VENUES_TAB_DEFAULT_WEIGHT_XPATH, value)

    def get_default_weight(self):
        return self.get_text_by_xpath(ClientTierConstants.CLIENT_TIER_INSTRUMENTS_SPOT_VENUES_TAB_DEFAULT_WEIGHT_XPATH)

    def set_default_weight_filter(self, value):
        self.set_text_by_xpath(ClientTierConstants.CLIENT_TIER_INSTRUMENTS_SPOT_VENUES_TAB_DEFAULT_WEIGHT_FILTER_XPATH,
                               value)
