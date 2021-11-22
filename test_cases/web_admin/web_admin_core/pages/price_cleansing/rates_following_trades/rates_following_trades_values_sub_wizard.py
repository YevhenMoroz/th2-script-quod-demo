from test_cases.web_admin.web_admin_core.pages.common_page import CommonPage
from test_cases.web_admin.web_admin_core.pages.price_cleansing.rates_following_trades.rates_following_trades_constants import \
    RatesFollowingTradesConstants
from test_cases.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer


class RatesFollowingTradesValuesSubWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def set_name(self, value):
        self.set_text_by_xpath(RatesFollowingTradesConstants.VALUES_TAB_NAME_XPATH, value)

    def get_name(self):
        return self.get_text_by_xpath(RatesFollowingTradesConstants.VALUES_TAB_NAME_XPATH)

    def click_on_remove_detected_price_updates_checkbox(self):
        self.find_by_xpath(
            RatesFollowingTradesConstants.VALUES_TAB_REMOVE_DETECTED_PRICE_UPDATES_CHECKBOX_XPATH).click()

    def set_related_rates_delay(self, value):
        self.set_text_by_xpath(RatesFollowingTradesConstants.VALUES_TAB_RELATED_RATES_DELAY_XPATH, value)

    def get_related_rates_delay(self):
        return self.get_text_by_xpath(RatesFollowingTradesConstants.VALUES_TAB_RELATED_RATES_DELAY_XPATH)
