from selenium.webdriver import ActionChains

from test_framework.web_admin_core.pages.common_page import CommonPage
from test_framework.web_admin_core.pages.market_making.quoting_sessions.quoting_sessions_constants import \
    QuotingSessionsConstants
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer


class QuotingSessionsClientTiersSymbolsSubWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def click_on_plus(self):
        """
        ActionChains helps to avoid falling test when adding several quantities at once.
        (The usual "click" method fails because after adding the first entry, the cursor remains on the "edit" button
        and the pop-up of edit btn covers half of the "+" button)
        """
        element = self.find_by_xpath(QuotingSessionsConstants.CLIENT_TIER_SYMBOLS_TAB_PLUS_BUTTON_XPATH)
        action = ActionChains(self.web_driver_container.get_driver())
        action.move_to_element(element)
        action.click()
        action.perform()

    def click_on_checkmark(self):
        self.find_by_xpath(QuotingSessionsConstants.CLIENT_TIER_SYMBOLS_TAB_CHECKMARK_BUTTON_XPATH).click()

    def click_on_close(self):
        self.find_by_xpath(QuotingSessionsConstants.CLIENT_TIER_SYMBOLS_TAB_CLOSE_BUTTON_XPATH).click()

    def click_on_edit(self):
        self.find_by_xpath(QuotingSessionsConstants.CLIENT_TIER_SYMBOLS_TAB_EDIT_BUTTON_XPATH).click()

    def click_on_delete(self):
        self.find_by_xpath(QuotingSessionsConstants.CLIENT_TIER_SYMBOLS_TAB_DELETE_BUTTON_XPATH).click()

    def set_symbol(self, value):
        self.set_combobox_value(QuotingSessionsConstants.CLIENT_TIER_SYMBOLS_TAB_SYMBOL_XPATH, value)

    def get_symbol(self):
        return self.get_text_by_xpath(QuotingSessionsConstants.CLIENT_TIER_SYMBOLS_TAB_SYMBOL_XPATH)

    def set_symbol_filter(self, value):
        self.set_text_by_xpath(QuotingSessionsConstants.CLIENT_TIER_SYMBOLS_TAB_SYMBOL_FILTER_XPATH, value)

    def set_client_tier(self, value):
        self.set_combobox_value(QuotingSessionsConstants.CLIENT_TIER_SYMBOLS_TAB_CLIENT_TIER_XPATH, value)

    def get_client_tier(self):
        return self.get_text_by_xpath(QuotingSessionsConstants.CLIENT_TIER_SYMBOLS_TAB_CLIENT_TIER_XPATH)

    def set_client_tier_filter(self, value):
        self.set_text_by_xpath(QuotingSessionsConstants.CLIENT_TIER_SYMBOLS_TAB_CLIENT_TIER_FILTER_XPATH, value)

    def set_broadcast_client_client_tier_id(self, value):
        self.set_text_by_xpath(QuotingSessionsConstants.CLIENT_TIER_SYMBOLS_TAB_BROADCAST_CLIENT_CLIENT_TIER_ID_XPATH,
                               value)

    def get_broadcast_client_client_tier_id(self):
        return self.get_text_by_xpath(
            QuotingSessionsConstants.CLIENT_TIER_SYMBOLS_TAB_BROADCAST_CLIENT_CLIENT_TIER_ID_XPATH)

    def set_broadcast_client_client_tier_id_filter(self, value):
        self.set_text_by_xpath(QuotingSessionsConstants.CLIENT_TIER_SYMBOLS_TAB_BROADCAST_CLIENT_CLIENT_TIER_ID_XPATH,
                               value)
