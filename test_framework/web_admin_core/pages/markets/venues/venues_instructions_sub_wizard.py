from test_framework.web_admin_core.pages.common_page import CommonPage
from test_framework.web_admin_core.pages.markets.venues.venues_constants import VenuesConstants
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer


class VenuesInstructionsSubWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def set_instructions(self, value):
        self.set_checkbox_list(VenuesConstants.INSTRUCTIONS_TAB_INSTRUCTIONS_XPATH, value)

    def set_ord_capacity(self, value):
        self.set_checkbox_list(VenuesConstants.INSTRUCTIONS_TAB_ORD_CAPACITY_XPATH, value)
