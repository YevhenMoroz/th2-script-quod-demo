from test_framework.web_admin_core.pages.common_page import CommonPage
from test_framework.web_admin_core.pages.users.users.users_constants import UsersConstants
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer


class UsersAssignmentsSubWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def click_on_desks(self):
        self.find_by_xpath(UsersConstants.DESKS_AT_ASSIGNMENTS_SUB_WIZARD).click()

    def set_desks(self, value: list):
        self.set_multiselect_field_value(UsersConstants.DESKS_AT_ASSIGNMENTS_SUB_WIZARD, value)

    def set_location(self, value):
        self.set_combobox_value(UsersConstants.LOCATION_AT_ASSIGNMENTS_SUB_WIZARD, value)

    def get_location(self):
        return self.get_text_by_xpath(UsersConstants.LOCATION_AT_ASSIGNMENTS_SUB_WIZARD)

    def set_zone(self, value):
        self.set_combobox_value(UsersConstants.ZONE_AT_ASSIGNMENTS_SUB_WIZARD, value)

    def get_zone(self):
        return self.get_text_by_xpath(UsersConstants.ZONE_AT_ASSIGNMENTS_SUB_WIZARD)

    def click_on_zone_link(self):
        self.find_by_xpath(UsersConstants.SELECTED_ZONE_URL_AT_ASSIGNMENTS_SUB_WIZARD).click()

    def set_institution(self, value):
        self.set_combobox_value(UsersConstants.INSTITUTION, value)

    def get_institution(self):
        return self.get_text_by_xpath(UsersConstants.INSTITUTION)

    def click_on_institution_field(self):
        self.find_by_xpath(UsersConstants.INSTITUTION).click()

    def is_desks_field_enabled(self):
        return self.find_by_xpath(UsersConstants.DESKS_AT_ASSIGNMENTS_SUB_WIZARD).is_enabled()

    def is_desks_field_displayed(self):
        return self.is_element_present(UsersConstants.DESKS_AT_ASSIGNMENTS_SUB_WIZARD)

    def is_location_field_enabled(self):
        return self.find_by_xpath(UsersConstants.LOCATION_AT_ASSIGNMENTS_SUB_WIZARD).is_enabled()

    def is_location_field_displayed(self):
        return self.is_element_present(UsersConstants.LOCATION_AT_ASSIGNMENTS_SUB_WIZARD)

    def is_zone_field_enabled(self):
        return self.find_by_xpath(UsersConstants.ZONE_AT_ASSIGNMENTS_SUB_WIZARD).is_enabled()

    def is_zone_field_displayed(self):
        return self.is_element_present(UsersConstants.ZONE_AT_ASSIGNMENTS_SUB_WIZARD)

    def is_institution_field_enabled(self):
        return self.find_by_xpath(UsersConstants.INSTITUTION).is_enabled()

    def is_institution_field_displayed(self):
        return self.is_element_present(UsersConstants.INSTITUTION)

    def clear_assignments_tab(self):
        if self.is_desks_field_displayed():
            selected_desks = self.get_text_by_xpath(UsersConstants.DESKS_AT_ASSIGNMENTS_SUB_WIZARD)
            if self.is_desks_field_enabled() and len(selected_desks) > 1:
                self.set_desks([_.strip() for _ in selected_desks.split(",")])
        if self.is_location_field_displayed():
            if self.is_location_field_enabled():
                self.set_text_by_xpath(UsersConstants.LOCATION_AT_ASSIGNMENTS_SUB_WIZARD, "")
        if self.is_zone_field_displayed():
            if self.is_zone_field_enabled():
                self.set_text_by_xpath(UsersConstants.ZONE_AT_ASSIGNMENTS_SUB_WIZARD, "")
        if self.is_institution_field_displayed():
            if self.is_institution_field_enabled():
                self.set_text_by_xpath(UsersConstants.INSTITUTION, "")

    def is_not_found_option_displayed(self):
        return self.is_element_present(UsersConstants.NOT_FOUND_OPTION_XPATH)

    def select_technical_user_checkbox(self):
        self.find_by_xpath(UsersConstants.TECHNICAL_USER_CHECKBOX_AT_ASSIGNMENTS_SUB_WIZARD).click()

    def is_technical_user_selected(self):
        return self.is_checkbox_selected(UsersConstants.TECHNICAL_USER_CHECKBOX_AT_ASSIGNMENTS_SUB_WIZARD)

    def select_head_of_desk_checkbox(self):
        self.find_by_xpath(UsersConstants.HEAD_OF_DESK_AT_ASSIGNMENTS_SUB_WIZARD).click()

    def is_head_of_desk_selected(self):
        return self.is_checkbox_selected(UsersConstants.HEAD_OF_DESK_AT_ASSIGNMENTS_SUB_WIZARD)

    def is_head_of_desk_enabled(self):
        return self.find_by_xpath(UsersConstants.HEAD_OF_DESK_AT_ASSIGNMENTS_SUB_WIZARD_INPUT).is_enabled()
