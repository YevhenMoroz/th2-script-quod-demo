from test_framework.web_admin_core.pages.common_page import CommonPage
from test_framework.web_admin_core.pages.site.locations.locations_constants import LocationsConstants
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer


class LocationsValuesSubWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def set_name(self, value):
        self.set_text_by_xpath(LocationsConstants.VALUES_TAB_NAME_XPATH, value)

    def get_name(self):
        return self.get_text_by_xpath(LocationsConstants.VALUES_TAB_NAME_XPATH)
