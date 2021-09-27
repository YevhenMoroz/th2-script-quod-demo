from quod_qa.web_admin.web_admin_core.pages.common_page import CommonPage
from quod_qa.web_admin.web_admin_core.pages.reference_data.venues.venues_constants import VenuesConstants
from quod_qa.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer


class VenuesTradingSessionSubWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def click_on_plus_button(self):
        self.find_by_xpath(VenuesConstants.TRADING_SESSION_TAB_PLUS_BUTTON_XPATH).click()

    def click_on_checkmark(self):
        self.find_by_xpath(VenuesConstants.TRADING_SESSION_TAB_CHECKMARK_BUTTON_XPATH).click()

    def click_on_close(self):
        self.find_by_xpath(VenuesConstants.TRADING_SESSION_TAB_CLOSE_BUTTON_XPATH).click()

    def click_on_edit(self):
        self.find_by_xpath(VenuesConstants.TRADING_SESSION_TAB_EDIT_BUTTON_XPATH).click()

    def click_on_delete(self):
        self.find_by_xpath(VenuesConstants.TRADING_SESSION_TAB_DELETE_BUTTON_XPATH).click()

    def set_venue_trading_session_id(self, value):
        self.set_text_by_xpath(VenuesConstants.TRADING_SESSION_TAB_VENUE_TRADING_SESSION_ID_XPATH, value)

    def set_venue_trading_session_id_filter(self, value):
        self.set_text_by_xpath(VenuesConstants.TRADING_SESSION_TAB_VENUE_TRADING_SESSION_ID_FILTER_XPATH, value)

    def get_venue_trading_session_id(self):
        self.get_text_by_xpath(VenuesConstants.TRADING_SESSION_TAB_VENUE_TRADING_SESSION_ID_XPATH)

    def set_trading_session_description(self, value):
        self.set_text_by_xpath(VenuesConstants.TRADING_SESSION_TAB_TRADING_SESSION_DESCRIPTION_XPATH, value)

    def set_trading_session_description_filter(self, value):
        self.set_text_by_xpath(VenuesConstants.TRADING_SESSION_TAB_TRADING_SESSION_DESCRIPTION_XPATH, value)

    def get_trading_session_description(self):
        self.get_text_by_xpath(VenuesConstants.TRADING_SESSION_TAB_TRADING_SESSION_DESCRIPTION_XPATH)
