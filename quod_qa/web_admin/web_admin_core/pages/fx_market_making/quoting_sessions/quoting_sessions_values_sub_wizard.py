from quod_qa.web_admin.web_admin_core.pages.common_page import CommonPage
from quod_qa.web_admin.web_admin_core.pages.fx_market_making.quoting_sessions.quoting_sessions_constants import \
    QuotingSessionsConstants

from quod_qa.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer


class QuotingSessionsValuesSubWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def set_name(self, value):
        self.set_text_by_xpath(QuotingSessionsConstants.VALUES_TAB_NAME_XPATH, value)

    def get_name(self):
        return self.get_text_by_xpath(QuotingSessionsConstants.VALUES_TAB_NAME_XPATH)

    def set_concurrently_active_quotes_age(self, value):
        self.set_text_by_xpath(QuotingSessionsConstants.VALUES_TAB_CONCURRENTLY_ACTIVE_QUOTES_AGE_XPATH, value)

    def get_concurrently_active_quotes(self):
        return self.get_text_by_xpath(QuotingSessionsConstants.VALUES_TAB_CONCURRENTLY_ACTIVE_QUOTES_AGE_XPATH)

    def set_quote_update_interval(self, value: int):
        self.set_text_by_xpath(QuotingSessionsConstants.VALUES_TAB_QUOTE_UPDATE_INTERVAL_XPATH, str(value))

    def get_quote_update_interval(self):
        return self.get_text_by_xpath(QuotingSessionsConstants.VALUES_TAB_QUOTE_UPDATE_INTERVAL_XPATH)

    def set_published_quote_id_format(self, value):
        self.set_text_by_xpath(QuotingSessionsConstants.VALUES_TAB_PUBLISHED_QUOTE_ID_FORMAT_XPATH, value)

    def get_published_quote_id_format(self):
        return self.get_text_by_xpath(QuotingSessionsConstants.VALUES_TAB_PUBLISHED_QUOTE_ID_FORMAT_XPATH)

    def set_quote_update_format(self, value):
        self.set_combobox_value(QuotingSessionsConstants.VALUES_TAB_QUOTE_UPDATE_FORMAT_XPATH, value)

    def get_quote_update_format(self):
        return self.get_text_by_xpath(QuotingSessionsConstants.VALUES_TAB_QUOTE_UPDATE_FORMAT_XPATH)

    def click_on_always_use_new_md_entry_id_checkbox(self):
        self.find_by_xpath(QuotingSessionsConstants.VALUES_TAB_ALWAYS_USER_NEW_MD_ENTRY_ID_CHECKBOX).click()

    def click_on_always_acknowledge_orders_checkbox(self):
        self.find_by_xpath(QuotingSessionsConstants.VALUES_TAB_ALWAYS_ACKNOWLEDGE_CHECKBOX).click()

    def click_on_wait_for_market_data_subscriptions(self):
        self.find_by_xpath(QuotingSessionsConstants.VALUES_TAB_WAIT_FOR_MARKET_DATE_SUBSCRIPTIONS_CHECKBOX).click()

    def click_on_use_same_session_for_market_date_and_trading(self):
        self.find_by_xpath(
            QuotingSessionsConstants.VALUES_TAB_USE_SAME_SESSION_FOR_MARKET_DATA_AND_TRADING_CHECKBOX).click()
