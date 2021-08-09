from quod_qa.web_admin.web_admin_core.pages.common_page import CommonPage
from quod_qa.web_admin.web_admin_core.pages.fx_market_making.client_tier.client_tier_constants import \
    ClientTierConstants
from quod_qa.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer


class ClientTiersInstrumentInternalClientsSubWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def click_on_plus(self):
        self.find_by_xpath(ClientTierConstants.CLIENT_TIER_INSTRUMENTS_INTERNAL_CLIENTS_TAB_PLUS_BUTTON_XPATH).click()

    def click_on_checkmark(self):
        self.find_by_xpath(
            ClientTierConstants.CLIENT_TIER_INSTRUMENTS_INTERNAL_CLIENTS_TAB_CHECKMARK_BUTTON_XPATH).click()

    def click_on_close(self):
        self.find_by_xpath(ClientTierConstants.CLIENT_TIER_INSTRUMENTS_INTERNAL_CLIENTS_TAB_CLOSE_BUTTON_XPATH).click()

    def click_on_edit(self):
        self.find_by_xpath(ClientTierConstants.CLIENT_TIER_INSTRUMENTS_INTERNAL_CLIENTS_TAB_EDIT_BUTTON_XPATH).click()

    def click_on_delete(self):
        self.find_by_xpath(ClientTierConstants.CLIENT_TIER_INSTRUMENTS_INTERNAL_CLIENTS_TAB_DELETE_BUTTON_XPATH).click()

    def set_client(self, value):
        self.set_combobox_value(ClientTierConstants.CLIENT_TIER_INSTRUMENTS_INTERNAL_CLIENTS_TAB_CLIENT_XPATH, value)

    def set_client_filter(self, value):
        self.set_text_by_xpath(ClientTierConstants.CLIENT_TIER_INSTRUMENTS_INTERNAL_CLIENTS_TAB_CLIENT_FILTER_XPATH,
                               value)

    def get_client(self):
        return self.get_text_by_xpath(ClientTierConstants.CLIENT_TIER_INSTRUMENTS_INTERNAL_CLIENTS_TAB_CLIENT_XPATH)
