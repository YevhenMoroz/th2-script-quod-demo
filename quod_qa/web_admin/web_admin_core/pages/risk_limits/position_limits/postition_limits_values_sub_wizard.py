from quod_qa.web_admin.web_admin_core.pages.common_page import CommonPage
from quod_qa.web_admin.web_admin_core.pages.risk_limits.position_limits.position_limits_constants import \
    PositionsLimitsConstants
from quod_qa.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer


class PositionLimitsValuesSubWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def set_min_soft_qty(self, value):
        self.set_text_by_xpath(PositionsLimitsConstants.VALUES_TAB_MIN_SOFT_QTY_XPATH, value)

    def get_min_soft_qty(self):
        return self.get_text_by_xpath(PositionsLimitsConstants.VALUES_TAB_MIN_SOFT_QTY_XPATH)

    def set_min_soft_amt(self, value):
        self.set_text_by_xpath(PositionsLimitsConstants.VALUES_TAB_MIN_SOFT_AMT_XPATH, value)

    def get_min_soft_amt(self):
        return self.get_text_by_xpath(PositionsLimitsConstants.VALUES_TAB_MIN_SOFT_AMT_XPATH)

    def set_max_soft_qty(self, value):
        self.set_text_by_xpath(PositionsLimitsConstants.VALUES_TAB_MAX_SOFT_QTY_XPATH, value)

    def get_max_soft_qty(self):
        return self.get_text_by_xpath(PositionsLimitsConstants.VALUES_TAB_MAX_SOFT_QTY_XPATH)

    def set_max_soft_amt(self, value):
        self.set_text_by_xpath(PositionsLimitsConstants.VALUES_TAB_MAX_SOFT_AMT_XPATH, value)

    def get_max_soft_amt(self):
        return self.get_text_by_xpath(PositionsLimitsConstants.VALUES_TAB_MAX_SOFT_AMT_XPATH)

    def set_min_hard_qty(self, value):
        self.set_text_by_xpath(PositionsLimitsConstants.VALUES_TAB_MIN_HARD_QTY_XPATH, value)

    def get_min_hard_qty(self):
        return self.get_text_by_xpath(PositionsLimitsConstants.VALUES_TAB_MIN_HARD_QTY_XPATH)

    def set_min_hard_amt(self, value):
        self.set_text_by_xpath(PositionsLimitsConstants.VALUES_TAB_MIN_HARD_AMT_XPATH, value)

    def get_min_hard_amt(self):
        return self.get_text_by_xpath(PositionsLimitsConstants.VALUES_TAB_MIN_HARD_AMT_XPATH)

    def set_max_hard_qty(self, value):
        self.set_text_by_xpath(PositionsLimitsConstants.VALUES_TAB_MAX_HARD_QTY_XPATH, value)

    def get_max_hard_qty(self):
        return self.get_text_by_xpath(PositionsLimitsConstants.VALUES_TAB_MAX_HARD_QTY_XPATH)

    def set_max_hard_amt(self, value):
        self.set_text_by_xpath(PositionsLimitsConstants.VALUES_TAB_MAX_HARD_AMT_XPATH, value)

    def get_max_hard_amt(self):
        return self.get_text_by_xpath(PositionsLimitsConstants.VALUES_TAB_MAX_HARD_AMT_XPATH)

    def set_currency(self, value):
        self.set_combobox_value(PositionsLimitsConstants.VALUES_TAB_CURRENCY_XPATH, value)

    def get_currency(self):
        return self.get_text_by_xpath(PositionsLimitsConstants.VALUES_TAB_CURRENCY_XPATH)
