from test_framework.web_admin_core.pages.common_page import CommonPage
from test_framework.web_admin_core.pages.markets.venues.venues_constants import VenuesConstants
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer


class VenuesSorCriteriaSubWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def set_settlement_rank(self, value):
        self.set_text_by_xpath(VenuesConstants.SOR_CRITERIA_TAB_SETTLEMENT_RANK_XPATH, value)

    def get_settlement_rank(self):
        self.get_text_by_xpath(VenuesConstants.SOR_CRITERIA_TAB_SETTLEMENT_RANK_XPATH)

    def set_latency(self, value):
        self.set_text_by_xpath(VenuesConstants.SOR_CRITERIA_TAB_LATENCY_XPATH, value)

    def get_latency(self):
        self.get_text_by_xpath(VenuesConstants.SOR_CRITERIA_TAB_LATENCY_XPATH)
