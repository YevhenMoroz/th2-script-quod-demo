from quod_qa.web_admin.web_admin_core.pages.common_page import CommonPage
from quod_qa.web_admin.web_admin_core.pages.price_cleansing.unbalanced_rates.unbalanced_rates_constants import \
    UnbalancedRatesConstants
from quod_qa.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer


class UnbalancedRatesValuesSubWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def set_name(self, value):
        self.set_text_by_xpath(UnbalancedRatesConstants.VALUES_TAB_NAME_XPATH, value)

    def get_name(self):
        return self.get_text_by_xpath(UnbalancedRatesConstants.VALUES_TAB_NAME_XPATH)

    def click_on_remove_detected_price_updates_checkbox(self):
        self.find_by_xpath(
            UnbalancedRatesConstants.VALUES_TAB_REMOVE_DETECTED_PRICE_UPDATES_CHECKBOX_XPATH).click()

    def click_on_enrich_empty_side_of_book(self):
        self.find_by_xpath(UnbalancedRatesConstants.VALUES_TAB_ENRICH_EMPTY_SIDE_OF_BOOK_XPATH).click()
