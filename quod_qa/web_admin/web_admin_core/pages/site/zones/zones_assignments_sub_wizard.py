from quod_qa.web_admin.web_admin_core.pages.common_page import CommonPage
from quod_qa.web_admin.web_admin_core.pages.site.zones.zones_constants import ZonesConstants
from quod_qa.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer


class ZonesAssignmentsSubWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def set_institution(self, value):
        self.set_text_by_xpath(ZonesConstants.ASSIGNMENTS_TAB_INSTITUTION_XPATH, value)

    def get_institution(self):
        return self.get_text_by_xpath(ZonesConstants.ASSIGNMENTS_TAB_INSTITUTION_XPATH)
