from test_framework.web_admin_core.pages.common_page import CommonPage
from test_framework.web_admin_core.pages.markets.listings.listings_constants import ListingsConstants
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer


class ListingsShortShellSubWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def click_on_allow_short_sell(self):
        self.find_by_xpath(ListingsConstants.SHORT_SELL_TAB_ALLOW_SHORT_SELL_CHECKBOX_XPATH).click()

    def is_allow_short_sell_checked(self):
        return self.is_checkbox_selected(ListingsConstants.SHORT_SELL_TAB_ALLOW_SHORT_SELL_CHECKBOX_XPATH)

    def set_disable_update_time(self,value):
        self.set_text_by_xpath(ListingsConstants.SHORT_SELL_TAB_DISABLE_UPDATE_TIME_XPATH,value)

    def get_disable_update_time(self):
        return self.get_text_by_xpath(ListingsConstants.SHORT_SELL_TAB_DISABLE_UPDATE_TIME_XPATH)

    def set_disable_percent(self,value):
        self.set_text_by_xpath(ListingsConstants.SHORT_SELL_TAB_DISABLE_PERCENT_XPATH,value)

    def get_disable_percent(self):
        self.get_text_by_xpath(ListingsConstants.SHORT_SELL_TAB_DISABLE_PERCENT_XPATH)

    def set_disable_until_date(self,value):
        self.set_text_by_xpath(ListingsConstants.SHORT_SELL_TAB_DISABLE_UNTIL_DATE_XPATH,value)

    def get_disable_until_date(self):
        return self.get_text_by_xpath(ListingsConstants.SHORT_SELL_TAB_DISABLE_UNTIL_DATE_XPATH)

