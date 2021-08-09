from quod_qa.web_admin.web_admin_core.pages.common_page import CommonPage
from quod_qa.web_admin.web_admin_core.pages.fx_market_making.client_tier.client_tier_constants import \
    ClientTierConstants
from quod_qa.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer


class ClientTiersValuesSubWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def set_name(self, value):
        self.set_text_by_xpath(ClientTierConstants.CLIENT_TIER_VALUES_TAB_NAME_XPATH, value)

    def get_name(self):
        return self.get_text_by_xpath(ClientTierConstants.CLIENT_TIER_VALUES_TAB_NAME_XPATH)

    def set_core_spot_price_strategy(self, value):
        self.set_combobox_value(ClientTierConstants.CLIENT_TIER_VALUES_TAB_CORE_SPOT_PRICE_STRATEGY_XPATH, value)

    def get_core_spot_price_strategy(self):
        return self.get_text_by_xpath(ClientTierConstants.CLIENT_TIER_VALUES_TAB_CORE_SPOT_PRICE_STRATEGY_XPATH)
