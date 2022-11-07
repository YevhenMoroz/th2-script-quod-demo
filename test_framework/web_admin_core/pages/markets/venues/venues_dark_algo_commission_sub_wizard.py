from test_framework.web_admin_core.pages.common_page import CommonPage
from test_framework.web_admin_core.pages.markets.venues.venues_constants import VenuesConstants
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer


class VenuesDarkAlgoCommissionSubWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def set_cost_per_trade(self, value):
        self.set_text_by_xpath(VenuesConstants.DARK_ALGO_COM_COST_PER_TRADE_XPATH, value)

    def set_per_unit_comm_amt(self, value):
        self.set_text_by_xpath(VenuesConstants.DARK_ALGO_COM_PER_UNIT_COMM_AMT_XPATH, value)

    def set_comm_basis_point(self, value):
        self.set_text_by_xpath(VenuesConstants.DARK_ALGO_COM_COMM_BASIS_POINT_XPATH, value)

    def set_spread_discount_proportion(self, value):
        self.set_text_by_xpath(VenuesConstants.DARK_ALGO_COM_SPREAD_DISCOUNT_PROPORTION_XPATH, value)

    def click_on_is_comm_per_unit_checkbox(self):
        self.find_by_xpath(VenuesConstants.DARK_ALGO_COM_IS_COMM_PER_UNIT_XPATH).click()

    def get_cost_per_trade(self):
        return self.get_text_by_xpath(VenuesConstants.DARK_ALGO_COM_COST_PER_TRADE_XPATH)

    def get_per_unit_comm_amt(self):
        return self.get_text_by_xpath(VenuesConstants.DARK_ALGO_COM_PER_UNIT_COMM_AMT_XPATH)

    def get_comm_basis_point(self):
        return self.get_text_by_xpath(VenuesConstants.DARK_ALGO_COM_COMM_BASIS_POINT_XPATH)

    def get_spread_discount_proportion(self):
        return self.get_text_by_xpath(VenuesConstants.DARK_ALGO_COM_SPREAD_DISCOUNT_PROPORTION_XPATH)

    def is_comm_per_unit_checkbox_selected(self):
        return self.is_checkbox_selected(VenuesConstants.DARK_ALGO_COM_IS_COMM_PER_UNIT_XPATH)
