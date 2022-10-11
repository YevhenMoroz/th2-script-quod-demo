from selenium.webdriver.common.action_chains import ActionChains
from test_framework.web_admin_core.pages.common_page import CommonPage
from test_framework.web_admin_core.pages.market_making.client_tier.client_tier_constants import \
    ClientTierConstants
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer


class ClientTiersInstrumentSweepableQuantitiesSubWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def click_on_plus(self):
        """
        ActionChains helps to avoid falling test when adding several quantities at once.
        (The usual "click" method fails because after adding the first entry, the cursor remains on the "edit" button
        and the pop-up of edit btn covers half of the "+" button)
        """
        element = self.find_by_xpath(ClientTierConstants.CLIENT_TIER_INSTRUMENTS_SWEEPABLE_QUANTITIES_TAB_PLUS_BUTTON_XPATH)
        action = ActionChains(self.web_driver_container.get_driver())
        action.move_to_element(element)
        action.click()
        action.perform()

    def click_on_checkmark(self):
        self.find_by_xpath(
            ClientTierConstants.CLIENT_TIER_INSTRUMENTS_SWEEPABLE_QUANTITIES_TAB_CHECKMARK_BUTTON_XPATH).click()

    def click_on_close(self):
        self.find_by_xpath(
            ClientTierConstants.CLIENT_TIER_INSTRUMENTS_SWEEPABLE_QUANTITIES_TAB_CLOSE_BUTTON_XPATH).click()

    def click_on_edit(self):
        self.find_by_xpath(
            ClientTierConstants.CLIENT_TIER_INSTRUMENTS_SWEEPABLE_QUANTITIES_TAB_EDIT_BUTTON_XPATH).click()

    def click_on_delete(self):
        self.find_by_xpath(
            ClientTierConstants.CLIENT_TIER_INSTRUMENTS_SWEEPABLE_QUANTITIES_TAB_DELETE_BUTTON_XPATH).click()

    def click_on_delete_by_value(self, value):
        self.find_by_xpath(ClientTierConstants
                           .CLIENT_TIER_INSTRUMENTS_SWEEPABLE_QUANTITIES_TAB_DELETE_BY_VALUE_BUTTON_XPATH.format(value)
                           ).click()

    def set_quantity(self, value):
        self.set_text_by_xpath(ClientTierConstants.CLIENT_TIER_INSTRUMENTS_SWEEPABLE_QUANTITIES_TAB_QUANTITY_XPATH,
                               value)

    def get_quantity(self):
        return self.get_text_by_xpath(
            ClientTierConstants.CLIENT_TIER_INSTRUMENTS_SWEEPABLE_QUANTITIES_TAB_QUANTITY_XPATH)

    def set_quantity_filter(self, value):
        self.set_text_by_xpath(
            ClientTierConstants.CLIENT_TIER_INSTRUMENTS_SWEEPABLE_QUANTITIES_TAB_QUANTITY_FILTER_XPATH, value)

    def click_on_published_checkbox(self):
        self.find_by_xpath(ClientTierConstants.CLIENT_TIER_INSTRUMENTS_SWEEPABLE_QUANTITIES_TAB_PUBLISHED_XPATH).click()

    def get_published(self):
        return self.is_checkbox_selected(
            ClientTierConstants.CLIENT_TIER_INSTRUMENTS_SWEEPABLE_QUANTITIES_TAB_PUBLISHED_XPATH)

    def set_published_filter_xpath(self, value):
        self.set_text_by_xpath(
            ClientTierConstants.CLIENT_TIER_INSTRUMENTS_SWEEPABLE_QUANTITIES_TAB_PUBLISHED_FILTER_XPATH, value)
