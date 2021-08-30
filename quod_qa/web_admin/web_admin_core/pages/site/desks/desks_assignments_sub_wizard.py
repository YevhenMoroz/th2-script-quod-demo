from quod_qa.web_admin.web_admin_core.pages.common_page import CommonPage
from quod_qa.web_admin.web_admin_core.pages.site.desks.desks_constants import DesksConstants
from quod_qa.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer


class DesksAssignmentsSubWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def set_location_at_description_tab(self, value):
        self.set_combobox_value(DesksConstants.LOCATION_AT_DESCRIPTION_TAB_XPATH, value)

    def get_location_at_description_tab(self):
        return self.get_text_by_xpath(DesksConstants.LOCATION_AT_DESCRIPTION_TAB_XPATH)
