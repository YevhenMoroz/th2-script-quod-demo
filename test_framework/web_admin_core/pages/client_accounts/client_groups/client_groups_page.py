import time

from test_framework.web_admin_core.pages.client_accounts.client_groups.client_groups_constants import \
    ClientGroupsConstants
from test_framework.web_admin_core.pages.common_page import CommonPage

from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer


class ClientGroupsPage(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def click_on_more_actions(self):
        self.find_by_xpath(ClientGroupsConstants.MORE_ACTIONS_XPATH).click()

    def click_on_edit(self):
        self.find_by_xpath(ClientGroupsConstants.EDIT_XPATH).click()

    def click_on_clone(self):
        self.find_by_xpath(ClientGroupsConstants.CLONE_XPATH).click()

    def click_on_delete(self, confirmation):
        self.find_by_xpath(ClientGroupsConstants.DELETE_XPATH).click()
        if confirmation:
            time.sleep(2)
            self.find_by_xpath(ClientGroupsConstants.OK_BUTTON_XPATH).click()
        else:
            self.find_by_xpath(ClientGroupsConstants.CANCEL_BUTTON_XPATH).click()

    def click_download_pdf_entity_button_and_check_pdf(self, value):
        self.clear_download_directory()
        self.find_by_xpath(ClientGroupsConstants.DOWNLOAD_PDF_BUTTON_XPATH).click()
        time.sleep(2)
        return self.is_pdf_contains_value(value)

    def click_on_pin_row(self):
        self.find_by_xpath(ClientGroupsConstants.PIN_ROW_XPATH).click()

    def click_on_new(self):
        self.find_by_xpath(ClientGroupsConstants.NEW_BUTTON_XPATH).click()

    def click_on_user_icon(self):
        self.find_by_xpath(ClientGroupsConstants.USER_ICON_AT_RIGHT_CORNER).click()

    def click_on_logout(self):
        self.find_by_xpath(ClientGroupsConstants.LOGOUT_BUTTON_XPATH).click()

    def set_name(self, value):
        self.set_text_by_xpath(ClientGroupsConstants.MAIN_PAGE_NAME_FILTER_XPATH, value)

    def set_description(self, value):
        self.set_text_by_xpath(ClientGroupsConstants.MAIN_PAGE_DESCRIPTION_FILTER_XPATH, value)

    def set_fix_user(self, value):
        self.set_text_by_xpath(ClientGroupsConstants.MAIN_PAGE_FIX_USER_FILTER_XPATH, value)

    def set_booking_inst(self, value):
        self.set_text_by_xpath(ClientGroupsConstants.MAIN_PAGE_BOOKING_INST_FILTER_XPATH, value)

    def set_allocation_preference(self, value):
        self.set_text_by_xpath(ClientGroupsConstants.MAIN_PAGE_ALLOCATION_PREFERENCE_FILTER_XPATH, value)

    def set_rounding_direction(self, value):
        self.set_text_by_xpath(ClientGroupsConstants.MAIN_PAGE_ROUNDING_DIRECTION_FILTER_XPATH, value)

    def get_name(self):
        return self.find_by_xpath(ClientGroupsConstants.MAIN_PAGE_NAME_XPATH).text

    def get_description(self):
        return self.find_by_xpath(ClientGroupsConstants.MAIN_PAGE_DESCRIPTION_XPATH).text

    def get_fix_user(self):
        return self.find_by_xpath(ClientGroupsConstants.MAIN_PAGE_FIX_USER_XPATH).text

    def get_booking_inst(self):
        return self.find_by_xpath(ClientGroupsConstants.MAIN_PAGE_BOOKING_INST_XPATH).text

    def get_allocation_preference(self):
        return self.find_by_xpath(ClientGroupsConstants.MAIN_PAGE_ALLOCATION_PREFERENCE_XPATH).text

    def get_rounding_direction(self):
        return self.find_by_xpath(ClientGroupsConstants.MAIN_PAGE_ROUNDING_DIRECTION_XPATH).text

    def is_searched_client_group_found_by_name(self, name):
        return self.is_element_present(ClientGroupsConstants.DISPLAYED_ENTITY_XPATH.format(name))
