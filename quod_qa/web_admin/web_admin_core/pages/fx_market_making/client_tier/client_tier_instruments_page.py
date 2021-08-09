from quod_qa.web_admin.web_admin_core.pages.common_page import CommonPage
from quod_qa.web_admin.web_admin_core.pages.fx_market_making.client_tier.client_tier_constants import \
    ClientTierConstants
from quod_qa.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer


class ClientTierInstrumentsPage(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    # region more actions
    def click_on_more_actions(self):
        self.find_by_xpath(ClientTierConstants.CLIENT_TIER_INSTRUMENTS_MORE_ACTIONS_XPATH).click()

    def click_on_cancel(self):
        self.find_by_xpath(ClientTierConstants.CANCEL_BUTTON_XPATH).click()

    def click_on_ok_xpath(self):
        self.find_by_xpath(ClientTierConstants.OK_BUTTON_XPATH).click()

    def click_on_edit(self):
        self.find_by_xpath(ClientTierConstants.MAIN_PAGE_CLIENT_TIER_INSTRUMENTS_EDIT_XPATH).click()

    def click_on_clone(self):
        self.find_by_xpath(ClientTierConstants.MAIN_PAGE_CLIENT_TIER_INSTRUMENTS_CLONE_XPATH).click()

    # endregion

    # region filter setters
    def set_symbol(self, value):
        self.set_text_by_xpath(ClientTierConstants.MAIN_PAGE_CLIENT_TIER_INSTRUMENTS_SYMBOL_FILTER_XPATH, value)

    def set_rfq_response_stream_ttl(self, value):
        self.set_text_by_xpath(
            ClientTierConstants.MAIN_PAGE_CLIENT_TIER_INSTRUMENTS_RFQ_RESPONSE_STREAM_TTL_FILTER_XPATH, value)

    def set_core_spot_price_strategy(self, value):
        self.set_text_by_xpath(
            ClientTierConstants.MAIN_PAGE_CLIENT_TIER_INSTRUMENTS_CORE_SPOT_PRICE_STRATEGY_FILTER_XPATH, value)

    def set_enabled_schedule(self, value):
        self.select_value_from_dropdown_list(ClientTierConstants.MAIN_PAGE_CLIENT_TIER_INSTRUMENTS_ENABLED_FILTER_XPATH,
                                             value)

    # endregion

    def click_on_enable_disable(self):
        self.find_by_xpath(ClientTierConstants.MAIN_PAGE_CLIENT_TIER_INSTRUMENTS_ENABLED_DISABLED_BUTTON_XPATH).click()

    def click_on_new(self):
        self.find_by_xpath(ClientTierConstants.MAIN_PAGE_CLIENT_TIER_INSTRUMENTS_NEW_BUTTON_XPATH).click()

    def click_on_download_csv(self):
        self.find_by_xpath(ClientTierConstants.MAIN_PAGE_CLIENT_TIER_INSTRUMENTS_DOWNLOAD_CSV_XPATH).click()
