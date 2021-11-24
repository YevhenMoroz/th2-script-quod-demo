from test_cases.web_admin.web_admin_core.pages.common_page import CommonPage
from test_cases.web_admin.web_admin_core.pages.general.mdentitlements.mdentitlements_constants import \
    MDEntitlementsConstants
from test_cases.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer


class MDEntitlementsValuesSubWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def click_on_tick_by_tick_depth_checkbox(self):
        self.find_by_xpath(MDEntitlementsConstants.VALUES_TAB_TICK_BY_TICK_DEPTH_CHECKBOX_XPATH).click()

    def is_tick_by_tick_depth_checkbox_selected(self):
        return self.is_checkbox_selected(MDEntitlementsConstants.VALUES_TAB_TICK_BY_TICK_DEPTH_CHECKBOX_XPATH)

    def click_on_historical_checkbox(self):
        self.find_by_xpath(MDEntitlementsConstants.VALUES_TAB_HISTORICAL_CHECKBOX_XPATH).click()

    def is_historical_checkbox_selected(self):
        self.is_checkbox_selected(MDEntitlementsConstants.VALUES_TAB_HISTORICAL_CHECKBOX_XPATH)

    def click_on_times_and_sales_checkbox(self):
        self.find_by_xpath(MDEntitlementsConstants.VALUES_TAB_TIMES_AND_SALES_CHECKBOX_XPATH).click()

    def is_times_and_sales_checkbox_selected(self):
        self.is_checkbox_selected(MDEntitlementsConstants.VALUES_TAB_TIMES_AND_SALES_CHECKBOX_XPATH)

    def click_on_delayed_quote_checkbox(self):
        self.find_by_xpath(MDEntitlementsConstants.VALUES_TAB_DELAYED_QUOTE_CHECKBOX_XPATH).click()

    def is_delayed_quote_checkbox_selected(self):
        self.is_checkbox_selected(MDEntitlementsConstants.VALUES_TAB_DELAYED_QUOTE_CHECKBOX_XPATH)

    def click_on_delayed_depth_checkbox(self):
        self.find_by_xpath(MDEntitlementsConstants.VALUES_TAB_DELAYED_DEPTH_CHECKBOX_XPATH).click()

    def is_delayed_depth_checkbox_selected(self):
        self.is_checkbox_selected(MDEntitlementsConstants.VALUES_TAB_DELAYED_DEPTH_CHECKBOX_XPATH)

    def click_on_tick_by_tick_quote_checkbox(self):
        self.find_by_xpath(MDEntitlementsConstants.VALUES_TAB_TICK_BY_TICK_QUOTE_CHECKBOX_XPATH).click()

    def is_tick_by_tick_quote_checkbox_selected(self):
        self.is_checkbox_selected(MDEntitlementsConstants.VALUES_TAB_TICK_BY_TICK_QUOTE_CHECKBOX_XPATH)

    def click_on_news_checkbox(self):
        self.find_by_xpath(MDEntitlementsConstants.VALUES_TAB_NEWS_CHECKBOX_XPATH).click()

    def is_news_checkbox_selected(self):
        self.is_checkbox_selected(MDEntitlementsConstants.VALUES_TAB_NEWS_CHECKBOX_XPATH)

    def click_on_intraday_checkbox(self):
        self.find_by_xpath(MDEntitlementsConstants.VALUES_TAB_INTRADAY_CHECKBOX_XPATH).click()

    def is_intraday_checkbox_selected(self):
        self.is_checkbox_selected(MDEntitlementsConstants.VALUES_TAB_INTRADAY_CHECKBOX_XPATH)
