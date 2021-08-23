from quod_qa.web_admin.web_admin_core.pages.common_page import CommonPage
from quod_qa.web_admin.web_admin_core.pages.fx_market_making.quoting_sessions.quoting_sessions_constants import \
    QuotingSessionsConstants
from quod_qa.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer


class QuotingSessionsClientClientTiersSubWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def click_on_plus(self):
        self.find_by_xpath(QuotingSessionsConstants.CLIENT_CLIENT_TIERS_TAB_PLUS_BUTTON_XPATH).click()

    def click_on_checkmark(self):
        self.find_by_xpath(QuotingSessionsConstants.CLIENT_CLIENT_TIERS_TAB_CHECKMARK_BUTTON_XPATH).click()

    def click_on_close(self):
        self.find_by_xpath(QuotingSessionsConstants.CLIENT_CLIENT_TIERS_TAB_CLOSE_BUTTON_XPATH).click()

    def click_on_edit(self):
        self.find_by_xpath(QuotingSessionsConstants.CLIENT_CLIENT_TIERS_TAB_EDIT_BUTTON_XPATH).click()

    def click_on_delete(self):
        self.find_by_xpath(QuotingSessionsConstants.CLIENT_CLIENT_TIERS_TAB_DELETE_BUTTON_XPATH).click()

    def set_client_client_tier_id(self, value):
        self.set_text_by_xpath(QuotingSessionsConstants.CLIENT_CLIENT_TIERS_TAB_CLIENT_CLIENT_TIER_ID_XPATH, value)

    def get_client_client_tier_id(self):
        return self.get_text_by_xpath(QuotingSessionsConstants.CLIENT_CLIENT_TIERS_TAB_CLIENT_CLIENT_TIER_ID_XPATH)

    def set_client_client_tier_id_filter(self, value):
        self.set_text_by_xpath(QuotingSessionsConstants.CLIENT_CLIENT_TIERS_TAB_CLIENT_CLIENT_TIER_ID_FILTER_XPATH,
                               value)

    def set_client_tier(self, value):
        self.set_combobox_value(QuotingSessionsConstants.CLIENT_CLIENT_TIERS_TAB_CLIENT_TIER_XPATH, value)

    def get_client_tier(self):
        return self.get_text_by_xpath(QuotingSessionsConstants.CLIENT_CLIENT_TIERS_TAB_CLIENT_TIER_XPATH)

    def set_client_tier_filter(self, value):
        self.set_text_by_xpath(QuotingSessionsConstants.CLIENT_CLIENT_TIERS_TAB_CLIENT_TIER_FILTER_XPATH, value)
