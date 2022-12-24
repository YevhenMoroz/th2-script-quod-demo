from test_framework.web_admin_core.pages.common_page import CommonPage
from test_framework.web_admin_core.pages.risk_limits.order_tolerance_limits.constants \
    import OrderToleranceLimitsConstants
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer


class OrderToleranceLimitsAssignmentsSubWizardPage(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def set_institution(self, value):
        self.set_combobox_value(OrderToleranceLimitsConstants.ASSIGNMENTS_TAB_INSTITUTIONS, value)

    def clear_institution_field(self):
        self.set_text_by_xpath(OrderToleranceLimitsConstants.ASSIGNMENTS_TAB_INSTITUTIONS, "")

    def get_institution(self):
        return self.get_text_by_xpath(OrderToleranceLimitsConstants.ASSIGNMENTS_TAB_INSTITUTIONS)

    def is_institutions_field_enable(self):
        return self.is_field_enabled(OrderToleranceLimitsConstants.ASSIGNMENTS_TAB_INSTITUTIONS)

