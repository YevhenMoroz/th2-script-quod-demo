import time

from test_framework.web_admin_core.pages.common_page import CommonPage
from test_framework.web_admin_core.pages.market_making.client_tier.client_tier_constants import \
    ClientTierConstants
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer


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

    def is_client_tier_instrument_enabled(self):
        '''
         Method was created for check is client tier instrument enable or disable, if enable (aria-checked return true)
         if not , that's mean entity disabled
        '''
        return self.find_by_xpath(
            ClientTierConstants.MAIN_PAGE_CLIENT_TIER_INSTRUMENTS_ENABLE_DISABLE_ARIA_CHECK_XPATH).get_attribute(
            'aria-checked') == "true"

    def click_on_new(self):
        self.find_by_xpath(ClientTierConstants.MAIN_PAGE_CLIENT_TIER_INSTRUMENTS_NEW_BUTTON_XPATH).click()

    def click_on_download_csv(self):
        self.find_by_xpath(ClientTierConstants.MAIN_PAGE_CLIENT_TIER_INSTRUMENTS_DOWNLOAD_CSV_XPATH).click()

    def click_download_pdf_entity_button_and_check_pdf(self, value):
        self.clear_download_directory()
        self.find_by_xpath(ClientTierConstants.MAIN_PAGE_CLIENT_TIER_INSTRUMENTS_DOWNLOAD_PDF_XPATH).click()
        time.sleep(2)
        return self.is_pdf_contains_value(value)

    def get_core_spot_price_strategy(self):
        return self.find_by_xpath(
            ClientTierConstants.MAIN_PAGE_CLIENT_TIER_INSTRUMENTS_CORE_SPOT_PRICE_STRATEGY_XPATH).text
