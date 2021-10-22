from quod_qa.web_admin.web_admin_core.pages.common_page import CommonPage
from quod_qa.web_admin.web_admin_core.pages.site.locations.locations_constants import LocationsConstants
from quod_qa.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer


class LocationsAssignmentsSubWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def set_zone(self, value):
        self.set_combobox_value(LocationsConstants.ASSIGNMENTS_TAB_ZONE_XPATH, value)

    def get_zone(self):
        return self.get_text_by_xpath(LocationsConstants.ASSIGNMENTS_TAB_ZONE_XPATH)

    def click_on_desks(self, desk_name):
        self.find_by_xpath(LocationsConstants.ASSIGNMENTS_TAB_DESKS_XPATH.format(desk_name)).click()

    def click_on_user(self, user_name):
        self.find_by_xpath(LocationsConstants.ASSIGNMENTS_TAB_USERS_LINK_XPATH.format(user_name)).click()
