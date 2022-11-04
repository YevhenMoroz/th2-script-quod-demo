from test_framework.web_admin_core.pages.common_page import CommonPage
from test_framework.web_admin_core.pages.risk_limits.order_tolerance_limits.constants import \
    OrderToleranceLimitsConstants

from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer


class OrderToleranceLimitsValuesSubWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def set_name(self,value):
        self.set_text_by_xpath(OrderToleranceLimitsConstants.VALUES_TAB_NAME_XPATH,value)

    def get_name(self):
        return self.get_text_by_xpath(OrderToleranceLimitsConstants.VALUES_TAB_NAME_XPATH)

    def set_external_id(self,value):
        self.set_text_by_xpath(OrderToleranceLimitsConstants.VALUES_TAB_EXTERNAL_ID_XPATH,value)

    def get_external_id(self):
        return self.get_text_by_xpath(OrderToleranceLimitsConstants.VALUES_TAB_EXTERNAL_ID_XPATH)













































