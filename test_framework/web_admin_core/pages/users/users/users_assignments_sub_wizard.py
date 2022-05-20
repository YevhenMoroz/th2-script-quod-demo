from test_framework.web_admin_core.pages.common_page import CommonPage
from test_framework.web_admin_core.pages.users.users.users_constants import UsersConstants
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer


class UsersAssignmentsSubWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def click_on_desks(self):
        self.find_by_xpath(UsersConstants.DESKS_AT_ASSIGNMENTS_SUB_WIZARD).click()

    def set_desks(self, value: list):
        self.set_checkbox_list(UsersConstants.DESKS_AT_ASSIGNMENTS_SUB_WIZARD, value)

    def set_location(self, value):
        self.set_combobox_value(UsersConstants.LOCATION_AT_ASSIGNMENTS_SUB_WIZARD, value)

    def get_location(self):
        return self.get_text_by_xpath(UsersConstants.LOCATION_AT_ASSIGNMENTS_SUB_WIZARD)

    def set_zone(self, value):
        self.set_combobox_value(UsersConstants.ZONE_AT_ASSIGNMENTS_SUB_WIZARD, value)

    def get_zone(self):
        return self.get_text_by_xpath(UsersConstants.ZONE_AT_ASSIGNMENTS_SUB_WIZARD)

    def set_institution(self, value):
        self.set_combobox_value(UsersConstants.INSTITUTION, value)

    def get_institution(self):
        return self.get_text_by_xpath(UsersConstants.INSTITUTION)

    def is_desks_field_enabled(self):
        return self.find_by_xpath(UsersConstants.DESKS_AT_ASSIGNMENTS_SUB_WIZARD).is_enabled()

    def is_location_field_enabled(self):
        return self.find_by_xpath(UsersConstants.LOCATION_AT_ASSIGNMENTS_SUB_WIZARD).is_enabled()

    def is_zone_field_enabled(self):
        return self.find_by_xpath(UsersConstants.ZONE_AT_ASSIGNMENTS_SUB_WIZARD).is_enabled()

    def is_institution_field_enabled(self):
        return self.find_by_xpath(UsersConstants.INSTITUTION).is_enabled()
