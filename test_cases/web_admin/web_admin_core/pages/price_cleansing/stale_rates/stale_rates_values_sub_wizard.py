from test_cases.web_admin.web_admin_core.pages.common_page import CommonPage
from test_cases.web_admin.web_admin_core.pages.price_cleansing.stale_rates.stale_rates_constants import StaleRatesConstants
from test_cases.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer


class StaleRatesValuesSubWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def set_name(self, value):
        self.set_text_by_xpath(StaleRatesConstants.VALUES_TAB_NAME_XPATH, value)

    def get_name(self):
        return self.get_text_by_xpath(StaleRatesConstants.VALUES_TAB_NAME_XPATH)

    def click_on_remove_detected_price_updates_checkbox(self):
        self.find_by_xpath(StaleRatesConstants.VALUES_TAB_REMOVE_DETECTED_PRICE_UPDATES_CHECKBOX_XPATH).click()
    
    def set_stale_rates_delay(self,value):
        self.set_text_by_xpath(StaleRatesConstants.VALUES_TAB_STALE_RATES_DELAY_XPATH,value)

    def get_stale_rates_delay(self):
        return self.get_text_by_xpath(StaleRatesConstants.VALUES_TAB_STALE_RATES_DELAY_XPATH)
