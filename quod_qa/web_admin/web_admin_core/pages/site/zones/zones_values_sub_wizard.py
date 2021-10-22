from quod_qa.web_admin.web_admin_core.pages.common_page import CommonPage
from quod_qa.web_admin.web_admin_core.pages.site.zones.zones_constants import ZonesConstants
from quod_qa.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer


class ZonesValuesSubWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def set_name(self, value):
        self.set_text_by_xpath(ZonesConstants.VALUES_TAB_NAME_XPATH, value)

    def get_name(self):
        return self.get_text_by_xpath(ZonesConstants.VALUES_TAB_NAME_XPATH)
